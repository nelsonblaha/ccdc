"""CCDC site + signup endpoint.

Serves the static site and accepts mailing-list signups, appending them to a
JSONL file on disk. Deliberately small: no database, no third-party form
service, no analytics, no trackers. Replacing a Google Form with forty lines of
our own code is the whole thesis of the organization in miniature.

Signups land in $CCDC_DATA/signups.jsonl and can always be read over SSH.
There is also one authenticated HTTP view of them at /admin, gated by a
password whose hash lives only in the deploy environment. Without both
CCDC_SECRET_KEY and CCDC_ADMIN_PASSWORD_HASH set, that route and its login
page 404 and the page carries no admin markup at all, so a copy of this repo
run by anyone else exposes nothing.
"""

import fcntl
import hashlib
import json
import os
import re
import time
from collections import deque
from pathlib import Path

from datetime import timedelta

from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    request,
    send_from_directory,
    session,
)
from markupsafe import escape
from werkzeug.security import check_password_hash

SITE_DIR = Path(os.environ.get("CCDC_SITE", "/app/site"))
DATA_DIR = Path(os.environ.get("CCDC_DATA", "/data"))
SIGNUP_FILE = DATA_DIR / "signups.jsonl"
# Watermark for the admin tag: what had been seen the last time the list was
# opened. Kept beside the data rather than in the cookie so the tag is right on
# a device that has never seen it.
SEEN_FILE = DATA_DIR / "admin_seen.json"

# Secrets come from the environment only. Both empty is a valid state and means
# "no admin here": the routes disappear and no session can be minted.
SECRET_KEY = os.environ.get("CCDC_SECRET_KEY", "")
ADMIN_HASH_FILE = Path(
    os.environ.get("CCDC_ADMIN_HASH_FILE", str(DATA_DIR / "admin_password_hash"))
)


def _read_admin_hash() -> str:
    """The password hash, from a file first.

    Not from the environment by preference, for a reason worth recording: a
    Werkzeug hash contains '$' as its field separator, and Docker Compose
    interpolates $VAR inside a project .env file. That silently removed the salt
    from the middle of the hash, so the value the container saw was well-formed,
    non-empty, and wrong, and every correct password was rejected. A file also
    keeps the hash out of `docker inspect` and out of the process environment.

    The environment variable still works for deployments that are not Compose,
    but it must not contain an unescaped '$'.
    """
    try:
        from_file = ADMIN_HASH_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        from_file = ""
    return from_file or os.environ.get("CCDC_ADMIN_PASSWORD_HASH", "").strip()


ADMIN_PASSWORD_HASH = _read_admin_hash()

# Login is the one password field on the site, so it gets its own, tighter
# budget than the signup form.
LOGIN_MAX = 8
LOGIN_WINDOW = 900

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

# --------------------------------------------------------------------------
# Canonical host.
#
# chucodata.org is the intended permanent home (doc 06, item 9). ccdc.blaha.io is
# a personal hostname that served the proposal while it had no domain of its own.
#
# The switch is off until the new name is verified serving the site end to end,
# because turning it on early would 301 every visitor to a domain that does not
# resolve yet, and a 301 is exactly the response browsers cache hardest. Flipping
# it also requires the form's absolute action to move in the same commit: a POST
# through a 301 is downgraded to GET by browsers, which would silently break
# signups rather than redirect them.
# --------------------------------------------------------------------------

CANONICAL_HOST = "chucodata.org"
LEGACY_HOSTS = {"ccdc.blaha.io", "epcdc.blaha.io", "www.chucodata.org"}
REDIRECT_LEGACY_HOSTS = os.environ.get("CCDC_CANONICAL_REDIRECT") == "1"
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

# A random key when none is configured: unforgeable, and unusable, which is what
# "no admin" should mean. Sessions are a signed cookie, so there is no store.
app.secret_key = SECRET_KEY or os.urandom(32)
app.config.update(
    SESSION_COOKIE_NAME="ccdc_admin",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=365),
)


def admin_enabled() -> bool:
    return bool(SECRET_KEY and ADMIN_PASSWORD_HASH)


