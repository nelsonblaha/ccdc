# Chucodata — Chuco Community Data Center

Meta is building a $10 billion AI data center in Northeast El Paso. This is the
working repo for a proposal for an alternative that belongs to the people who
live here: a Texas nonprofit whose board is elected by its members, whose
finances and decisions are published, and whose water and power use is reported
honestly.

Nothing is running yet. No entity is formed. The site is live, the research is
public, and the first step is finding out whether anyone here wants it.

"El Chuco" is the local nickname for El Paso. It is used here because it names
the place people live in rather than a municipal government, and because it has
never stopped at the river (doc 11).

## Why

Meta's El Paso facility was sold on commitments about water and clean
electricity that residents believe were not kept once the deal closed. At least
one city council member has said publicly that they took those commitments at
face value.

This is not here to keep Meta honest. It is here to build something different
that does not ask you to take its word: a service whose numbers are published
rather than promised, run by a board you can name, meet, and remove.

The water and the air are shared with Juárez, so the response is binational too.

The premise is local control and verifiable ethics, not price. This will almost
certainly never beat OpenAI on cost per token. It can beat them on:

- a board residents can name, meet, and remove
- published water, electricity and carbon figures per unit of compute
- conversations that are never used to train anything, by contract and in
  configuration
- money that stays in the community

## What it is

The same sort of AI assistant people pay $20 a month for — chat, document
analysis, research and writing help — run by a nonprofit instead of a company.

The reason a small nonprofit can offer that at all is that the hard part is
done. The chat interface is [Open WebUI](https://openwebui.com/), a mature
open-source project used by organizations far larger than this one. Documents,
web search, voice and per-user permissions are already built and freely
licensed. This would be configuring it, not writing it.

What has to be built on top is small and dull: a public page, accounts and
membership records, and per-user limits so a generous free tier cannot quietly
bankrupt the organization.

No donations are collected, now or on the confirmation page. There is nothing to
donate to yet.

## Status

The site is deployed at <https://chucodata.org/> and takes signups. No entity is
formed, no board exists, no service is running, and no money has changed hands.

## The four findings that matter most

1. **Open WebUI covers about 80–85% of what is needed**, and its license allows
   all of this. What is missing is payments, per-user limits, a public site and
   membership records. Doc 01, verified against the source at v0.11.0.
2. **Nothing in the license prevents any of this.** BSD-3-Clause plus one
   branding clause. The only thing that cannot be done for free is removing the
   Open WebUI name above 50 users, and that is enforced in code rather than only
   in prose. Doc 02.
3. **Google for Nonprofits provides up to $10,000 a year in cloud credits**,
   which plausibly covers hosting and inference for roughly 700 members. The
   cash cost in year one is close to zero. The real spend is legal. Doc 03.
4. **A nonprofit can charge for this. It cannot run a closed buyers' club.**
   501(c)(3)s sell services routinely and related fee income is not taxed;
   surplus reinvested is simply what a nonprofit is. The constraints are that
   the people served must be a broader group than the people paying, and that
   pricing must not look commercial. That shapes the certificate of formation,
   so it has to be settled before filing. Doc 05.

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

`site/index.html` and `site/es/index.html` are the advertisement. They share one
stylesheet and one script, so the two languages cannot drift apart, and both of
those now live in [campaignlanding](https://github.com/nelsonblaha/campaignlanding)
— this page's machinery, with the campaign taken out of it, so the next person
with something to propose does not have to rebuild it. What is left in
`site/style.css` is the one rule that was about these particular words: how wide
the Spanish headline runs.

Everything in `docs/` is the evidence behind them, which is the point: every
claim on the site is checkable against the research here.

Live at <https://chucodata.org/>, in whichever language your browser asks for.
`/es/` and `/en/` name a language explicitly, and `/why`, `/roadmap` and the
other section slugs open the page at that section.

The signup form is ours. It posts to our own server, which appends to a JSONL
file on the host, readable over SSH. No Google Form, no third-party form service,
and nothing that sees the list except us. `deploy/app.py` is now the whole of the
configuration; the code that receives it is campaignlanding, pinned to a tag so a
deploy never picks up an upstream change nobody here decided to take.

`tools/cost_model.py` is a runnable version of the cost model in doc 03. Change
the assumptions at the top and re-run rather than trusting the numbers in prose.

## Why this is all public

Including the parts that are not flattering. Doc 05 works through how a
founder-controlled board fails an independence test, and what it would take to
pay the founder defensibly. Doc 06 is a list of everything still unresolved.
Doc 03 is the entire budget.

An organization whose pitch is *don't take our word for it* has no business
keeping its own risk assessment private. If you are deciding whether to join,
serve on the board, or ignore this, you should be able to read exactly what is
known and what is not.

These documents were drafted for the founder and address the reader as "you" in
places. They are working notes, not marketing.

## Sourcing convention

Because this repo will be shown to prospective board members and donors, every
factual claim is tagged:

- **[code]** — verified by reading Open WebUI source at the pinned commit
- **[docs]** — from official vendor documentation
- **[web]** — from secondary sources; treat as approximate, re-verify before quoting
- **[est]** — our own modeling assumption, not a measured or published figure

Do not remove these tags when editing. If you cannot tag a claim, it does not
belong in a document that a donor might read.
