"""EPCDC site + signup endpoint.

Serves the static site and accepts mailing-list signups, appending them to a
JSONL file on disk. Deliberately small: no database, no third-party form
service, no analytics, no trackers. Replacing a Google Form with forty lines of
our own code is the whole thesis of the organization in miniature.

Signups land in $EPCDC_DATA/signups.jsonl. Read them over SSH; there is no
HTTP endpoint that returns stored contact details, on purpose.
"""

import fcntl
import json
import os
import re
import time
from collections import deque
from pathlib import Path

from flask import Flask, Response, jsonify, redirect, request, send_from_directory

SITE_DIR = Path(os.environ.get("EPCDC_SITE", "/app/site"))
DATA_DIR = Path(os.environ.get("EPCDC_DATA", "/data"))
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

app = Flask(__name__, static_folder=None)
_hits: dict[str, deque] = {}

# epcdc.blaha.io is canonical. The GitHub Pages copy is a mirror whose form
# posts here cross-origin, so it needs an explicit allowance. Everything else
# gets no CORS header and is blocked by the browser.
CORS_ORIGINS = {
    "https://epcdc.blaha.io",
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


def wants_json() -> bool:
    return (
        request.headers.get("X-Requested-With") == "fetch"
        or "application/json" in request.headers.get("Accept", "")
    )


def fail(msg: str, code: int = 400):
    if wants_json():
        return jsonify({"ok": False, "error": msg}), code
    return Response(_plain_page("Something went wrong", msg), status=code, mimetype="text/html")


@app.post("/api/signup")
def signup():
    form = request.form if request.form else (request.get_json(silent=True) or {})

    # Honeypot: a field hidden from people and irresistible to bots.
    if (form.get("website") or "").strip():
        return jsonify({"ok": True}) if wants_json() else redirect("/thanks", code=303)

    try:
        elapsed = time.time() - float(form.get("t") or 0)
    except (TypeError, ValueError):
        elapsed = 0.0
    if elapsed < MIN_FILL_SECONDS:
        return fail("That submitted faster than a person can type. Try again.", 429)

    if rate_limited(client_ip()):
        return fail("Too many signups from this address. Try again later.", 429)

    contact = (form.get("contact") or "").strip()[:MAX_FIELD]
    if not contact:
        return fail("An email address or phone number is required.")
    kind = classify(contact)
    if not kind:
        return fail("That doesn't look like an email address or a phone number.")

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
        }
    )
    # Never log the contact itself — container logs are not a place for PII.
    app.logger.info("signup recorded (%s)", kind)

    if wants_json():
        return jsonify({"ok": True})
    return redirect("/thanks", code=303)


@app.get("/thanks")
def thanks():
    return Response(
        _plain_page(
            "You're on the list.",
            "That's the whole thing. We'll email when there's something real to "
            "report — a board, a filing, a service you can actually use.",
        ),
        mimetype="text/html",
    )


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "signups_file": SIGNUP_FILE.exists()})


@app.get("/")
def index():
    return send_from_directory(SITE_DIR, "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(SITE_DIR, path)


def _plain_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} &middot; El Paso Community Data Center</title>
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
<p><a href="/">&larr; Back to the proposal</a></p>
</main></body></html>"""