def is_admin() -> bool:
    return admin_enabled() and session.get("admin") is True


def render_page(relative: str) -> Response:
    html = (SITE_DIR / relative).read_text(encoding="utf-8")
    for name, digest in ASSET_VERSIONS.items():
        for prefix in ("", "../"):
            for attr in ("href", "src"):
                html = html.replace(
                    f'{attr}="{prefix}{name}"', f'{attr}="{prefix}{name}?v={digest}"'
                )
    # Placement is in the markup, at <!--JOIN-TAG--> and <!--JOIN-INLINE-->; the
    # count and the destination are decided here. Both markers are replaced
    # unconditionally, so a page never ships a stray comment or a stale count.
    tag, inline = join_markup("es" if relative.startswith("es/") else "en")
    html = html.replace("<!--JOIN-TAG-->", tag)
    html = html.replace("<!--JOIN-INLINE-->", inline)
    return Response(
        html,
        mimetype="text/html",
        headers={
            "Cache-Control": "no-cache, must-revalidate",
            # Cookie is load-bearing twice over: the language choice and now the
            # admin variant. A shared cache must never hand one visitor's copy to
            # another.
            "Vary": "Accept-Language, Cookie",
        },
    )
_hits: dict[str, deque] = {}

# ccdc.blaha.io is canonical and serves the form itself, so it needs no allowance
# of its own; the entry is kept because the pre-rename alias below is a genuine
# cross-origin case. Everything else gets no CORS header and is blocked by the
# browser. The nelsonblaha.github.io entry is gone with GitHub Pages: nothing is
# served from there any more, and an allowance for an origin we no longer control
# the content of is worth exactly nothing to us and something to an attacker.
CORS_ORIGINS = {
    "https://chucodata.org",
    "https://www.chucodata.org",
    # Kept so a page a reader already had open can still post after the move. The
    # redirect deliberately exempts /api/, so those posts arrive here rather than
    # being turned into a GET by a 301.
    "https://ccdc.blaha.io",
    "https://epcdc.blaha.io",
}


@app.before_request
def canonical_redirect():
    """Send the old hostnames to the canonical one, preserving path and query.

    Deliberately not applied to /api/ or /healthz. The API is posted to
    cross-origin by anything still holding an old copy of the page, and a redirect
    there loses the body; the health check is called by Docker with a bare host
    header and has nothing to do with names.
    """
    if not REDIRECT_LEGACY_HOSTS:
        return None
    host = (request.host or "").split(":")[0].lower()
    if host not in LEGACY_HOSTS:
        return None
    if request.path.startswith("/api/") or request.path == "/healthz":
        return None
    target = f"https://{CANONICAL_HOST}{request.full_path.rstrip('?') or '/'}"
    resp = redirect(target, code=301)
    resp.headers["Cache-Control"] = "public, max-age=3600"
    return resp


@app.after_request
def cors(resp):
    origin = request.headers.get("Origin")
    if origin in CORS_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        # Append: assigning here used to discard the Accept-Language and Cookie
        # that the page responses set, which with an admin variant in play would
        # have been a cache-poisoning bug rather than a cosmetic one.
        existing = [v.strip() for v in resp.headers.get("Vary", "").split(",") if v.strip()]
        if "Origin" not in existing:
            existing.append("Origin")
        resp.headers["Vary"] = ", ".join(existing)
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
    """Serves whichever language fits, at one address.

    It used to redirect a Spanish-preferring browser to /es/, which put the
    language into the address bar and therefore into every link anyone copied from
    it. In a metro where the sender's language says nothing about the recipient's,
    that is the wrong thing to hand around: a shared /es/ forces Spanish on whoever
    opens it. Now "/" negotiates and stays "/", so what gets pasted into a group
    chat lets each reader's own browser decide.

    /es/ still serves Spanish at its own URL, so it remains indexable and remains
    available to anyone who wants to send Spanish deliberately.
    """
    chosen = request.cookies.get(CHOICE_COOKIE)
    if chosen in MESSAGES:
        lang = chosen
    elif prefers_spanish(request.headers.get("Accept-Language", "")):
        lang = "es"
    else:
        lang = "en"
    # render_page sets Vary: Accept-Language, Cookie, which this depends on twice
    # over: a cache must never serve one visitor's language to another.
    return render_page("es/index.html" if lang == "es" else "index.html")


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



