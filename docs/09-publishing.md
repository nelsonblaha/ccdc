# Publishing the site

`site/index.html` is the public advertisement — a single self-contained file,
no build step, no dependencies, no external requests.

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

Point 2 is the decision, and it is not only about the site. **Making `epcdc`
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
| **A — Separate public repo** | New public `epcdc-site` holding only `site/`. `epcdc` stays private. | Two repos to keep in sync; the site loses its link to the evidence behind it |
| **B — Make `epcdc` public** | Site *and* research go public. The radical-transparency play. | Irreversible in practice — search engines and archives cache |
| **C — Publish elsewhere** | Cloudflare Pages, Netlify, or a plain VM serve a private repo's contents for free | One more account; no GitHub Pages dependency |

**Recommendation: A now, B later.** Ship the site immediately without deciding
the harder question, then move to B once the docs have been reread with a public
audience in mind. B is the more on-message answer and probably where this ends
up — but it should happen because it was chosen, not because Pages needed it.

## Enabling Pages once the repo is public

```bash
gh api -X POST repos/nelsonblaha/epcdc/pages \
  -f 'build_type=workflow'
gh workflow run pages.yml --repo nelsonblaha/epcdc
```

Then the site is at `https://nelsonblaha.github.io/epcdc/`. A custom domain
(`epcdc.org` or similar) needs a `CNAME` file in `site/` and a DNS record.

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
