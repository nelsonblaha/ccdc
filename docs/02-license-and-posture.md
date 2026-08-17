# Is this allowed? License, branding, and how Open WebUI is likely to react

## Short answer

**Yes, unambiguously allowed.** Nothing in the license restricts commercial use,
public use, hosted/SaaS use, charging money, or nonprofit use. There is exactly
one restriction, and it is about the *name on the screen*, not what you do with
the software.

The one thing you cannot do for free: **rebrand it as "El Paso Community AI"**
once you have more than 50 users.

## What the license actually says

Open WebUI relicensed at **v0.6.6 (2025-04-19)** from MIT to a custom
BSD-3-Clause variant **[web]**. Reading the current `LICENSE` file in full
**[code]**, it is standard BSD-3-Clause with one added clause:

> 4. Notwithstanding any other provision of this License, and as a material
> condition of the rights granted herein, licensees are strictly prohibited
> from altering, removing, obscuring, or replacing any "Open WebUI" branding,
> including but not limited to the name, logo, or any visual, textual, or
> symbolic identifiers that distinguish the software and its interfaces, in any
> deployment or distribution, except in the following circumstances: (i)
> deployments or distributions where the total number of end users (defined as
> individual natural persons with direct access to the application) does not
> exceed fifty (50) within any rolling thirty (30) day period; (ii) the
> licensee has obtained specific prior written permission from the copyright
> holder; or (iii) where the licensee has obtained a duly executed enterprise
> license expressly permitting such modification.

That is the *entire* added restriction. Note what is **absent**:

- ❌ No field-of-use restriction
- ❌ No non-commercial clause
- ❌ No SaaS / hosting / "offering as a service" restriction (this is not AGPL,
  and not the Elastic/SSPL style of source-available license)
- ❌ No revenue threshold
- ❌ No restriction on charging your users

Running a paid, public, multi-tenant Open WebUI service for El Paso is squarely
within the grant. You are doing exactly what BSD permits.

`LICENSE_HISTORY` **[code]** further confirms code before commit `a76068d6…` is
MIT and before `60d84a3a…` is plain BSD-3 — so the pre-relicense codebase stays
permissively licensed regardless.

## The branding gate is enforced in code, not just in prose

This is the practical detail that determines your options.
`backend/open_webui/env.py:891` **[code]**:

```python
WEBUI_NAME = os.getenv('WEBUI_NAME', 'Open WebUI')
if WEBUI_NAME != 'Open WebUI':
    WEBUI_NAME += ' (Open WebUI)'
```

Set `WEBUI_NAME="El Paso Community AI"` and the application displays
**"El Paso Community AI (Open WebUI)"**. The suffix is appended
unconditionally. The favicon is likewise hardcoded to
`https://openwebui.com/favicon.png` **[code]**.

The unlock is `LICENSE_KEY` **[code]** (`env.py:866`). At startup
(`main.py:345`) it POSTs your key to `https://api.openwebui.com/api/v1/license/`
and the response payload can set `app.state.WEBUI_NAME` directly — bypassing the
suffix — plus `count` (a seat count) and `resources` (static asset overrides,
i.e. logos). **[code]** `utils/auth.py:85`.

So: white-labeling is a paid, server-validated feature. Patching the two lines
out is trivially easy and is a **material breach of license** above 50 users.
Don't. For an organization whose entire pitch is "we keep our commitments," a
license violation in the founding stack is a fatal look — and it is the first
thing a hostile El Paso journalist or a Meta PR shop would find.

## What this means for the three viable paths

### Path A — Ship with the suffix (recommended for MVP)

Display "El Paso Community AI (Open WebUI)" and put the explanation on the
public site: *"Our chat interface is built on Open WebUI, an open-source
project. We credit them because their license asks us to and because we think
you should know what we're running."*

Cost: $0. Risk: none. And it is arguably *on-message* — an organization
premised on transparency disclosing its stack is a feature, not a wart. It also
lets you honestly say "you can audit every line of what we run."