# --------------------------------------------------------------------------
# Admin: one password, one signed cookie, one list view.
#
# Deliberately self-contained. Nothing here knows or cares that the site is
# currently served from a blaha.io hostname: the cookie is scoped to whatever
# host served the page, so moving to another domain means setting a new secret
# and signing in once. The throwaway part of this is the smallest part.
#
# The list is the most sensitive thing the box holds. It stays behind a single
# route that does one thing, with no search, no export and no API.
# --------------------------------------------------------------------------

_login_hits: dict[str, deque] = {}


def login_limited(ip: str) -> bool:
    now = time.time()
    q = _login_hits.setdefault(ip, deque())
    while q and now - q[0] > LOGIN_WINDOW:
        q.popleft()
    if len(q) >= LOGIN_MAX:
        return True
    q.append(now)
    if len(_login_hits) > 2000:
        for k in [k for k, v in _login_hits.items() if not v or now - v[-1] > LOGIN_WINDOW]:
            _login_hits.pop(k, None)
    return False


def read_signups() -> list[dict]:
    """Every stored signup, oldest first. Unparseable lines are skipped rather
    than raising: one bad line should never make the whole list unreadable."""
    if not SIGNUP_FILE.exists():
        return []
    out: list[dict] = []
    with open(SIGNUP_FILE, encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_SH)
        try:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except ValueError:
                    continue
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    return out


def read_seen() -> tuple[str, int]:
    try:
        data = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
        return str(data.get("seen_ts") or ""), int(data.get("seen_count") or 0)
    except (OSError, ValueError, TypeError):
        return "", 0


def write_seen(ts: str, count: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SEEN_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"seen_ts": ts, "seen_count": count}), encoding="utf-8")
    os.replace(tmp, SEEN_FILE)  # atomic: never a half-written watermark
    try:
        os.chmod(SEEN_FILE, 0o600)
    except OSError:
        pass


def signup_state() -> dict:
    """Total, how many are new, and whether the tag should be lit.

    Both a timestamp and a count are compared. The count alone would go wrong
    the first time a junk entry is deleted; the timestamp alone would go wrong
    for two signups inside the same second, since timestamps are second
    resolution. Either one moving means there is something unseen.
    """
    recs = read_signups()
    total = len(recs)
    newest = max((str(r.get("ts") or "") for r in recs), default="")
    seen_ts, seen_count = read_seen()
    unseen = max(total - seen_count, 0)
    active = bool(total) and (total != seen_count or newest > seen_ts)
    return {"total": total, "unseen": unseen, "active": active, "newest": newest, "records": recs}


# Counts the founder, who is on the list in every sense except having submitted
# the form. Set to 0 to show the stored count alone.
FOUNDER_OFFSET = 1

JOIN_WORDS = {
    "en": {"lead": "join", "one": "other", "many": "others"},
    "es": {"lead": "\u00fanete a", "one": "persona", "many": "personas"},
}


def join_markup(lang: str) -> tuple[str, str]:
    """(edge tag, inline text) for the join count.

    Public: every visitor sees the same words and the same number. What differs
    is where it goes. A visitor's tag opens the signup form, which is the whole
    point of showing a count next to an invitation; the administrator's goes to
    the list, and is the only trace of /admin anywhere in the markup.

    Empty strings when there is nothing to count, so an empty list never
    advertises itself.
    """
    st = signup_state()
    if not st["total"]:
        return "", ""
    # The founder never filled in his own form, so the stored rows are one short
    # of the people actually on the hook for this. The public number counts him;
    # /admin shows the stored rows and says so, so the two never look like a
    # discrepancy.
    total = st["total"] + FOUNDER_OFFSET
    w = JOIN_WORDS.get(lang, JOIN_WORDS["en"])
    unit = w["one"] if total == 1 else w["many"]
    admin = is_admin()
    # The lit state is only ever visible to the administrator: a visitor has no
    # watermark, so their tag is never in it.
    lit = " is-new" if admin and st["active"] else ""
    tag = (
        f'<a class="jointag{lit}{" is-admin" if admin else ""}" '
        f'href="{"/admin" if admin else "#signup"}">'
        f'<span class="jt-lead">{w["lead"]}</span>'
        f'<span class="jt-n">{total}</span>'
        f'<span class="jt-unit">{unit}</span></a>'
    )
    # Always a span: this now renders inside the signup button, and an anchor
    # nested in an anchor is invalid and behaves unpredictably. The administrator
    # keeps a route to the list through the edge tab, which .is-admin reveals at
    # phone widths where it is otherwise hidden.
    inline = f'<span class="joininline">{w["lead"]} <b>{total}</b> {unit}</span>'
    return tag, inline


