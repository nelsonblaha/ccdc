"""CCDC site + signup endpoint.

Serves the static site and accepts mailing-list signups, appending them to a
JSONL file on disk. Deliberately small: no database, no third-party form
service, no analytics, no trackers. Replacing a Google Form with forty lines of
our own code is the whole thesis of the organization in miniature.

Signups land in $CCDC_DATA/signups.jsonl. Read them over SSH; there is no
HTTP endpoint that returns stored contact details, on purpose.
"""

import fcntl
import hashlib
import json
import os
import re
import time
from collections import deque
from pathlib import Path

from flask import Flask, Response, jsonify, redirect, request, send_from_directory

SITE_DIR = Path(os.environ.get("CCDC_SITE", "/app/site"))
DATA_DIR = Path(os.environ.get("CCDC_DATA", "/data"))
SIGNUP_FILE = DATA_DIR / "signups.jsonl"

# Rate limit: per-IP sliding window. Generous for humans, useless for scripts.
RATE_MAX = 5
RATE_WINDOW = 3600
# Anything submitted faster than this was not typed by a person.
MIN_FILL_SECONDS = 2.0

MAX_FIELD = 500
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9][0-9\-.() ]{6,19}$")
HELP_CHOICES = {"updates", "board", "legal", "technical", "spread"}

# --------------------------------------------------------------------------
# Asset versioning. style.css and script.js are shared by both language pages,
# so a returning visitor would otherwise run new HTML against a cached old
# stylesheet until max-age expired. The HTML is served no-cache and its asset
# references are rewritten to include a content hash, which makes the assets
# safely immutable and any change visible immediately.
# --------------------------------------------------------------------------

VERSIONED_ASSETS = ("style.css", "script.js")

# --------------------------------------------------------------------------
# Language selection.
#
# "/" adapts to Accept-Language exactly once: if the visitor has never chosen a
# language, and their browser prefers Spanish over English, they are redirected to
# /es/. Everything else is deterministic.
#
# Why a redirect here when switching is otherwise done in place: on first load
# there is no scroll position to preserve, so the redirect costs nothing the
# in-place swap was built to protect, and it avoids showing a Spanish speaker a
# page of English before JavaScript can replace it. Doing this client-side would
# either flash the wrong language or require a blocking script in <head>.
#
# Why the redirect is this narrow:
#   - "/es/" NEVER redirects, so a shared Spanish link always lands on Spanish.
#   - "/" with a `lang` cookie never redirects either. Asking for the English URL
#     after having made a choice gets English. That also makes the no-JS path
#     loop-free: clicking EN on /es/ navigates to "/" and stays there.
#   - The cookie is written only by the client, when the reader actually switches.
#     Its single job is to mean "stop guessing for me", in either direction.
# --------------------------------------------------------------------------

CHOICE_COOKIE = "lang"


def prefers_spanish(header: str) -> bool:
    """True when Accept-Language ranks Spanish above English.

    Absent or unparseable headers mean no preference, which means no redirect.
    """
    best = {}
    for part in (header or "").split(","):
        piece = part.strip()
        if not piece:
            continue
        tag, _, params = piece.partition(";")
        tag = tag.strip().lower()
        quality = 1.0
        for param in params.split(";"):
            key, _, value = param.partition("=")
            if key.strip() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        primary = tag.split("-")[0]
        if primary in ("es", "en"):
            best[primary] = max(best.get(primary, 0.0), quality)
    return best.get("es", 0.0) > best.get("en", 0.0)


def _asset_versions() -> dict[str, str]:
    out = {}
    for name in VERSIONED_ASSETS:
        path = SITE_DIR / name
        if path.exists():
            out[name] = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    return out


app = Flask(__name__, static_folder=None)
ASSET_VERSIONS = _asset_versions()


def render_page(relative: str) -> Response:
    html = (SITE_DIR / relative).read_text(encoding="utf-8")
    for name, digest in ASSET_VERSIONS.items():
        for prefix in ("", "../"):
            for attr in ("href", "src"):
                html = html.replace(
                    f'{attr}="{prefix}{name}"', f'{attr}="{prefix}{name}?v={digest}"'
                )
    return Response(
        html,
        mimetype="text/html",
        headers={"Cache-Control": "no-cache, must-revalidate"},
    )
