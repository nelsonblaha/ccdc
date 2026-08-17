# From "a website I set up" to a nonprofit people can trust

> **Not legal advice.** I am not a lawyer. Everything below is research to make
> you a well-prepared client, not a substitute for a Texas nonprofit attorney.
> The one line item in this whole project genuinely worth paying cash for is
> counsel on the bylaws and the exemption application.

## The decision that shapes everything else

You wrote: *"I'd imagine voting members pay flat dues and get a flat share of
the AI output."*

### First, clear away two things that are *not* the problem

**Charging money is not the problem.** A 501(c)(3) may absolutely sell services.
Hospitals, universities, community health clinics, YMCAs, and NPR member
stations all charge. Fee income that is **substantially related** to the exempt
purpose is not even subject to unrelated business income tax **[web]**. The test
has two routes: services are substantially related if they are **provided
substantially below cost** *or* **further the exempt purpose** **[web]**.

**Reinvesting surplus is not the problem either.** The prohibition is on
*inurement* — value flowing to insiders (directors, officers, founders, their
families). There are no owners to distribute to, so "profits are only
reinvested" is not a concession you make to qualify; it is simply what a
nonprofit is. Nonprofits are allowed to run surpluses and accumulate reserves.

And a third: **you do not have to check driver's licenses.** A charitable class
may consist of "all individuals located in a city, county, or state" **[web]**;
the requirement is that the class be large or indefinite enough that the
community rather than a pre-selected group benefits **[web]**. El Paso County is
~865,000 people — plainly large and indefinite. Self-attestation or a ZIP code
field is fine, and heavy identity verification would actually work *against* you
by narrowing the class and adding a barrier to the very access you claim to
provide.

### What the problem actually is

Two distinct doctrines, and it is worth keeping them separate:

**1. Private benefit — the *closed loop* is the problem, not the payment.**
501(c)(3) requires the organization serve "a public rather than a private
interest" **[web]**; benefits to private individuals must be incidental both
qualitatively (a byproduct of the public benefit) and quantitatively
(insubstantial) **[web]**. A **mutual-benefit corporation cannot obtain
501(c)(3) status** **[web]**, and in *Korean-American Senior Mutual Association
Inc. v. Commissioner* the IRS moved to revoke exemption where members paid dues
and received member benefits in return **[web]**.

What triggers this is not "money came in." It is **dues in → compute out,
members only, in proportion to what you paid.** That is a buyers' club: the
class of beneficiaries is exactly the class of payers. The fix is not to stop
charging. The fix is to **open the beneficiary class beyond the payers.**

**2. Commerciality — do you look like a business?** This is the doctrine that
actually bites organizations doing what we are doing, and it is about the
aggregate picture rather than any single fact. *Living Faith, Inc. v.
Commissioner*, 950 F.2d 365 (7th Cir. 1991) denied exemption to a health food
store because it sold goods and services to the public and was in direct
competition with for-profit businesses **[web]**. Courts weigh pricing policy
and the extent of below-cost service, competition with commercial firms,
commercial marketing, and the presence or absence of donations and volunteer
labor. A nonexempt purpose "somewhat beyond a de minimis level" is tolerated;
it simply cannot be **substantial** **[web]**.

Selling AI chat subscriptions at $20/month against ChatGPT is close to the
center of this doctrine. Selling access at a fraction of cost, subsidized by
donations, on a sliding scale, to people who cannot buy the commercial product,
is nowhere near it. **The distance between those two is a pricing policy, and
it is yours to set.**

**So: charge. Just don't price like a vendor, and don't close the loop.**

### Three ways to structure it

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

A concrete ladder that fits inside this, all of it open to any resident of the
metro rather than to members only. **Three tiers, and the paid band is stated as
a range on purpose** — the board should set the numbers, and a page that commits
to $15 invites an argument about $15 instead of about the structure:

| Tier | Price | Why it is defensible |
|---|---|---|
| Free | **$0** | Real, usable, and used. This is the charitable program, not a demo. |
| Member | **flat annual dues**, waived on request | Buys **governance**, not compute |
| Supporter | **$5–50/mo** | Priced under the $20 commercial equivalent rather than against it; the top of the band cross-subsidizes the free tier |

Note the ordering matters to the argument: Free first because it is the point,
Member second because governance is what dues buy, Supporter last because paying
more is how you fund somebody else's access — not how you buy more say.

Every paid tier is priced below the commercial alternative and the surplus
visibly funds free access. That is the opposite of the *Living Faith* fact
pattern, and it is a story you can tell in one sentence at a city council
meeting.