def _admin_shell(title: str, inner: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{escape(title)} &middot; CCDC</title>
<style>
:root {{ color-scheme: light dark; --bg:#ECEDF1; --fg:#15171E; --dim:#4C5164;
  --line:#D2D5DE; --card:#FFFFFF; --sun:#C77503; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#101219; --fg:#E9EBF1;
  --dim:#A2A8BC; --line:#2B2F3B; --card:#181B23; --sun:#F0A32C; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); padding:1.5rem;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; line-height:1.5; }}
main {{ max-width:60rem; margin:0 auto; display:flex; flex-direction:column; gap:1.25rem; }}
h1 {{ font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace; font-size:1.3rem;
  letter-spacing:-0.02em; margin:0; }}
a {{ color:inherit; text-underline-offset:3px; }}
.row {{ display:flex; gap:1rem; align-items:baseline; flex-wrap:wrap; }}
.dim {{ color:var(--dim); font-size:.85rem; }}
label {{ display:block; font-size:.8rem; color:var(--dim); margin-bottom:.35rem;
  text-transform:uppercase; letter-spacing:.08em; }}
input[type=password] {{ width:100%; padding:.7rem .8rem; font-size:1rem; color:var(--fg);
  background:var(--card); border:1px solid var(--line); border-radius:.35rem; }}
button {{ padding:.7rem 1.1rem; font:inherit; font-weight:600; cursor:pointer;
  color:#15171E; background:var(--sun); border:0; border-radius:.35rem; }}
form.inline {{ display:inline; }}
form.inline button {{ background:none; color:var(--dim); border:1px solid var(--line);
  font-weight:400; font-size:.85rem; padding:.35rem .7rem; }}
.err {{ color:#E4776A; font-size:.9rem; }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
th,td {{ text-align:left; padding:.55rem .6rem; border-bottom:1px solid var(--line);
  vertical-align:top; }}
th {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--dim);
  font-weight:600; }}
td.ts {{ white-space:nowrap; font-variant-numeric:tabular-nums; color:var(--dim);
  font-size:.82rem; }}
td.contact {{ font-family:ui-monospace,Menlo,monospace; word-break:break-all; }}
tr.new td {{ background:color-mix(in srgb, var(--sun) 12%, transparent); }}
.tags {{ display:flex; flex-wrap:wrap; gap:.25rem; }}
.tag {{ font-size:.72rem; padding:.1rem .4rem; border:1px solid var(--line);
  border-radius:.25rem; color:var(--dim); }}
.scroll {{ overflow-x:auto; }}
.empty {{ padding:2rem; text-align:center; color:var(--dim); border:1px dashed var(--line);
  border-radius:.4rem; }}
</style></head>
<body><main>{inner}</main></body></html>"""


@app.get("/login")
def login_form():
    if not admin_enabled():
        return Response("Not found", status=404, mimetype="text/plain")
    if is_admin():
        return redirect("/admin", code=303)
    return _login_response()


def _login_response(error: str = "", status: int = 200) -> Response:
    msg = f'<p class="err">{escape(error)}</p>' if error else ""
    body = f"""<h1>Sign in</h1>
<p class="dim">Administrator access to the mailing list.</p>
{msg}
<form method="post" action="/login">
  <label for="p">Password</label>
  <input id="p" name="password" type="password" autocomplete="current-password" required>
  <p><button type="submit">Sign in</button></p>
</form>
<p class="dim"><a href="/">&larr; Back to the site</a></p>"""
    resp = Response(_admin_shell("Sign in", body), status=status, mimetype="text/html")
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Robots-Tag"] = "noindex, nofollow"
    return resp


@app.post("/login")
def login():
    if not admin_enabled():
        return Response("Not found", status=404, mimetype="text/plain")
    if login_limited(client_ip()):
        return _login_response("Too many attempts. Try again later.", 429)
    supplied = (request.form.get("password") or "")
    # check_password_hash compares in constant time and the failure text is the
    # same either way, so neither timing nor wording says whether a password
    # exists to guess at.
    if not check_password_hash(ADMIN_PASSWORD_HASH, supplied):
        app.logger.warning("admin login failed from %s", client_ip())
        return _login_response("That password is not right.", 401)
    session.clear()
    session.permanent = True
    session["admin"] = True
    app.logger.info("admin signed in from %s", client_ip())
    return redirect("/admin", code=303)


@app.post("/logout")
def logout():
    session.clear()
    return redirect("/", code=303)


@app.get("/admin")
def admin():
    if not admin_enabled():
        return Response("Not found", status=404, mimetype="text/plain")
    if not is_admin():
        return redirect("/login", code=303)

    st = signup_state()
    seen_ts, seen_count = read_seen()
    recs = st["records"]
    # Newest first, and mark the ones that arrived since the last visit before
    # the watermark moves.
    fresh_from = len(recs) - st["unseen"]
    rows = []
    for i, r in reversed(list(enumerate(recs))):
        tags = "".join(f'<span class="tag">{escape(h)}</span>' for h in (r.get("help") or []))
        rows.append(
            "<tr{cls}>"
            '<td class="ts">{ts}</td>'
            '<td class="contact">{contact}</td>'
            "<td>{name}</td>"
            '<td><div class="tags">{tags}</div></td>'
            "<td>{note}</td>"
            '<td class="ts">{lang}</td>'
            "</tr>".format(
                cls=' class="new"' if i >= fresh_from else "",
                ts=escape(str(r.get("ts") or "")).replace("T", " ").replace("Z", ""),
                contact=escape(str(r.get("contact") or "")),
                name=escape(str(r.get("name") or "")) or '<span class="dim">&mdash;</span>',
                tags=tags or '<span class="dim">&mdash;</span>',
                note=escape(str(r.get("note") or "")) or '<span class="dim">&mdash;</span>',
                lang=escape(str(r.get("lang") or "")),
            )
        )

    table = (
        '<div class="scroll"><table><thead><tr>'
        "<th>When (UTC)</th><th>Contact</th><th>Name</th><th>Offered to help</th>"
        "<th>Note</th><th>Filled in</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        if rows
        else '<p class="empty">No signups yet.</p>'
    )
    since = (
        f"{st['unseen']} new since you last looked."
        if st["unseen"]
        else "Nothing new since you last looked."
    )
    body = f"""<div class="row">
  <h1>Mailing list</h1>
  <span class="dim">{st['total']} stored &middot; {escape(since)}</span>
  <span style="margin-left:auto">
    <form class="inline" method="post" action="/logout"><button type="submit">Sign out</button></form>
  </span>
</div>
{table}
<p class="dim">The public page says <strong>{st['total'] + FOUNDER_OFFSET}</strong>, which is
these {st['total']} plus you: FOUNDER_OFFSET in app.py counts the founder, who never
submitted the form. Set it to 0 to publish the stored count alone.</p>
<p class="dim">Stored at {escape(str(SIGNUP_FILE))} on the host, mode 0600, and readable
over SSH. This page is the only route that returns any of it.</p>
<p class="dim"><a href="/">&larr; Back to the site</a></p>"""

    # The watermark moves only once the list has actually been rendered.
    write_seen(st["newest"], st["total"])
    resp = Response(_admin_shell("Mailing list", body), mimetype="text/html")
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Robots-Tag"] = "noindex, nofollow"
    return resp

def _plain_page(title: str, body: str, lang: str = "en") -> str:
    m = MESSAGES[lang]
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &middot; Chucodata</title>
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
