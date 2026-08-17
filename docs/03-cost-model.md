# What it costs

All prices as researched 2026-08-16. Re-verify before quoting any of this to a
donor. `tools/cost_model.py` runs these numbers.

## Headline

Hosting is not the expensive part. **Inference is.** And the single most
important financial fact in this document:

> **Google for Nonprofits provides up to $10,000/year in Google Cloud
> credits** to qualifying 501(c)(3) organizations. **[web]**

$10,000/year covers hosting *and* inference for a few hundred active members at
modest usage. The MVP can plausibly run on **$0 of cash** for its first year or
two — which changes the fundraising story from "we need money to exist" to "we
need money to grow and to prove we can pay our own way." Get the 501(c)(3), get
the credits.

⚠️ **Verify before relying on this**: confirm the credits apply to **Vertex AI**
inference and not just to compute/storage, and confirm the current annual
amount. This single question is worth an hour of someone's time; it is the
difference between a $0 and a $4,000 first-year budget.

## Part 1 — Hosting the application

Open WebUI needs: a container, a Postgres database, persistent storage for
uploaded files, and a warm process (it streams over WebSockets, so cold starts
are user-visible).

### Google Cloud — recommended shape: one VM

| Item | Spec | Monthly |
|---|---|---|
| Compute Engine `e2-standard-2` | 2 vCPU, 8 GiB | **$48.92** on-demand **[web]** |
| — same, 1-year committed use | | ~**$31** **[est]**, CUDs run ~37% **[web]** |
| Balanced persistent disk | 100 GB | ~**$10** **[est]** |
| Postgres on the same VM | | **$0** |
| Egress, DNS, misc | | ~**$5** **[est]** |
| **Total** | | **~$65/mo** on-demand, **~$46/mo** committed |

Add managed Postgres only when you want someone else responsible for backups:
Cloud SQL smallest instance (1 vCPU / 3.75 GiB) ≈ **$30/mo** **[web]** plus SSD
storage at **$0.222/GB-month** **[web]**. Call it **+$35/mo**.

### Google Cloud — Cloud Run

Tier-1 request-based rates: **$0.000024 per vCPU-second** and **$0.0000025 per
GiB-second**, with a free tier of 180,000 vCPU-s / 360,000 GiB-s / 2M requests
per month **[web]**.

A 2 vCPU / 4 GiB service pinned warm 24/7 is an upper bound of
2 × 2,592,000 × $0.000024 + 4 × 2,592,000 × $0.0000025 ≈ **$150/mo**.

Cloud Run is a poor fit here and I would not lead with it: the app is stateful
and long-lived, streaming responses hold connections open for the full
generation, and scaling to zero produces cold starts in a chat box. You pay a
premium for elasticity you cannot use. Instance-based billing is cheaper than
the request-based rates above but I could not verify the exact per-unit figure —
**[unverified]**.

### AWS equivalent

`t4g.large` (2 vCPU ARM, 8 GiB) on-demand is roughly comparable to the GCE VM;
RDS Postgres `db.t4g.micro` adds a similar increment. AWS's nonprofit credit
program is smaller than Google's. Given the preference for Google Cloud and the
$10k credit, AWS is the fallback, not the plan. **[est]**

### Frugal tier

| Option | Spec | Monthly |
|---|---|---|
| Hetzner `CPX31` | 4 vCPU, 8 GB, 160 GB NVMe | **~€25 / ~$27** **[web]** |
| Cloudflare in front | | **$0** |
| **Total** | | **~$30/mo** |

Note Hetzner repriced hard in June 2026 — CPX/CCX lines rose 113–175% **[web]** —
so the old "€8 VPS" folklore is stale. Even so it is roughly half the GCE price.

**Recommendation:** run the MVP on Google Cloud even though Hetzner is cheaper.
Not for technical reasons — because the $10k nonprofit credit dwarfs the ~$35/mo
difference, and because "our infrastructure is in Google Cloud, here is our
billing export" is an auditable transparency story in a way a German VPS is not.

## Part 2 — Inference, the actual cost driver

### Published token prices

Per 1M tokens, input / output:

| Model | Input | Output | Source |
|---|---|---|---|
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | **[docs]** |
| GPT-5-nano | $0.05 | $0.40 | **[docs]** |
| GPT-5-mini | $0.25 | $2.00 | **[docs]** |
| Gemini 2.5 Flash | $0.30 | $2.50 | **[docs]** |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | **[docs]** |
| **Gemini 3.7 Flash** | **$0.75** | **$3.75** | **[docs]** — through 2026-12-31; **doubles to $1.50/$7.50 on 2027-01-01** |
| Claude Haiku 4.5 | $1.00 | $5.00 | **[web]** |
| Gemini 2.5 Pro | $1.25 | $10.00 | **[docs]** |
| GPT-5.1 / GPT-5 | $1.25 | $10.00 | **[docs]** |
| Gemini 3.5 Flash | $1.50 | $9.00 | **[docs]** |
| Claude Sonnet 5 | $2.00 | $10.00 | **[web]** — intro rate; **$3/$15 from 2026-09-01** |
| GPT-5.4 | $2.50 | $15.00 | **[docs]** |
| Claude Opus 5 | $5.00 | $25.00 | **[web]** |

Two scheduled price increases land inside any 12-month plan you write today.
Budget on the post-increase numbers.

### Cost per member per month

Modeling assumption **[est]**: an average chat turn costs **6,000 input tokens**
(system prompt + retrieved context + accumulated conversation history) and
**700 output tokens**. Input dominates because history is resent every turn.