**Option B — Charge market rate to organizations, and accept (or isolate) the
tax.** Selling AI seats to local businesses at commercial rates is probably
*not* substantially related to a digital-equity purpose. That does **not**
disqualify you. It means that slice is unrelated business income: report on
Form 990-T and pay corporate tax on it **[web]**. Exemption is only threatened
if the unrelated activity becomes **substantial** relative to everything else
**[web]**.

If that revenue grows into something real, the standard move is a **taxable
subsidiary** — a for-profit LLC or corporation wholly owned by the nonprofit,
selling at market rate, with profits flowing up to the parent. This is roughly
the Mozilla structure. It keeps the commercial activity out of the exemption
analysis entirely and gives the board a clean place to put "we sell AI to
businesses to fund free AI for everyone else."

**Do not build this in year one.** Note it as the answer to "how do we make real
money and reinvest it," which is a legitimate thing to want and a solved
problem.

**Option C — Give up 501(c)(3) and be a cooperative honestly.** If the whole
point is members-only compute proportional to dues, structure as a co-op or a
501(c)(6)/(c)(4) and stop pretending. Cost: contributions are **not** charitable
deductions, you lose Google for Nonprofits' $10,000 in cloud credits (doc 03),
and you lose most grant funding. Pick this only if the closed member benefit is
genuinely the point.

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
first annual report and Form 990. Mechanics below.

## Membership and how the board actually gets elected

### Separate the two products

The cleanest structure, and the one that resolves the private-benefit problem
by construction:

| | **Subscription** | **Voting membership** |
|---|---|---|
| What it buys | AI access | governance: vote for directors, attend the annual meeting, inspect the books |
| Who is eligible | anyone (El Paso focus) | El Paso County residents, self-attested |
| Price | $0 / ~$5 / ~$15 per month | flat annual dues, ~$25–50 |
| Required to have the other? | **No** | **No** |

A subscriber need not be a member. A member need not subscribe. **Dues buy a
vote, not compute** — which is what keeps this out of buyers'-club territory
while still letting members fund the organization.

Two refinements worth building in:

- **Waive dues on request, no questions asked.** If governance is gated by $30,
  the organization is governed by people who have $30. A published, frictionless
  waiver costs almost nothing and is a strong answer to the obvious criticism.
- **Dues that buy only voting rights are largely deductible.** Intangible
  governance privileges have minimal fair market value. The moment membership
  also conveys compute, you must subtract its FMV and — for payments over $75
  where the member receives goods or services — make a written quid-pro-quo
  disclosure. Keeping compute out of the membership bundle keeps the accounting
  simple and the deduction clean.

### The bootstrap: the first board is appointed, not elected

There is no way around this and it is not a compromise — every membership
nonprofit starts here. As incorporator you name the initial directors (minimum
three, TBOC § 22.204) on **Form 202** and at the organizational meeting. They
adopt the bylaws. Elections begin once there are members to hold them.

What matters is that the bylaws **commit to the handover on a date certain**,
adopted while you still control the process. Writing "the first member election
shall be held no later than [18 months after formation]" into the founding
bylaws is the single most credible governance act available to you, because you
are binding yourself at the only moment you have the power to.

### Texas defaults you must consciously override

TBOC supplies defaults that mostly do not fit. Bylaws control; silence is a
decision.

- **Quorum defaults to one-tenth** of votes entitled to be cast, in person or by
  proxy (§ 22.159) **[web]**. For a 500-member org that is 50 people — probably
  achievable. For 5,000 it is not, and a failed quorum means the organization
  cannot act. Set it deliberately, and allow electronic ballots so "attendance"
  is not a room in El Paso on a Tuesday.
- **Proxies are permitted by default** (§ 22.159) **[web]**. Proxy solicitation
  is *the* classic capture vector for member organizations. Either bar proxies
  and use direct electronic balloting, or cap how many proxies one person may
  hold.
- **One member, one vote regardless of class** is the default (§ 22.160)
  **[web]**. Keep it. Resist any structure where larger donors get more votes;
  it is the fastest possible way to lose the plot.
- **Majority of votes cast at a quorate meeting carries** (§ 22.159) **[web]** —
  except where you have deliberately required a supermajority (the mission lock,
  below).

### Anti-capture provisions

Cheap dues plus online signup means a motivated group — a competitor, a
political faction, or one annoyed person with 40 friends — can take the board in
a single cycle. Standard, unglamorous protections:

1. **One natural person, one membership, dues paid by that person.** No bulk or
   gifted memberships with voting rights. No organizational memberships that
   vote.
2. **A waiting period.** Membership must be established some fixed period (60–90
   days) before the record date to vote in that election. This alone defeats
   most signup surges.
3. **Staggered terms.** Three classes, three-year terms, roughly one-third
   elected annually. A hostile majority then needs to win two consecutive
   elections rather than one, which is the whole point — it converts a raid into
   a campaign.
