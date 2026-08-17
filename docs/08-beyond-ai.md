# Why AI is the wedge and not the point

The thesis that turns this from "a nonprofit chatbot" into something that
deserves the phrase *data center*.

## The argument

Self-hosting is a mature movement with millions of participants. Nextcloud
instead of Google Drive, Matrix instead of Discord, Mastodon instead of X,
Jellyfin instead of Netflix, Immich instead of Google Photos. The software
works, the guides exist, the communities are large.

**And pooling money for a shared server was never worth the trouble.** Every one
of those services runs fine on a €5 VPS or a retired desktop. The savings from
splitting a server are small; the cost of *organizing* — deciding who
administers it, who pays, who is accountable when it breaks, what happens when
the person holding the root password loses interest — is large and mostly fixed.
Small savings against a large fixed coordination cost is why community hosting
stayed niche while individual self-hosting grew.

**Serious AI breaks that arithmetic.** It is the first widely-wanted
self-hosted service where the hardware is genuinely expensive and genuinely
lumpy. You cannot run a competitive model on a Raspberry Pi. A capable GPU is a
four-figure purchase or a $300–500/month rental (doc 03). For the first time the
savings from pooling are larger than the coordination cost.

**And the coordination cost is one-time.** Once the entity exists, the board
exists, the billing works, someone is on call, and members trust the operator —
the marginal cost of adding Nextcloud is a container and some disk. The
expensive thing was never the software. It was the trust and the administration,
and those amortize across every service afterward.

So: **AI is the reason it finally becomes worth organizing. It is not the
point.** The point is that El Paso ends up owning a general-purpose piece of
civic infrastructure, and the AI is what justified building it.

## Why this matters strategically

It resolves the naming problem flagged in doc 05. "Community Data Center" is
an overclaim for an org that resells Gemini API calls. It is an accurate
description of an org running AI, files, chat, photos, video, search, email, and
web hosting for a city — even while renting the metal.

It also fixes the step-11 economics. A GPU bought only for chat sits idle most
of the day. A machine carrying the community's files, backups, and chat is
utilized around the clock, which is exactly the condition under which owning
beats renting.

And it broadens the funding and volunteer base well beyond people who care about
AI — which, given how contested AI is, is worth something on its own.

## Candidate services

Not commitments. Members decide (roadmap step 09).

| Service | Replaces | Notes |
|---|---|---|
| Nextcloud | Google Drive / Docs | Files, calendar, contacts. The obvious first addition. |
| Matrix / Element | Discord, Slack | Note Discord itself is not self-hostable; Matrix is the federated equivalent |
| Mastodon | X | A local instance with real moderation |
| Immich | Google Photos | Storage-hungry; price it before promising it |
| Jitsi | Zoom | Already familiar to Open WebUI deployments |
| SearXNG | Google | We need this anyway — it is how we avoid $14/1,000 grounding charges (doc 03) |
| Email + mailing lists | Mailchimp, Google Groups | High operational burden. Deliverability is a real job. |
| Static web hosting | Squarespace | Nearly free; high value to small local nonprofits |
| Offsite backup | Backblaze, iCloud | Cheap, boring, and probably the most genuinely useful thing on this list |

Two cautions worth writing down before anyone gets excited: **email is a trap**
(deliverability, abuse handling, and blocklists make it the highest-maintenance
service here), and **storage grows without bound** unless quotas exist from day
one — the same lesson as the AI credit ledger (doc 01), for the same reason.

## Precedents

We are not inventing this.

- **May First Movement Technology** — a US nonprofit membership cooperative.
  Members pay dues, the organization collectively owns the equipment, and
  membership includes email and Nextcloud accounts, with higher tiers priced on
  benefits and income. Structurally this is *almost exactly* the organization
  described in doc 05, already operating. Worth studying their bylaws, and
  worth contacting at roadmap step 12.

  **They are binational, and that is the most valuable thing about them to us.**
  Their own words: "a democratically run non-profit binational cooperative of
  movement organizations and activists" [web, mayfirst.coop/en/about,
  2026-08-17]. Doc 11's open question is how a US nonprofit serves members in
  Juárez without tripping over foreign-activity rules; they appear to have
  answered it in practice already. That is worth an email before it is worth a
  citation — ask how membership, dues and governance actually work across the
  border, and what their counsel told them.

  **Not cited on the public page, deliberately.** Their framing is explicit:
  "Digital infrastructure for liberation. Member-run, movement-rooted." That is
  a fine thing to be and it is not what this organization is claiming to be. A
  reader who follows the link swaps the frame we built — a utility that
  publishes its numbers — for a different one, and then the water figures stop
  being the point. The homepage leads with rural electric cooperatives and
  credit unions instead: member-governed, Texan, and boring in exactly the way
  that earns trust from a reader who has not decided yet.
- **CHATONS** — a collective founded by Framasoft in 2016 out of its
  "De-google-ify Internet" campaign, now 70+ small ethical, transparent hosts
  offering Nextcloud, Mastodon and similar. The model for step 12: a federation
  of small hosts rather than one large one. Unrelated to May First: one is a
  single organization with members, the other is a charter plus a directory of
  independent hosts, in different countries with no formal link. Citing both is
  citing two examples, not one movement.

  **The charter is the part to steal.** Theirs commits signatories to
  transparency, no advertising, no data mining, and no lock-in — which is the
  same ground GOVERNED.md covers, already argued over by seventy hosts. Read it
  before drafting ours rather than after. Also not cited on the public page,
  though the risk is much lower than May First's: anti-GAFAM is a critique of
  practices rather than a US partisan position, and essentially no El Paso
  reader arrives with priors about a French hosting collective.
- **Framasoft** itself — roughly 90% donation-funded, which is a useful data
  point for whether the funding model here is realistic.
- **Rural electric cooperatives** — the closest local ancestor and the best
  rhetorical frame for an El Paso audience. Formed because incumbent utilities
  would not serve people the market found inconvenient. Member-owned,
  member-governed, and still operating a century later.

The pitch is not "nobody has done this." It is "this is a well-established
model, and El Paso should have one, in the middle of an argument about who gets
to build data centers here."
