# CCDC — Chuco Community Data Center

**Centro Comunitario de Datos de Chuco**

Working repo for a proposed nonprofit serving the El Paso–Ciudad Juárez metro,
operating AI infrastructure the community can actually inspect, govern, and
trust. "El Chuco" is the local nickname for El Paso — used here because it reads
as the place people live in rather than a municipal government, and because it
has never stopped at the river (doc 11).

## Why

Meta's El Paso data center was sold on commitments about water use and clean
electricity that residents believe were not kept once the deal closed. At least
one city council member has said publicly they took those commitments at face
value. The trust gap that leaves behind is the opening: a locally-governed,
nonprofit AI provider whose numbers are published rather than promised.

The water and the air are shared with Juárez, so the response is binational too —
an organization arguing for local accountability over a shared aquifer that drew
its own line at the river would be making a weaker version of its own case.

The premise is *local control and verifiable ethics*, not price. We will almost
certainly never beat OpenAI on cost per token. We can beat them on:

- a board residents can name, meet, and remove
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
4. **A nonprofit can charge for AI. It just cannot run a closed buyers' club.**
   501(c)(3)s sell services routinely, and fee income related to the exempt
   purpose is not even taxed — surplus reinvested is simply what a nonprofit is.
   The constraints are that the beneficiary class must be broader than the class
   of payers, and that pricing must not look commercial. This shapes the
   certificate of formation, so it has to be decided before filing. See doc 05.

## Docs

| Doc | What's in it |
|---|---|
| [01 — Open WebUI assessment](docs/01-openwebui-assessment.md) | What Open WebUI already does for us, verified against the source at v0.11.0, and the four things it does not do |
| [02 — License & posture](docs/02-license-and-posture.md) | Is this allowed? What the license actually says, the branding gate enforced in code, and how the project is likely to react |
| [03 — Cost model](docs/03-cost-model.md) | Google Cloud, AWS, and frugal options; inference costs; where the money actually goes |
| [04 — MVP architecture](docs/04-mvp-architecture.md) | What to build, in what order |
| [05 — Governance](docs/05-governance.md) | Getting from "a website I set up" to a real nonprofit: entity choice, the charity-vs-cooperative fork, board, voting members, dues, and what actually makes it trustworthy |
| [06 — Open questions](docs/06-open-questions.md) | Everything that needs a human decision or an external answer |
| [07 — Roadmap](docs/07-roadmap.md) | Twelve steps from paperwork to owning hardware, with the detail behind each |
| [08 — Beyond AI](docs/08-beyond-ai.md) | Why AI is the wedge and not the point: the shared-server argument, and the organizations already doing this |
| [09 — Publishing](docs/09-publishing.md) | How `site/` gets deployed, and the public-repo decision |
| [11 — Binational scope](docs/11-binational-scope.md) | Serving Ciudad Juárez, why the name changed, and the one question that needs a Mexican lawyer |
| [10 — The repo as a governance mechanism](docs/10-repo-as-governance.md) | Requiring director signatures to change the organization's commitments — why signatures beat permissions, why not unanimity, and the four ways it breaks |
| [GOVERNED.md](GOVERNED.md) | The operative version: which paths are organizational commitments, and what approval each tier needs. Written to be cited by the bylaws. |

## The public pitch

`site/index.html` (English) and `site/es/index.html` (Spanish) are the
advertisement, sharing `site/style.css` and `site/script.js` so the two cannot
drift. It's what you send people. Everything in `docs/` is the evidence behind
it, which is the whole point: the claims on the site are checkable against the
research in this repo.

Signup form: <https://docs.google.com/forms/d/e/1FAIpQLSff0rCCyxWvrcFeuTxaHyQrNMDb3yvZg5OyNvlqQu_T3Doxkw/viewform>

`tools/cost_model.py` is a runnable version of the cost model in doc 03 — change
the assumptions at the top and re-run rather than trusting the numbers in prose.

## Why this is all public

Including the parts that aren't flattering. `docs/05` works through how a
founder-controlled board fails an independence test and what it would take to
pay the founder defensibly. `docs/06` is a list of everything still unresolved.
`docs/03` is the entire budget.

An organization whose pitch is *don't take our word for it* has no business
keeping its own risk assessment private. If you're deciding whether to join,
donate, or serve on the board, you should be able to read exactly what we know
and what we don't.

These documents were drafted for the founder and address the reader as "you" in
places. Read them as working notes, not marketing.

## Sourcing convention

Because this repo will be shown to prospective board members and donors, every
factual claim is tagged:

- **[code]** — verified by reading Open WebUI source at the pinned commit
- **[docs]** — from official vendor documentation
- **[web]** — from secondary sources; treat as approximate, re-verify before quoting
- **[est]** — our own modeling assumption, not a measured or published figure

Do not remove these tags when editing. If you cannot tag a claim, it does not
belong in a document that a donor might read.