4. **Term limits** for directors, so the board renews without depending on
   anyone losing an election.
5. **A petition path onto the ballot.** A nominating committee that controls the
   entire slate makes elections decorative. Any member should reach the ballot
   by petition of a small number of members (say 10, or 2% of membership,
   whichever is less). This is the valve that makes member voting real, and it
   is the provision a self-interested founder would quietly omit.
6. **Members may remove directors**, with a defined vote threshold. The board
   fills interim vacancies until the next annual election.

### Board composition

Five to seven directors is the right size — large enough for real independent
committees (audit, compensation), small enough to function.

- **Member-elected majority.** This is what makes the governance claim true.
- At most a minority of appointed or at-large seats, for specific expertise you
  cannot count on an election to produce — a treasurer with nonprofit finance
  experience, someone with standing on the local water and energy fight.
- **No permanent founder seat**, or if there is one during the bootstrap, an
  explicit expiry written into the bylaws.
- The supermajority mission lock (below) should require a vote of the
  **membership**, not just the board — a board can be captured; a membership is
  much harder to capture quietly.

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

## Can the founder be paid?

**Yes.** Paying a founder to run the organization is ordinary and legal — most
501(c)(3) executive directors are compensated, and many are founders. The rule
is not "no salary." The rule is **reasonable compensation for services actually
rendered**, and the prohibition on *inurement* is about insiders extracting
value beyond what their work is worth.

But this is the single most attackable fact about the organization, so it is
worth doing to a standard well above the legal minimum.

### The safe harbor, and how to actually get it

There is a defined procedure — the **rebuttable presumption of
reasonableness**. Satisfy all three prongs and the compensation is presumed
reasonable, shifting the burden of proof to the IRS **[web]**:

1. **Approved in advance** by an authorized body composed of individuals with
   **no conflict of interest** as to the transaction **[web]**
2. The body **obtained and relied on appropriate comparability data** before
   deciding **[web]**
3. The body **adequately and contemporaneously documented** the basis for its
   determination **[web]**

Practically, for us:

- **Recuse completely.** You are not in the room, not in the vote, and not in
  the minutes except as the subject. If you are also the treasurer or secretary,
  that is worse — separate the roles.
- **Comparability data means real data**, not a feeling. Pull Form 990
  compensation for El Paso and comparable-budget Texas nonprofits from public
  990 filings. Compare against organizations with *our* budget, not our
  ambitions. An organization with a $60k budget cannot pay a $120k salary and
  call it comparable to anything.
- **Write the minutes the same day**, with the data attached.

### What happens if you get it wrong

Excess compensation is an **excess benefit transaction** under IRC § 4958:
a **25% excise tax on the disqualified person** who received it, rising to
**200%** if it is not corrected within the taxable period, plus **10% on
organization managers** who knowingly approved it (capped — commonly cited at
$20,000 per transaction, though sources vary) **[web]**.

Note who pays: **you**, personally, not the organization. And the board members
who approved it. This is precisely why you want the independent-approval
procedure — it protects your directors, which is also what makes good directors
willing to serve.

### The real problem is not legal, it is structural

The legal test assumes an **authorized body without a conflict of interest**.
If you founded the organization, recruited all three directors, and they are
your friends, that body is independent on paper and not in fact. The IRS may
never look. A journalist, a rival, or a skeptical council member absolutely
will — and "the founder's hand-picked board approved the founder's salary" is a
one-line story that ends the trust thesis this organization is built on.

Defensible looks like:

- **A compensation committee of directors you did not recruit**, or at minimum a
  majority-independent board (doc 05, "Structural") that includes someone with
  no prior relationship to you.
- **Publish the salary and the comparability data voluntarily**, before anyone
  asks. Form 990 Part VII makes it public anyway; publishing it first is free
  and converts a liability into evidence.
- **Fixed salary, no revenue share.** Never tie your pay to donations raised or
  members signed up. Revenue-based compensation for insiders is the shape
  regulators look for.
- **Target at or below the median** of the comparability set. You will be
  arguing that this organization exists to serve people who cannot afford $20/mo
  for ChatGPT; a top-quartile salary undermines that in a way no amount of
  compliance fixes.

### Sequencing

Realistically the question is moot for a while: at a $3.5k/year budget
(doc 03) there is nothing to pay anyone. The honest ladder is **volunteer →
documented reimbursement of actual expenses → a modest contract or stipend for
defined work → part-time employment → full-time**, each step approved by
independent directors with data on the record.

One more note: **founder-as-employee and founder-as-director are separable.**
Being the paid administrator does not require being on the board, and stepping
off the board while being employed by it is a *stronger* governance position,
not a weaker one — it makes the board your supervisor rather than your
committee. Worth considering once there are directors you trust.

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
