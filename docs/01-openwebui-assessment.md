# Open WebUI: what it already does for us

Assessed against the source, not the marketing page.

- Repo: `https://github.com/open-webui/open-webui`
- Version assessed: **v0.11.0**
- Commit: `01f4282f1ffe0d6212f58d3afbeae21fffd0c4be` (2026-07-27)

## Short answer

Open WebUI covers roughly **80–85% of the MVP**, and specifically covers the
hard, boring 80% — the chat UI, streaming, auth, accounts, RBAC, file handling,
RAG, admin. What it does *not* cover is exactly the part that makes this a
membership nonprofit rather than a hobby site: **money and quotas.**

## What you get for free

### Chat surface — complete

Model-agnostic chat against Ollama, OpenAI, Anthropic, or any OpenAI-compatible
endpoint. Side-by-side model comparison, per-model system prompts and
parameters. **[docs]**

Feature-by-feature against ChatGPT:

| ChatGPT feature | Open WebUI | Notes |
|---|---|---|
| Streaming chat, history, folders | ✅ | `src/routes/(app)/c`, `folders` **[code]** |
| File / image upload | ✅ | **[docs]** |
| Web search with citations | ✅ | Multiple providers incl. Brave, Tavily, DuckDuckGo, Firecrawl, SearXNG **[code]** — `backend/open_webui/retrieval/web/` |
| Image generation | ✅ | GPT-Image, Gemini, ComfyUI **[docs]** |
| Voice (STT/TTS, voice calls) | ✅ | **[docs]** |
| Code interpreter / sandbox | ⚠️ | `routers/terminals.py` is a *reverse proxy to an admin-configured terminal server* **[code]** — you supply and secure the sandbox. Also listed as an "enterprise-exclusive offering" **[docs]** |
| Memory | ✅ | `models/memories.py` **[code]** |
| Custom GPTs equivalent | ✅ | Model presets + Python tools + MCP + OpenAPI tool servers **[docs]** |
| Projects / knowledge bases | ✅ | `models/knowledge.py`, 13 vector DBs, hybrid BM25+vector with reranking **[docs]** |
| Deep research | ⚠️ | Agentic retrieval exists; not a packaged "deep research" mode |
| Shared chat links | ✅ | `src/routes/s/`, `models/shared_chats.py` **[code]** |

That is a genuinely competitive surface. The gaps versus ChatGPT are narrower
than the gaps versus ChatGPT's *model quality*, which is a purchasing decision
(doc 03), not a software one.

### Accounts and identity — complete, and better than you need

- Email/password signup and signin **[code]** `routers/auths.py`
- OAuth/OIDC against any provider, LDAP, and SCIM 2.0 provisioning **[code]**
  (`routers/scim.py`, `routers/auths.py:/ldap`, `/admin/config/oauth`)
- API keys per user **[code]** `/api_key` endpoints
- Signin rate limiting: 15 attempts / 180s **[code]**
  `signin_rate_limiter = RateLimiter(..., limit=5 * 3, window=60 * 3)`

Critically for a membership org, **`DEFAULT_USER_ROLE` defaults to
`'pending'`** **[code]** (`config.py:1699`). New signups land in a pending state
an admin must approve. That is the natural hook for "verify this person is a
member in good standing."

### Groups, roles, and per-resource access — complete

`models/access_grants.py` implements grants over
`{resource_type, resource_id, principal_type, principal_id, permission}` where
principal is a user, a group, or the wildcard `anyone`. **[code]**

This means **membership tiers are already expressible**: put Gemini Flash in a
group everyone can reach, put the expensive frontier model in a
`voting-members` group. No code needed — it is admin configuration.

### Usage measurement — present

`routers/analytics.py` exposes **[code]**:

- `/analytics/users` — messages and `input_tokens` / `output_tokens` /
  `total_tokens` **per user**
- `/analytics/tokens` — token usage **per model**
- `/analytics/summary`, `/daily`, `/models/{id}/overview`

So you can *measure* what every member consumed and what it cost you. This is
the raw material for both the transparency reports and the dues model.

### Operations — production-ready

Docker/Kubernetes/pip. S3/GCS/Azure Blob for stateless instances. Redis-backed
sessions for horizontal scaling. OpenTelemetry traces/metrics/logs. **[docs]**
641 environment-variable config keys **[code]** — it is configured, not forked.

## What you have to build

These four are the whole custom scope. Everything else is configuration.

### 1. Payments — nothing exists. Zero.

Grepping the entire backend and frontend for
`stripe|paypal|billing|invoice|checkout|payment` returns **two** hits **[code]**,
both false positives:

- `utils/security_headers.py:113` — the string `payment` inside a
  Permissions-Policy regex
- `internal/db.py:374` — the word "checkout" describing a *connection pool*
  checkout

There is no billing router, no payments model, no subscription concept. Every
donation, dues charge, receipt, and refund is ours to build.

### 2. Per-user quotas / credits — nothing exists

`utils/rate_limit.py` has a `RateLimiter`, but it is used in exactly two
places **[code]**, both in `routers/auths.py`: signin attempts and OAuth token
exchange. There is **no** per-user token budget, no spend cap, no credit
balance, no cutoff.

**This is the load-bearing gap for the membership model.** "Voting members pay
flat dues and get a flat share of the AI output" is, in software terms, a
metered credit ledger with enforcement. Open WebUI measures usage but will not
stop anyone. Without this, one enthusiastic member with a scripting habit can
spend a month of the budget in a weekend.

The hook to build against exists: the **filter `inlet`** mechanism in
`utils/filter.py` / `utils/middleware.py:2521` **[code]** runs a Python function
on every request before it reaches the model. A filter that checks a balance and
raises is the correct insertion point — it is a plugin, not a fork.

### 3. Public-facing site — nothing exists

Frontend routes are only **[code]**: `(app)` (the authenticated application),
`auth`, `error`, `s` (shared chats), `watch`. There is no marketing page, no
about page, no donate page, no membership signup.

Open WebUI is an application you log into, not a website. The explanatory page,
the donation flow, and the member onboarding are a separate small app in front
of it.

### 4. Membership records — nothing exists

Users, groups, and roles exist. "Member in good standing since 2027-03, dues
paid through 2027-12, eligible to vote in the board election" does not. That is
a governance system (doc 05), and it needs to be authoritative *outside* Open
WebUI, with Open WebUI group membership as a downstream projection of it.

## Consequence for the build order

The three custom pieces are not equally urgent:

1. **Public site + donations** — needed for launch, ~1–2 weeks of work
2. **Credit ledger + inlet filter** — needed before opening to more than a
   trusted handful, or the budget is unbounded
3. **Membership system** — needed only when there are actual voting members,
   which is a governance milestone, not a launch milestone

See doc 04.
