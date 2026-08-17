# GOVERNED.md — what the board controls, and how

**Status: proposed.** No entity exists, no directors are seated, and no key
registry is populated. This file is a draft for the bylaws to reference, not a
description of a mechanism currently in force. Every threshold below is a
starting proposal for counsel and the founding board to change.

---

This file enumerates the paths in this repository whose contents are
**organizational commitments rather than engineering choices**, and the approval
each tier requires.

It is intended to be **referenced by the bylaws**. On its own, branch protection
is a setting an administrator can toggle; cited in the bylaws, bypassing it
becomes a governance violation with a defined remedy. The mechanism is worth
very little without that citation.

Proposed bylaw language:

> Changes to files enumerated in `GOVERNED.md` in the Corporation's primary
> source repository require verified cryptographic signatures from the number of
> seated directors stated in that file for the applicable tier. Merging such a
> change without those signatures, or altering the enforcement configuration
> without a vote of the Board, is a breach of these Bylaws, and the Board shall
> restore the prior state and publish the circumstances within thirty days.

## Why signatures rather than a checkbox

The authority is the **signature**, not the hosting platform's access control.
A signed commit is verifiable by anyone with a clone, forever, on any host:

```bash
git log --show-signature -- governance/
git verify-commit <sha>
```

That check does not consult GitHub. It works from the GitLab mirror, from a
tarball, or from a copy a skeptic made three years ago. If the platform deletes
the account, changes its rules, or is simply not trusted by the person doing the
checking, the proof still holds. The platform is a venue that enforces a policy;
it is not the source of authority.

## Tiers

### Tier 1 — Constitutional

**Requires: verified signatures from two-thirds of seated directors, rounded up.**

Never unanimity. Requiring every director means any single one — on vacation,
with a lost key, or resigning unhappily — can halt the organization. A threshold
that can deadlock is not a safeguard, it is an outage.

| Path | Exists | What it holds |
|---|---|---|
| `GOVERNED.md` | ✅ | This file. Self-amending at its own highest tier, so the rules cannot be lowered by a lower-tier change. |
| `governance/commitments.md` | ⬜ | No training on user conversations; data retention and deletion; what we refuse to host |
| `governance/keys/` | ⬜ | Director signing-key registry (see below) |
| `governance/pricing.md` | ⬜ | Free-tier guarantee, tier prices, dues, fee-waiver policy |
| `governance/providers.md` | ⬜ | Which inference providers and models we buy, and on what contract terms |

### Tier 2 — Operational

**Requires: two approvals — two directors, or one director and one authorized
maintainer.**

| Path | Exists | What it holds |
|---|---|---|
| `deploy/` | ✅ | The service that runs in production and handles signup data |
| `site/` | ✅ | The public site, including every factual claim on it |
| `.github/workflows/` | ✅ | Anything that can publish or deploy |
| `tools/` | ✅ | The cost model the budget is argued from |

### Tier 3 — Routine

**Requires: one approval.**

Everything else, including `docs/` and `README.md`. Research and working notes
are improved by being easy to change.

## Break-glass

A security fix to a Tier 2 path may be merged by **one** director or maintainer
without waiting, provided that:

1. the commit message begins `BREAK-GLASS:` and states the specific risk,
2. it is announced to the full board the same day, and
3. it is **ratified at its normal tier within seven days, or reverted.**

There is no break-glass for Tier 1. Nothing about a data-retention promise is
ever an emergency, and "we had to move fast" is precisely the excuse this
organization exists to distrust.

## Keys

Each director registers a GPG or SSH signing key in `governance/keys/`, one file
per director, containing the public key and its fingerprint. Adding, removing,
or rotating a key is a **Tier 1** change — the key registry is the root of the
whole mechanism, so it gets the highest protection.

**Lost keys are expected, not exceptional.** A director who loses a key is
replaced in the registry by the remaining directors at the Tier 1 threshold.
This is deliberately the same process as adding a new director's key: there is
no separate recovery path with weaker rules, because a weak recovery path *is*
the attack.

If enough keys are lost simultaneously that the Tier 1 threshold cannot be met,
the mechanism has failed and the **Board's minuted vote governs** — the
corporate record, not the repository, is the ultimate authority. Reconstituting
the registry then requires publishing what happened.

## What this does not govern

Deliberately narrow. This mechanism handles **technical commitments** well and
handles everything else badly:

- ❌ Money, budgets, banking
- ❌ Contracts, employment, compensation
- ❌ Board elections, membership, dues
- ❌ Anything requiring a minuted vote

Those live in the corporate record. **A repository is not a corporation**, and
an elegant mechanism is not a reason to pretend otherwise. Git can prove that
five people signed a change to a retention policy. It cannot hold a board
meeting.

## Enforcement configuration

Enforced with GitHub repository **rulesets** — specifically the required
reviewer rule, which supports per-file granularity. Note that plain `CODEOWNERS`
is **not** sufficient: when a path lists several owners, an approval from any
*one* of them satisfies it, which is the opposite of a threshold.

Alongside it: require signed commits, require linear history, block force-push
and branch deletion, and disable administrator bypass.

**Known limit, stated plainly:** whoever holds organization-owner rights can
change these settings. There is no multi-signature control over organization
settings on any current platform. The protections are that multiple people hold
owner rights, that changes appear in the audit log, and that the bylaw citation
above makes an unvoted change a breach rather than an administrative act. This
is a real weakness and it should be disclosed rather than papered over.
