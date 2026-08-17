# From "a website I set up" to a nonprofit people can trust

> **Not legal advice.** I am not a lawyer. Everything below is research to make
> you a well-prepared client, not a substitute for a Texas nonprofit attorney.
> The one line item in this whole project genuinely worth paying cash for is
> counsel on the bylaws and the exemption application.

## The decision that shapes everything else

You wrote: *"I'd imagine voting members pay flat dues and get a flat share of
the AI output."*

That sentence describes a **cooperative** — a mutual-benefit organization where
members pay in and get value out in proportion to membership. It is a coherent,
honorable structure with a long El Paso-relevant pedigree (rural electric
co-ops were built on exactly this logic). But it is in tension with the other
thing you want, which is **tax-deductible donations from the public**.

The IRS draws a hard line here:

- **501(c)(3)** requires the organization serve "a public rather than a private
  interest" **[web]**. Benefits flowing to private individuals must be
  incidental **both qualitatively** (a byproduct of the public benefit) **and
  quantitatively** (insubstantial in amount) **[web]**.
- A **mutual-benefit corporation cannot obtain 501(c)(3) status** **[web]**.
- The cautionary case is *Korean-American Senior Mutual Association Inc. v.
  Commissioner*, where members paid dues and received member benefits, and the
  IRS moved to revoke exemption on the grounds the organization was not operated
  exclusively for exempt purposes **[web]**.

"Members pay $60/year and receive $60/year worth of AI compute" is, on its face,
a purchase, not a donation. Run naively, it puts the exemption at risk and makes
the dues non-deductible anyway.

**This is fixable, but it has to be designed in from the start, not retrofitted.**

### Three ways to resolve it

**Option A — Charity first, membership as governance only (recommended).**

The organization's *primary* activity is public benefit: free AI access for El
Paso residents who cannot afford commercial subscriptions, digital literacy
programming, public transparency reporting on data center resource use. The
program is open to the public, not gated behind dues.

Membership then buys **governance rights, not compute**: the right to vote for
the board, to attend the annual meeting, to see the books. Any compute
allocation attached to membership is deliberately kept modest and is disclosed
as a quid-pro-quo benefit — the donor's deduction is dues minus the fair market
value of what they received, and the IRS requires written disclosure for
payments over $75 where the donor gets goods or services in return.

This keeps 501(c)(3), keeps deductibility for the donation portion, and keeps
the public-trust story clean: *anyone in El Paso can use it; members govern it.*

**Option B — 501(c)(6) or (c)(4), and give up deductibility.**

Structure honestly as a member organization. Dues can be substantial and tied
directly to compute. Cost: contributions are **not** charitable deductions, you
lose access to Google for Nonprofits' $10,000 in cloud credits (doc 03) and most
grant funding, and "donate to us" becomes a much harder pitch.

**Option C — Two entities.** A 501(c)(3) charity plus a member cooperative,
with an arm's-length services agreement. This is what you would do at scale.
It is absurd overhead for year one — two sets of books, two boards, transfer
pricing between them. Note it as the eventual shape if the member side grows,
and do not build it now.

**Recommendation: Option A.** It gets the credits, the deductions, the grants,
and the trust. It requires you to mean it: the free public program has to be
real and primary, not a fig leaf over a compute club.

### How to define "a flat share of the AI output" so it survives contact with reality

Whatever structure you pick, **do not denominate the member benefit in dollars
or tokens.** Token prices move fast and in both directions — Gemini 3.7 Flash
doubles on 2027-01-01 and Claude Sonnet 5 rises 50% on 2026-09-01 (doc 03). A
bylaw promising "500,000 tokens per month" becomes either trivial or ruinous
within a year.

Denominate it as **an equal share of whatever the board allocates to member
compute for that period**:

> Each member in good standing receives an equal share of the compute budget
> allocated by the board to member use for that quarter. The board publishes
> the allocation, the per-member share, and actual consumption, in advance and
> in arrears.

This is honest, it is inflation-proof, it is deflation-proof, it cannot bankrupt
the organization, and — critically for the founding story — **it is a promise
the organization can always keep.** An organization created in response to
unkeepable commitments should not make an unkeepable commitment in its bylaws.

Mechanically this requires the credit ledger and inlet filter from doc 04. Open
WebUI measures usage but will not enforce a limit **[code]**. The governance
model is not implementable without that ~2.5 weeks of work.

## The staged path

Each stage has a gate. Don't skip; each one makes the next cheaper.

