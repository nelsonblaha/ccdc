# EPCDC — El Paso Community Data Center

Working repo for a proposed El Paso–specific nonprofit that operates AI
infrastructure the community can actually inspect, govern, and trust.

## Why

Meta's El Paso data center was sold on commitments about water use and clean
electricity that residents believe were not kept once the deal closed. At least
one city council member has said publicly they took those commitments at face
value. The trust gap that leaves behind is the opening: a locally-governed,
nonprofit AI provider whose numbers are published rather than promised.

The premise is *local control and verifiable ethics*, not price. We will almost
certainly never beat OpenAI on cost per token. We can beat them on:

- a board El Paso residents can name, meet, and remove
- published water/electricity/carbon figures per unit of compute
- no training on user conversations, contractually and technically
- money that stays in the community

## MVP

A cloud-hosted [Open WebUI](https://openwebui.com/) instance behind a thin
custom layer that handles:

1. a public page explaining the organization
2. donation collection
3. login / accounts / payment
4. the chat interface itself (Open WebUI provides this)

## Status

**Research phase.** Nothing deployed. No entity formed.

## The four findings that matter most

1. **Open WebUI covers ~80–85% of the MVP** and is licensed permissively enough
   to do all of this. The gaps are payments, per-user quotas, a public website,
   and membership records — see doc 01.
2. **Nothing in the license prevents any of this.** It is BSD-3-Clause plus one
   branding clause. The only thing you cannot do for free is remove the
   "Open WebUI" name above 50 users — and that is enforced in code, not just in
   prose. See doc 02.
3. **Google for Nonprofits provides up to $10,000/year in cloud credits.** That
   plausibly covers hosting *and* inference for ~700 members. The MVP's cash
   cost in year one is close to zero; the real spend is legal. See doc 03.
4. **The membership model as described has a tax problem that must be designed
   around, not retrofitted.** "Members pay dues and receive compute" is a
   cooperative; 501(c)(3) requires public rather than private benefit. There is
   a clean resolution, but it has to be chosen before the certificate of
   formation is filed. See doc 05.

## Docs

| Doc | What's in it |
|---|---|
| [01 — Open WebUI assessment](docs/01-openwebui-assessment.md) | What Open WebUI already does for us, verified against the source at v0.11.0, and the four things it does not do |
| [02 — License & posture](docs/02-license-and-posture.md) | Is this allowed? What the license actually says, the branding gate enforced in code, and how the project is likely to react |
| [03 — Cost model](docs/03-cost-model.md) | Google Cloud, AWS, and frugal options; inference costs; where the money actually goes |
| [04 — MVP architecture](docs/04-mvp-architecture.md) | What to build, in what order |
| [05 — Governance](docs/05-governance.md) | Getting from "a website I set up" to a real nonprofit: entity choice, the charity-vs-cooperative fork, board, voting members, dues, and what actually makes it trustworthy |
| [06 — Open questions](docs/06-open-questions.md) | Everything that needs a human decision or an external answer |

`tools/cost_model.py` is a runnable version of the cost model in doc 03 — change
the assumptions at the top and re-run rather than trusting the numbers in prose.

## Sourcing convention

Because this repo will be shown to prospective board members and donors, every
factual claim is tagged:

- **[code]** — verified by reading Open WebUI source at the pinned commit
- **[docs]** — from official vendor documentation
- **[web]** — from secondary sources; treat as approximate, re-verify before quoting
- **[est]** — our own modeling assumption, not a measured or published figure

Do not remove these tags when editing. If you cannot tag a claim, it does not
belong in a document that a donor might read.