At **150 turns/member/month** (~5/day, a genuinely engaged user):

| Model | $/turn | $/member/mo | 200 members | 1,000 members |
|---|---|---|---|---|
| Gemini 2.5 Flash-Lite | $0.0009 | **$0.13** | $26 | $132 |
| GPT-5-mini | $0.0029 | **$0.44** | $87 | $435 |
| Gemini 2.5 Flash | $0.0036 | **$0.53** | $107 | $533 |
| Gemini 3.7 Flash | $0.0071 | **$1.07** | $214 | $1,069 |
| Claude Haiku 4.5 | $0.0095 | **$1.43** | $285 | $1,425 |
| Gemini 2.5 Pro | $0.0145 | **$2.18** | $435 | $2,175 |
| Claude Sonnet 5 (post-Sep) | $0.0285 | **$4.28** | $855 | $4,275 |

**A ChatGPT-competitive service costs on the order of $1–2 per active member per
month in tokens.** ChatGPT Plus is $20/month. The gap is not compute — it is
brand, apps, and the fact that OpenAI is subsidizing.

### The three levers that actually matter

1. **Context caching — the biggest one.** Input is ~85% of the token cost above,
   and most of it is conversation history resent unchanged every turn. Gemini
   context caching drops input from $0.75/M to **$0.075/M** **[docs]**; Anthropic
   cache hits cost 10% of standard input **[web]**. Getting this right plausibly
   cuts total inference cost **50–70%**. Do this before optimizing anything else.
2. **Model routing.** Default everyone to Flash-Lite or Flash. Reserve Pro/Opus
   for members who ask for it and count against their allocation at a higher
   rate. Open WebUI's group-based per-model access control (doc 01) implements
   the gate with zero code.
3. **Batch API.** 50% off both directions on OpenAI and Anthropic **[web]** for
   anything not interactive. Irrelevant for chat, useful for any background
   summarization or moderation the org runs.

### Watch out: web search grounding is expensive

Gemini search grounding is 5,000 free requests/month, then **$14 per 1,000
requests** **[docs]** — i.e. **$0.014 per search**, roughly **2× the cost of an
entire Flash chat turn**. Gemini 2.5 Flash grounding is worse: $35/1,000 after
1,500/day free **[docs]**.

Open WebUI supports **SearXNG** as a search backend **[code]**, which you
self-host for the cost of the CPU it uses. Use that. This one configuration
choice can be worth more than the entire hosting bill.

## Part 3 — Running your own GPUs

The name says "Data Center." The economics say: not yet. This deserves to be
stated plainly because it is the biggest tension in the concept.

| Option | Cost |
|---|---|
| GCP `g2-standard-4` (1× NVIDIA L4, 24 GB) on-demand | **$0.7068/hr ≈ $516/mo** **[web]** |
| Same, Spot | **$0.4171/hr ≈ $304/mo** **[web]** |

$516/month of Gemini 3.7 Flash buys roughly **72,000 chat turns** — about
**480 members** at 150 turns each. A single L4 running a 4-bit ~30B model cannot
serve 480 members, and the model it *can* serve is not competitive with
Gemini Flash on quality.

**Self-hosted inference is worse on cost and worse on quality until you are
serving thousands of active members.** Anyone who tells the board otherwise is
selling something.

This does not kill the concept — it sequences it. See doc 05 for how to hold the
mission honestly in the meantime.

## Part 4 — Money in

Stripe's **discounted 501(c)(3) rate is 2.2% + $0.30** per charge, versus the
standard 2.9% + $0.30 **[web]**. Requires an EIN or IRS determination letter,
applies to *donations* only (not ticket or merchandise sales), and you must be
processing 80%+ of donation payments through Stripe. Apply to
`nonprofit@stripe.com`; review is weekly and takes 5–10 business days, and it is
**not retroactive** **[web]**. Apply the day the determination letter arrives.

Fee impact is a real design constraint on small donations:

| Donation | Fee @ 2.2% + $0.30 | Effective rate |
|---|---|---|
| $5 | $0.41 | 8.2% |
| $10 | $0.52 | 5.2% |
| $25 | $0.85 | 3.4% |
| $50 (annual dues) | $1.40 | 2.8% |
| $120 (annual dues) | $2.94 | 2.5% |

Prefer **annual** dues over monthly: twelve $5 charges cost $4.92 in fees; one
$60 charge costs $1.62.

## Part 5 — Putting it together

**Year 1, 200 members, Gemini 3.7 Flash default, self-hosted SearXNG:**

| Line | Monthly | Annual |
|---|---|---|
| GCE VM + disk + egress | $65 | $780 |
| Inference (200 × $1.07) | $214 | $2,565 |
| Domain, email, misc | $15 | $180 |
| **Subtotal** | **$294** | **$3,525** |
| Google for Nonprofits credit **[web]** | | **−$3,525** (ceiling $10,000) |
| **Net cash cost** | | **$0** |

The $10,000 credit covers this configuration up to roughly **700 members** at
150 turns/month before any cash is required. Run
`python3 tools/cost_model.py --members 700` to see the edge.

Plus one-time formation costs: Texas Form 202 filing **$25** **[web]**, IRS Form
1023-EZ user fee **$275** **[web]** (see doc 05 on whether EZ is appropriate),
and legal review — budget **$1,500–5,000** for a Texas nonprofit attorney to do
the bylaws properly **[est]**. The legal spend is the real year-one number, and
it is the one worth paying for.

**The organization's first year is cheap. Its credibility is the expensive
part.**