### Stage 0 — Personal project (now)

You, a VM, ten friends. Under 50 users so the Open WebUI branding restriction
does not bind (doc 02). **No donations of any kind.** Taking money before there
is an entity or a fiscal sponsor creates personal tax liability and a bad
paper trail.

*Gate to Stage 1: at least three people who are not you want this to exist and
will say so on the record.*

### Stage 1 — Fiscal sponsorship (the bridge)

The answer to "how do I take tax-deductible donations before I have a
501(c)(3)?" A fiscal sponsor is an existing 501(c)(3) that accepts donations on
your project's behalf for a fee — typically 5–10% **[est]** — and holds them
restricted to your project.

This is the single highest-leverage move for the transition you described,
because it lets you **prove demand before spending $3,000 on formation**. It
also forces early financial discipline: the sponsor's back office will not let
you commingle funds.

Look for a local El Paso or Texas community foundation, or a national tech-
oriented sponsor.

*Gate to Stage 2: enough donation interest, or enough member interest, that the
formation cost is justified. And three people willing to be directors.*

### Stage 2 — Texas nonprofit corporation

- **File Form 202**, Certificate of Formation – Nonprofit Corporation, with the
  Texas Secretary of State. Fee **$25** (plus 2.7% if paying by card) **[web]**.
- Form 202 itself specifies the registered agent, the **purpose**, **whether you
  will have members**, and what happens to assets on dissolution **[web]**.
  These are the mission lock. Get them right at filing; amending later is
  possible but it is a moment of vulnerability.
- **Texas requires at least three directors** (TBOC § 22.204), plus a president
  and a secretary (§ 22.231) **[web]**. You cannot be a one-person nonprofit,
  and you should not want to be.
- Texas nonprofit corporations *may* have members with voting rights, may have
  no members and be board-managed, or may be member-managed with no board. If
  you elect to have no members or no board, § 3.009(1) requires a statement to
  that effect in the certificate **[web]**.

  👉 **Elect to have members at formation.** Retrofitting voting membership onto
  a board-only corporation later means amending the certificate and rewriting
  the bylaws — precisely when the founder's informal authority is hardest to
  give up. Build the constraint before you are tempted to avoid it.
- Adopt **bylaws**. Bylaws must set quorum and voting rules; the statutory
  defaults are a poor fit for most nonprofits and cause deadlock (§ 22.213)
  **[web]**. This is where counsel earns their fee.
- Get an **EIN**, open a **bank account in the corporation's name**, and stop
  paying for anything personally.

*Gate to Stage 3: bylaws adopted, three directors seated, bank account open.*

### Stage 3 — Federal tax exemption

- **Form 1023-EZ**: user fee **$275** **[web]**, requires projected gross
  receipts ≤ $50,000/year for three years and ≤ $250,000 total assets **[web]**.
- **Form 1023 (long form)**: more work, higher fee, far more scrutiny — and a
  much more solid determination.

⚠️ **Recommendation: file the long-form 1023, not the EZ**, despite eligibility.
The EZ is an attestation with almost no review; that is exactly why it is a weak
answer to "why should I trust you?" More importantly, the member-benefit
question above is a genuinely contestable one, and a full 1023 that describes the
membership model up front and receives a favorable determination is worth
enormously more than an EZ that never asked. An organization founded on
"someone made promises nobody verified" should choose the process with
verification in it.

- Apply to **Stripe's nonprofit rate** the day the determination letter arrives
  (doc 03) — it is not retroactive **[web]**.
- Apply to **Google for Nonprofits** for the cloud credits (doc 03).
- Apply for **Texas franchise tax and sales tax exemption** separately —
  federal exemption does not grant state exemption automatically.

*Gate to Stage 4: determination letter in hand.*

### Stage 4 — Members and elections

Open membership. Hold the first annual meeting. Elect the board. Publish the
first annual report and Form 990.

## What actually makes it trustworthy

Legal structure is table stakes; plenty of untrustworthy organizations are
properly incorporated. Trust comes from **irreversible commitments and
verifiable numbers.** Given that this organization exists because commitments
were made and not kept, its founding documents should be unusually hard to walk
back.

### Structural — hard to reverse

1. **Purpose and dissolution clauses in the certificate of formation.** Assets
   on dissolution go to another 501(c)(3) with a similar purpose — never to
   members, never to the founder. This is required for exemption anyway; make it
   specific and public.