_hits: dict[str, deque] = {}

# ccdc.blaha.io is canonical. The GitHub Pages copy is a mirror whose form
# posts here cross-origin, so it needs an explicit allowance. Everything else
# gets no CORS header and is blocked by the browser.
CORS_ORIGINS = {
    "https://ccdc.blaha.io",
    "https://epcdc.blaha.io",  # pre-rename alias; drop when nothing points at it
    "https://nelsonblaha.github.io",
}


@app.after_request
def cors(resp):
    origin = request.headers.get("Origin")
    if origin in CORS_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
    return resp


def client_ip() -> str:
    # nginx-proxy sets X-Forwarded-For; take the leftmost entry it appended.
    fwd = request.headers.get("X-Forwarded-For", "")
    return fwd.split(",")[0].strip() or (request.remote_addr or "unknown")


def rate_limited(ip: str) -> bool:
    now = time.time()
    q = _hits.setdefault(ip, deque())
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_MAX:
        return True
    q.append(now)
    if len(_hits) > 5000:  # bound memory; oldest buckets are stale anyway
        for k in [k for k, v in _hits.items() if not v or now - v[-1] > RATE_WINDOW]:
            _hits.pop(k, None)
    return False


def classify(contact: str) -> str | None:
    if EMAIL_RE.match(contact):
        return "email"
    if PHONE_RE.match(contact):
        return "phone"
    return None


def append_signup(record: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with open(SIGNUP_FILE, "a", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    try:
        os.chmod(SIGNUP_FILE, 0o600)
    except OSError:
        pass


# --------------------------------------------------------------------------
# Localization. Two languages, one endpoint: the form posts a `lang` field and
# errors come back in the language the visitor was reading.
# --------------------------------------------------------------------------

MESSAGES = {
    "en": {
        "too_fast": "That submitted faster than a person can type. Try again.",
        "rate": "Too many signups from this address. Try again later.",
        "required": "An email address or phone number is required.",
        "invalid": "That doesn't look like an email address or a phone number.",
        "oops_title": "Something went wrong",
        "thanks_title": "You're on the list.",
        "thanks_body": (
            "That's the whole thing. We'll email when there's something real to "
            "report \u2014 a board, a filing, a service you can actually use."
        ),
        "back": "Back to the proposal",
        "thanks_path": "/thanks",
        "home": "/",
    },
    "es": {
        "too_fast": "Eso se envi\u00f3 m\u00e1s r\u00e1pido de lo que alguien puede escribir. Intenta de nuevo.",
        "rate": "Demasiados registros desde esta direcci\u00f3n. Intenta m\u00e1s tarde.",
        "required": "Hace falta un correo electr\u00f3nico o un tel\u00e9fono.",
        "invalid": "Eso no parece un correo electr\u00f3nico ni un tel\u00e9fono.",
        "oops_title": "Algo sali\u00f3 mal",
        "thanks_title": "Ya est\u00e1s en la lista.",
        "thanks_body": (
            "Eso es todo. Te escribiremos cuando haya algo real que contar: una "
            "junta directiva, un tr\u00e1mite, un servicio que de veras puedas usar."
        ),
        "back": "Volver a la propuesta",
        "thanks_path": "/es/gracias",
        "home": "/es/",
    },
}


def pick_lang() -> str:
    """Language for this request: explicit form field first, then the referring
    path, then English. Never guesses from Accept-Language — a visitor who chose
    a language by clicking should not be second-guessed by their browser."""
    form = request.form if request.form else (request.get_json(silent=True) or {})
    raw = (form.get("lang") or "").strip().lower()
    if raw in MESSAGES:
        return raw
    if "/es/" in (request.referrer or ""):
        return "es"
    return "en"


def wants_json() -> bool:
    return (
        request.headers.get("X-Requested-With") == "fetch"
        or "application/json" in request.headers.get("Accept", "")
    )


def fail(key: str, code: int = 400, lang: str = "en"):
    m = MESSAGES[lang]
    if wants_json():
        return jsonify({"ok": False, "error": m[key]}), code
    return Response(
        _plain_page(m["oops_title"], m[key], lang),
        status=code,
        mimetype="text/html",
    )


@app.post("/api/signup")
def signup():
    form = request.form if request.form else (request.get_json(silent=True) or {})
    lang = pick_lang()
    thanks_path = MESSAGES[lang]["thanks_path"]

    # Honeypot: a field hidden from people and irresistible to bots.
    if (form.get("website") or "").strip():
        return jsonify({"ok": True}) if wants_json() else redirect(thanks_path, code=303)

    try:
        elapsed = time.time() - float(form.get("t") or 0)
    except (TypeError, ValueError):
        elapsed = 0.0
    if elapsed < MIN_FILL_SECONDS:
        return fail("too_fast", 429, lang)

    if rate_limited(client_ip()):
        return fail("rate", 429, lang)

    contact = (form.get("contact") or "").strip()[:MAX_FIELD]
    if not contact:
        return fail("required", 400, lang)
    kind = classify(contact)
    if not kind:
        return fail("invalid", 400, lang)

    raw_help = form.getlist("help") if hasattr(form, "getlist") else (form.get("help") or [])
    if isinstance(raw_help, str):
        raw_help = [raw_help]

    append_signup(
        {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "kind": kind,
            "contact": contact,
            "name": (form.get("name") or "").strip()[:MAX_FIELD] or None,
            "note": (form.get("note") or "").strip()[:2000] or None,
            "help": sorted({h for h in raw_help if h in HELP_CHOICES}),
            # Which language they were reading. Tells us what the list speaks.
            "lang": lang,
        }
    )
    # Never log the contact itself — container logs are not a place for PII.
    app.logger.info("signup recorded (%s, %s)", kind, lang)

    if wants_json():
        return jsonify({"ok": True})
    return redirect(thanks_path, code=303)


def _thanks(lang: str):
    m = MESSAGES[lang]
    return Response(_plain_page(m["thanks_title"], m["thanks_body"], lang), mimetype="text/html")


@app.get("/thanks")
def thanks():
    return _thanks("en")


@app.get("/es/gracias")
def thanks_es():
    return _thanks("es")


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "signups_file": SIGNUP_FILE.exists()})


