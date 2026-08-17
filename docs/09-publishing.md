# Publishing the site

`site/index.html` is the public advertisement — a single self-contained file,
no build step, no external requests.

## Canonical: ccdc.blaha.io, self-hosted on nelnet

**`https://ccdc.blaha.io` is the real site.** GitHub Pages is a mirror.

`deploy/` holds a small Flask app that serves the static site *and* accepts
mailing-list signups, in one container. It follows the existing nelnet pattern
exactly: join the external `infra-net`, declare `VIRTUAL_HOST`, and
`nginx-proxy` + `acme-companion` handle routing and TLS automatically — the
same way `git.blaha.io`, `chat.blaha.io`, and the rest already work. `*.blaha.io`
already wildcards to Cloudflare, so **no DNS record is required.**

```bash
# on nelnet, from the repo root
docker compose -f deploy/docker-compose.yml up -d --build
```

### Signups

There is no Google Form, no Mailchimp, no analytics, no trackers, and no
cookies. The form posts to `/api/signup` and the app appends one JSON object per
signup to `/home/ben/ccdc-data/signups.jsonl` (mode 0600).

**There is deliberately no HTTP endpoint that returns stored contact details.**
Read them over SSH:

```bash
nelnet 'wc -l /home/ben/ccdc-data/signups.jsonl'
nelnet 'jq -r "[.ts,.kind,.contact,(.help|join(\",\"))] | @tsv" /home/ben/ccdc-data/signups.jsonl'
nelnet 'jq -r "select(.help|index(\"board\")) | .contact" /home/ben/ccdc-data/signups.jsonl'
```

Abuse controls, in order of usefulness: a honeypot field, a per-IP rate limit
(5/hour), a submit-speed trap, and length caps. The contact value is **never
written to the container logs** — docker logs are not a place for other people's
email addresses.

`ccdc-data/` is gitignored. It must never end up in this repo, which is public.

### Why the form posts to an absolute URL

`https://ccdc.blaha.io/api/signup`, not a relative path. This began as a way to
let a GitHub Pages mirror's form work; Pages is now disabled and the absolute URL
is kept because it also lets a local copy of `site/` post to the real endpoint
while working on the page. `deploy/app.py` allows CORS from `ccdc.blaha.io` and
the pre-rename `epcdc.blaha.io`, and nothing else.

Consequence worth knowing: the form **will not submit from a Claude artifact
preview**, whose CSP blocks all external requests. Artifacts are for reviewing
copy, not for collecting signups.

## Mirror: GitHub Pages

## Decision made (2026-08-16): this repo is public

Option B below was chosen deliberately. The research, the budget, the open
questions, and the analysis of how this project could fail — including how a
founder-controlled board fails the independence test — are all public alongside
the pitch.

That is the point. An organization whose argument is "don't take our word for
it" should not keep its own risk assessment private. Anyone evaluating whether
to join, donate, or serve on the board can read exactly what we know and what we
don't.

The consequence to hold onto: **these documents are now written for a public
audience.** They address the founder directly in places because that is who
they were drafted for, and that's fine — but new material should assume a
skeptical outside reader, not an internal one.

The options as they were weighed:

## Background: GitHub Pages requires a public repo

`.github/workflows/pages.yml` deploys `site/` to GitHub Pages. It will not run
until two things are true:

1. **Pages is enabled** in repo settings with source = "GitHub Actions"
2. **The repository is public** — on a free GitHub plan, Pages from a private
   repo requires a paid plan

Point 2 is the decision, and it is not only about the site. **Making `ccdc`
public publishes `docs/` too**, including:

- `05-governance.md`, which analyses founder compensation, board capture, and
  the ways a founder-controlled board fails the independence test
- `05` and `07`, which discuss what a hostile journalist or council member would
  attack
- `06-open-questions.md`, which is a list of everything unresolved

None of that is embarrassing — arguably it is the strongest possible evidence
the project means what it says, and publishing your own risk analysis is exactly
the behaviour the organization claims to stand for. But it is candid strategy
written for an internal audience, and shipping it publicly should be a
deliberate choice rather than a side effect of wanting a prettier landing page.

### Three options

| | What happens | Cost |
|---|---|---|
| **A — Separate public repo** | New public `ccdc-site` holding only `site/`. `ccdc` stays private. | Two repos to keep in sync; the site loses its link to the evidence behind it |
| **B — Make `ccdc` public** | Site *and* research go public. The radical-transparency play. | Irreversible in practice — search engines and archives cache |
| **C — Publish elsewhere** | Cloudflare Pages, Netlify, or a plain VM serve a private repo's contents for free | One more account; no GitHub Pages dependency |

**Recommendation: A now, B later.** Ship the site immediately without deciding
the harder question, then move to B once the docs have been reread with a public
audience in mind. B is the more on-message answer and probably where this ends
up — but it should happen because it was chosen, not because Pages needed it.

## Pages: disabled, deliberately

GitHub Pages was disabled on 2026-08-17 and `.github/workflows/pages.yml` deleted.
The site is self-hosted at `ccdc.blaha.io` from `deploy/`, which is the version
with the signup endpoint; a Pages copy could only ever be a read-only shadow of it
with a form pointing back here, and two URLs for one page is a way to have a stale
one. `site/` remains plain static files, so Pages can be turned back on in a few
minutes if that ever becomes useful:

```bash
gh api -X POST repos/nelsonblaha/ccdc/pages -f 'build_type=workflow'
```

The next home is expected to be a domain of its own on the new server rather than
`github.io`.

## Editing rules

- The page cites specific figures about Meta, El Paso Water, and El Paso
  Electric. **Every one is attributed and linked in the footer.** If you change
  a number, change the source with it.
- Meta's own position — closed-loop cooling, zero water most of the year, the
  West Texas golf course comparison, the 100% clean energy match — stays on the
  page. Removing it to strengthen the argument would make us the thing we are
  criticizing.
- The "what doesn't exist yet" section is load-bearing. Do not soften it, and
  update it the moment any line becomes untrue.
- No donation solicitation until there is an entity and a fiscal sponsor
  (roadmap 05).
- The disclaimer that this is unaffiliated with the City of El Paso, El Paso
  Water, El Paso Electric, and Meta stays in the footer.