2. **Supermajority lock on core commitments.** Bylaws requiring, say, a 3/4 vote
   of voting members — not just the board — to amend the purpose clause, to sell
   substantially all assets, or to change the data commitments below. A board
   can be captured; a membership is harder to capture quietly.
3. **Member-elected board majority.** Most seats elected by members, staggered
   terms, term limits. Reserve at most a minority of seats for appointment.
4. **No founder veto, or an explicit sunset on one.** If you keep any special
   rights during the bootstrap, write the expiry date into the bylaws. A founder
   right with no end date is the thing that makes sophisticated donors walk away.
5. **Independent board majority.** A majority of directors with no financial
   relationship to the organization and no family relationship to each other.
6. **Conflict-of-interest policy**, adopted at the first board meeting, with
   annual disclosures. Form 1023 asks about this; do it properly rather than
   pasting the sample.

### Transparency — verifiable, not promised

This is the part where the organization differentiates itself from Meta, and it
should be aggressive:

7. **Publish the cloud billing export.** Not a summary — the actual monthly
   spend by service. Anyone can check it against published rates.
8. **Publish token consumption** by model and in aggregate, and cost per member.
   Open WebUI's `/analytics` endpoints make this nearly free to produce **[code]**.
9. **Publish the resource figures.** Energy, water, and carbon attributable to
   our compute, sourced from the provider's published figures, with the
   methodology shown and its limitations stated. **Where we are guessing, say
   we are guessing.** The credibility comes from the caveats as much as the
   numbers — Meta's failure was confident claims, not uncertain ones.
10. **Publish Form 990** on the website the day it is filed, not just when
    someone requests it.
11. **Open-source everything we write** — this repo, the site, the ledger, the
    filter. "You can read our code" is a claim almost no AI provider can make.
12. **Automate the reports.** A transparency report that depends on someone
    remembering to write it will lapse in month eight. Generate and publish it
    on a schedule; a stale report is worse than none.

### Commitments to users — technical, not aspirational

13. **No training on user conversations.** Enforceable by contract with the
    inference provider — verify the enterprise/API terms actually say this — and
    documented in the privacy policy. Name the provider and link the terms.
14. **Stated data retention**, with actual deletion, and a user-facing delete
    that works.
15. **A stated escalation path** when we fall short: what gets published, by
    when, by whom. Write the failure procedure before you fail. Meta's council
    member had no recourse defined; define ours.

## Handing over what you already own

The specific transition you asked about — "a website I set up" to a real
organization — is mostly about **assets and authority**.

**Assets.** On the day the corporation exists, execute a written assignment
transferring to it: the domain, this repository and the code in it, the
trademark/name, the social accounts, and any hardware. Until you do, the
nonprofit is running on a founder's personal property and can be switched off
by one person — which is exactly the vulnerability the organization exists to
argue against. Anything you continue to provide personally (hosting, hardware,
your labor) should be a written donation or a written agreement, valued and
disclosed.

**Authority.** Recruit the other two directors *before* you need them, and
recruit people who will disagree with you. A founder-plus-two-friends board is
legally sufficient and reputationally worthless. For this organization
specifically, the board is the product: people are being asked to trust it
*because of who sits on it.* Strong candidates would be an El Paso community
member with standing on the water/energy issue, someone with nonprofit finance
experience, and someone with no technology background at all who will ask the
questions a normal donor would ask.

**Money.** Separate bank account from day one. No personal reimbursements
without receipts and board-approved policy. Never pay an organization expense
from a personal card after Stage 2.

## The uncomfortable thing to decide early

The organization is called a **data center** and, per doc 03, will not own a
data center — self-hosted GPUs are worse on cost *and* quality until thousands
of members. For the foreseeable future this is a nonprofit that buys API access
from the same hyperscalers the community is angry at, and resells it under local
governance.

That is a defensible and genuinely valuable thing to be. It is **not** what the
name promises, and someone hostile will point that out in a public meeting. Two
options, and picking one now is much easier than picking one under questioning:

- **Change the framing.** "El Paso Community AI," a nonprofit AI provider under
  local governance, with a stated long-term goal of local compute. Honest about
  what it is today.
- **Keep the name and define the path.** Publish an explicit milestone — "at
  N members / $X revenue, we deploy our own hardware in El Paso, and here is
  the water and power budget for it." Then report against it every year,
  including the years you miss.

The second is braver and much more on-message, and it only works if you actually
report the misses. The whole thesis is that this organization does what it said
it would do. That has to include the parts that are inconvenient.
