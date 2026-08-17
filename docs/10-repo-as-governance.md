# The repository as a governance mechanism

> **Proposed, not in force.** No entity, no directors, no keys. This documents a
> design so the bylaws can be drafted against something concrete.

The operative rules are in [`GOVERNED.md`](../GOVERNED.md). This explains why
they are shaped that way, and — more usefully — where the idea breaks.

## The idea

The organization's promises are mostly *technical*: we don't train on your
conversations, we keep data for N days, we buy from these providers, the free
tier stays free. Those promises are not implemented in a board minute. They are
implemented in configuration and code, in this repository.

So put the approval requirement where the change actually happens. Changing the
retention policy requires verified signatures from a supermajority of directors,
enforced at merge and visible forever in the history.

This gives the organization something almost no AI provider has: **a promise
whose enforcement anyone can verify without trusting us.** Not a policy page
that can be quietly edited, but a signed, timestamped, append-only record of who
authorized what.

## Why signatures, not permissions

The instinct is "lock the branch." The stronger version is "require signatures,"
because of what survives.

Branch protection is a row in a database at a company in San Francisco. It
proves nothing after the fact — it is a *current* setting, not a *historical*
record, and it evaporates the moment an administrator changes it or the account
is deleted.

A signature is a fact about a specific commit, checkable forever, offline, by
anyone:

```bash
git log --show-signature -- governance/
```

That command doesn't ask GitHub's permission. It works from the GitLab mirror we
already maintain, from a tarball, or from a clone a critic made years ago. The
platform stops being the source of authority and becomes a convenient place that
happens to enforce a policy.

For an organization whose entire argument is *reduce dependence on a handful of
large companies*, having its constitution enforced solely by one of them would
be an embarrassing look. Signatures fix that. And because we already mirror
GitLab → GitHub (doc 09), the proof exists in two places under different
control.

## Why not require every director

Because unanimity is an outage waiting to happen.

Requiring all N directors means **any single one can halt the organization** —
by taking a holiday, losing a laptop, being unreachable during a family
emergency, or resigning angry and declining to sign on the way out. Every
practical multi-signature scheme is M-of-N for exactly this reason.

`GOVERNED.md` proposes **two-thirds of seated directors, rounded up** for
constitutional changes. High enough that no faction moves alone; low enough that
one absent person cannot freeze the commitments.

This is also the failure mode to watch for in an organization founded on
distrust: it is tempting to make the safeguards maximally strict, and strictness
past a certain point converts a safeguard into a deadlock. A rule that cannot be
satisfied is not a strong rule.

## Why tiers, and why they mirror the bylaws

`GOVERNED.md` splits paths into constitutional / operational / routine. This is
not organizational neatness — it is a **deliberate mirror of the tiered
amendment thresholds** already recommended for the bylaws in doc 05.

| Bylaws (doc 05) | Repository (`GOVERNED.md`) |
|---|---|
| Supermajority of membership to amend the purpose clause and data commitments | Tier 1: ⅔ of directors, signed |
| Ordinary board action | Tier 2: two approvals |
| Staff discretion | Tier 3: one approval |

When those two line up, the repository becomes an **executable copy of the
governing documents** for the subset of decisions that are expressible as files.
A change that would require a membership supermajority in the bylaws requires a
director supermajority at merge. The bylaws and the branch protection say the
same thing, and one of them is machine-checked.

Where they *disagree*, that is a bug worth catching — and it is much easier to
notice in a table than in twelve pages of prose.

## Where this breaks

Four honest limits. All four belong in the pitch, not in a footnote, because an
organization arguing for verifiability should be first to publish the holes in
its own verification.

### 1. The organization-owner trapdoor

Whoever holds owner rights on the hosting organization can rewrite the rules —
lower a threshold, remove a required reviewer, transfer the repository. **No
current platform offers multi-signature control over organization settings.**
Merges can be gated; the gate's configuration cannot.

Mitigations, in descending order of usefulness:

- The bylaw citation, which makes an unvoted change a **breach** rather than an
  administrative act with no remedy
- History: past signed commits stay valid whatever happens to the settings, so
  the trapdoor allows future bypass, not retroactive forgery
- Multiple owners, so no one person holds it alone
- The audit log, so the change is at least visible

### 2. It is worthless without the bylaws

Branch protection is not a bylaw. Absent a citation, this is a convention that
lasts exactly until it is inconvenient, and nobody has standing to object when
it is dropped. **The mechanism's teeth come from the legal document, not from
the tooling.** Get the citation drafted with everything else (doc 05, step 04).

### 3. It governs a narrow slice

Git handles technical commitments well and money, contracts, employment, and
elections badly. A repository cannot hold a board meeting. The corporate record
remains the ultimate authority, and `GOVERNED.md` says so explicitly — including
for the case where enough keys are lost that the mechanism itself deadlocks.

The risk is being seduced by the elegance into governing *more* through the repo
than belongs there. Resist it.

### 4. Signing is a real barrier

Directors recruited for community standing rather than technical skill will not
arrive with GPG keys, and "set up commit signing" is a genuine obstacle for a
retired teacher who agreed to serve on a board. Two consequences worth accepting
in advance:

- Someone has to **actually onboard each director** — a real task with a real
  time cost, not a line in a README.
- If signing proves too hard for the people you most want on the board, **the
  right answer is to weaken the mechanism, not the board.** A cryptographically
  perfect process governed by only the technically confident is worse than a
  looser one governed by the community.

## Sequencing

Nothing here is urgent, and none of it should delay anything in doc 07.

1. **Now:** claim the organization name on GitHub. Free, reversible, and names
   are first-come. Nothing else changes; the repository can stay where it is
   (doc 09).
2. **Now:** create the Google Cloud billing account under the entity from the
   start. This is the one interim shortcut that genuinely hurts later —
   migrating billing and project ownership is painful, and Google for Nonprofits
   credits attach to the organization, not to a person (doc 03).
3. **At roadmap step 04**, when the bylaws are drafted: include the citation.
   This is the step that matters. Everything else is configuration.
4. **At roadmap step 08**, when directors are seated by election: populate
   `governance/keys/`, enable the rulesets, and move the repository to the
   organization.

The order is deliberate. **The mechanism should be turned on when there is a
real board to hold the keys**, not before — a threshold satisfied entirely by
the founder's own signature is theatre, and worse than having no mechanism at
all, because it looks like a safeguard.