### Path B — Buy an enterprise license

The enterprise page offers white-labeling, rebranding, and enterprise-exclusive
offerings (Terminals), and asks you to contact sales with your **seat count**
for a quote — **no public pricing** **[docs]**. Explicitly:

> "Open WebUI is free to use as-is for everyone. You can deploy it today
> without an enterprise agreement." **[docs]**

But also: enterprise licensing is limited to "registered entities and
organizations"; they "are unable to accommodate individual users" **[docs]**.
A formed Texas nonprofit qualifies as a registered entity. A guy with a website
does not — which is one more argument for forming the entity early (doc 05).

There is **no published nonprofit or public-sector discount** **[docs]**. Seat-
based pricing against a free-to-the-public community service is a bad shape for
us — our seat count is meant to grow while revenue per seat stays near zero.
Get a quote, but budget as if the answer is "no."

### Path C — Ask for written permission (worth trying, low cost)

Clause (ii) allows branding changes with "specific prior written permission from
the copyright holder." The documented precedent for a free carve-out is narrow —
academic researchers running **time-limited studies**, and the docs are explicit
that this is "intended exclusively for research studies, not general-purpose
use" **[docs]**. A permanent community service is not that.

Still: one email costs nothing, and the ask is sympathetic. Also note clause
(ii) can be earned another way — "substantive contributor" status. Which leads
to the posture question.

## Will they be friendly?

**Probably yes, with the important caveat that "friendly" and "free
white-labeling" are different things.** Read the incentives:

**Points in our favor:**

- Their stated posture is that free use is genuinely free and unconditional —
  "free to use as-is for everyone… deploy it today without an enterprise
  agreement" **[docs]**. They are not looking for reasons to police deployments.
- The relicense was aimed at large companies stripping the brand and reselling,
  not at community projects. We are the sympathetic case: a nonprofit that
  *keeps* their branding is a walking advertisement in a market segment
  (municipal/civic AI) they have no presence in.
- A named, on-the-record community nonprofit is a reference customer and a
  press story. "El Paso residents run their own AI on Open WebUI" is a headline
  they benefit from.
- Nothing about us competes with them.

**Points to be realistic about:**

- The 50-user threshold and the code-level enforcement are deliberate. They
  chose to make this the one thing you pay for. Expect them to hold the line on
  it, politely.
- Their nonprofit posture is *unstated*, not *generous*. The absence of a
  published discount is a real signal — there is a documented carve-out for
  academic research and none for nonprofits. Do not build a plan that assumes
  they'll waive it.
- "Registered entities only" means the ask lands better after incorporation.

**Recommended sequence:**

1. Launch on Path A with the suffix intact and the credit made loudly and
   voluntarily. This is compliant, free, and costs us nothing we care about.
2. Form the entity (doc 05).
3. Once formed, email enterprise sales **and** the maintainer, framed as: 501(c)
   community nonprofit, no revenue from AI resale, here is our transparency
   commitment, we would like either a nonprofit-rate enterprise license or
   written permission under clause (ii). Ask about co-marketing — we are worth
   more to them as a case study than as a seat-count invoice.
4. Contribute back. The credit-ledger inlet filter (doc 01, gap 2) is a real
   missing capability that other deployments want. Upstreaming it is genuinely
   useful, builds the relationship, and clause (ii) names "substantive
   contributor" status as a route to branding permission. This is the cheapest
   realistic path to Path C.

**Do not** patch out `WEBUI_NAME`, and do not launch with the branding removed
"until someone notices." The whole thesis of this organization is that it does
what it says. Start as you mean to continue.

## Open question for counsel

The clause defines end users as "individual natural persons with **direct
access** to the application." A donor who reads the public site is not an end
user; a member who logs into chat is. If we put our own UI in front of the API
and never expose Open WebUI's interface to members, the branding question gets
murky — but so does the value of using Open WebUI at all. Not worth being clever
about at MVP.
