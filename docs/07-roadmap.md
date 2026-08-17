# Roadmap

The public version of this is on the [site](../site/index.html). This is the
working version, with the detail a volunteer would need to actually do a step.

Steps are ordered but not all sequential — 01/02 run in parallel, and 10 never
finishes. Nothing here has a date attached on purpose: publishing dates we
cannot control is the failure mode this organization was founded to be the
opposite of. What *is* committed is the **order**, and the first-election
deadline written into the bylaws at step 04.

---

## Act I — Exist

### 01 · Find out if anyone wants this
**Status: now.** Mailing list via the signup form. The gate: if the list stays
short, say so publicly and stop. An organization premised on honesty should be
willing to publish its own negative result.

Also the cheapest possible de-risking — every later step costs money or somebody
else's time.

### 02 · Recruit three founding directors
**Status: now. Gates everything in Act II.**

TBOC § 22.204 requires at least three directors, plus a president and secretary
(§ 22.231) (doc 05). Recruit for disagreement, not agreement — the useful
profile is someone with standing on the local water/energy fight, someone with
nonprofit finance experience, and someone with no technology background who will
ask what a normal donor would ask.

Takes longer than any of the software. Start before you think you need to.

### 03 · File the certificate of formation
Texas SOS **Form 202**, $25 (doc 05). Encodes the purpose clause, whether there
are voting members, and the dissolution clause.

**Elect to have members at formation.** Retrofitting voting membership later
means amending the certificate at exactly the moment founder authority is
hardest to give up.

### 04 · Adopt bylaws that bind us
The step that actually matters, and the one worth paying a Texas nonprofit
attorney for (doc 05). Minimum contents:

- Supermajority of the **membership** to amend the purpose clause or the data
  commitments
- **A date certain for the first member election** — the most credible act
  available to a founder, because you are binding yourself at the only moment
  you have the power to
- Staggered terms, term limits, petition path onto the ballot, member removal
- Quorum and proxy rules that consciously override the TBOC defaults (§ 22.159)
- Conflict-of-interest policy
- No permanent founder seat, or an explicit expiry

---

## Act II — Serve

### 05 · Find a fiscal sponsor
Bridge to deductible donations while the 1023 is pending (doc 05, Stage 1).
Typically 5–10% of donations. Secondary benefit: someone else's back office
enforces financial discipline from day one.

### 06 · Turn the service on
Doc 04. One VM, Open WebUI, a public site, Stripe.

**The credit ledger and inlet filter are not optional and not deferrable.**
Open WebUI measures usage but will not stop anyone (doc 01). Opening public
signups without metering is how this fails in month two.

### 07 · Become tax-exempt
IRS **Form 1023 long form**, not the EZ (doc 05, Stage 3). Then, in order, as
each unlocks the next: Texas franchise and sales tax exemption → Stripe
nonprofit rate (not retroactive; apply the day the determination letter
arrives) → Google for Nonprofits cloud credits (doc 03).

### 08 · Hand over the keys
First member election. Board seated by vote. Founder's special role expires per
step 04. First annual report and Form 990 published the day they are filed.

This is the step that converts the claim into a fact. Everything before it is
a founder asking to be trusted.

---

## Act III — Grow into the name

### 09 · One machine, many services
Doc 08. The marginal cost of the second service is near zero once the machine,
the entity, the board, and the billing exist. Members vote on what to add and
in what order.

### 10 · Decide out loud what we won't do
**Never completes.** Which models we buy and from whom; retention and deletion;
whose money we accept; what we refuse to host; whether to run models with known
safety problems because they are cheaper.

These are genuinely contested and reasonable people disagree. The commitment is
procedural: **publish the deliberation, not just the verdict.** A published
disagreement is evidence the governance is real; a stream of unanimous decisions
is evidence it isn't.

### 11 · Own the hardware, in El Paso
Self-hosted GPU is worse on cost *and* quality until thousands of members
(doc 03) — but "many services" (step 09) changes the arithmetic, because the
non-AI workloads are cheap and the machine gets used around the clock.

Publish a water and power budget before buying anything, and report against it
annually **including the misses**.

### 12 · Find allies and build something better
One city's nonprofit cannot out-build a hyperscaler. A network can pool
purchasing, share operations, and make the case by demonstration rather than
demand.

Real counterparts already exist (doc 08): **May First Movement Technology** (US
nonprofit membership cooperative), the **CHATONS** collective (70+ ethical
hosts), municipal broadband projects, and — the closest local ancestor —
**rural electric cooperatives**.

The end state worth aiming at is not one community data center. It is enough of
them, coordinated, to establish what a well-built data center looks like, and
to have receipts.