@app.get("/")
def index():
    if request.cookies.get(CHOICE_COOKIE) is None and prefers_spanish(
        request.headers.get("Accept-Language", "")
    ):
        resp = redirect("/es/", code=302)
        resp.headers["Vary"] = "Accept-Language, Cookie"
        resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        return resp
    resp = render_page("index.html")
    # The response depends on both, so a cache must not serve one visitor's
    # variant to another.
    resp.headers["Vary"] = "Accept-Language, Cookie"
    return resp


@app.get("/es/")
def index_es():
    return render_page("es/index.html")


@app.get("/es")
def index_es_bare():
    return redirect("/es/", code=301)


@app.get("/<path:path>")
def static_files(path: str):
    resp = send_from_directory(SITE_DIR, path)
    if path in VERSIONED_ASSETS:
        # Immutable only when addressed by content hash; otherwise revalidate so
        # the GitHub Pages mirror and any bare link cannot pin a stale copy.
        resp.headers["Cache-Control"] = (
            "public, max-age=31536000, immutable"
            if request.args.get("v")
            else "no-cache, must-revalidate"
        )
    return resp


def _plain_page(title: str, body: str, lang: str = "en") -> str:
    m = MESSAGES[lang]
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &middot; Chuco Community Data Center</title>
<style>
:root {{ color-scheme: light dark; }}
body {{ margin:0; min-height:100vh; display:grid; place-items:center;
  background:#ECEDF1; color:#15171E; padding:2rem;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; line-height:1.6; }}
@media (prefers-color-scheme: dark) {{ body {{ background:#101219; color:#E9EBF1; }} }}
main {{ max-width:32rem; display:flex; flex-direction:column; gap:1rem; }}
h1 {{ font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  font-size:1.6rem; letter-spacing:-0.03em; margin:0; }}
a {{ color:inherit; text-underline-offset:3px; }}
</style></head>
<body><main>
<h1>{title}</h1>
<p>{body}</p>
<p><a href="{m["home"]}">&larr; {m["back"]}</a></p>
</main></body></html>"""
