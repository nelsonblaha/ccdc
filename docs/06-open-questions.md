# Open questions

Ordered by how much they change the plan. Each one needs a human decision or an
external answer; none of them should block Phase 0 (doc 04).

## Blocking before money changes hands

1. **Open charitable program, or closed member benefit?** Doc 05, "the decision
   that shapes everything else." Note this is *not* "can we charge money" —
   501(c)(3)s charge for services all the time, and related fee income is not
   even taxed. The fork is whether the beneficiary class is broader than the
   class of payers, and whether pricing looks charitable or commercial. Option A
   (open sliding-scale program; membership buys governance) is recommended.
   **Decide before filing Form 202**, because the certificate encodes it.

   1a. What are the actual **numbers in the paid band**? Doc 05 and the site both
   say $5–50/mo deliberately vaguely, because the board should set it. The free
   tier has to be real and used, not a demo, or the commerciality analysis (doc 05)
   gets much harder.

2. **Do the Google for Nonprofits cloud credits apply to Vertex AI inference,
   or only to compute/storage?** Doc 03 treats this as the load-bearing
   financial assumption. If inference is excluded, year-one cash cost goes from
   ~$0 to ~$2,600 and the fundraising story changes. **One hour of someone's
   time; highest value-per-minute item in this repo.**

3. **Who are directors #2 and #3?** Texas requires three (TBOC § 22.204)
   **[web]**. This gates Stage 2 entirely, and recruiting people who will
   disagree with you takes longer than any of the software.

   3a. **What date do the founding bylaws commit to the first member election?**
   Doc 05 argues for a hard deadline written in while you still control the
   process. Pick it now; it gets harder to pick later, which is the point.

   1b. **Is Ciudad Juárez in scope?** Doc 11. Serving Juárez residents over the
   internet is straightforward; hardware or staff in Mexico is not. If yes, the
   purpose clause must say so **at filing** — the third thing that has to be
   settled before Form 202.

## Needs a lawyer

4. Bylaws: quorum, voting, member classes, the supermajority lock on the purpose
   clause, and the founder-rights sunset (doc 05).
5. Whether the member compute allocation as designed survives the private
   benefit test, and how to word the quid-pro-quo disclosure on dues.
6. Long-form 1023 vs 1023-EZ. Doc 05 recommends the long form despite EZ
   eligibility; confirm the extra scrutiny is worth the delay.
6a. **Founder compensation.** Doc 05, "Can the founder be paid?" — yes, but the
   rebuttable-presumption procedure needs directors who are independent *in
   fact*, not just on paper. Moot until there is a budget; the structure that
   makes it defensible (who is on the comp committee) has to exist first.

7. Terms of service and privacy policy, specifically the "we do not train on
   your conversations" commitment — which needs to be backed by the inference
   provider's contract, not just our own promise.
8. Do we need charitable solicitation registration in states other than Texas if
   we solicit donations on a public website? **[unverified]**

8a. **A Mexican privacy lawyer**: does the 2025 LFPDPPP reach a service run from
   US servers? Doc 11 marks this unresolved, and it gates any Juárez outreach
   that collects data at scale.

8b. **Native review of the Spanish site copy** before it does real work. Written
   for a border-Mexican register and careful about the traps (`mil millones`, not
   `billón`), but not a native speaker's ear.

## Needs a decision from you

9. **The name.** "Community Data Center" promises hardware we will not own for
   years (doc 05, last section). Rename, or keep it and publish a milestone
   schedule we report against annually including misses.

   **Domain candidates, recorded before anything is registered:**
   `chucodc.org` and `chucodata.org`. Both keep "Chuco", which is the half of
   the name that means something locally, and neither claims a facility the way
   a `datacenter` domain would; `chucodc.org` is shorter to say aloud, and
   `chucodata.org` is the one someone can spell after hearing it once. Neither
   is registered yet and this is not a decision, only a note so the options are
   not rediscovered later. Whatever is chosen becomes the permanent home when
   the service moves off `ccdc.blaha.io`, which is currently a personal
   hostname; see doc 09. Check both against the Texas SOS name availability
   search at the same time as the entity name, since a domain that does not
   match the filed name is a small permanent annoyance.
10. **Who is the service *for*?** Any El Paso resident? Anyone who asks?
    Students? Small nonprofits? This determines the charitable class, which
    determines the exemption argument, which determines everything in doc 05.
    It is also the question a donor asks first.
11. **Default model.** Doc 03's table spans 50× in cost per member. Flash-Lite
    at $0.13/member/month is defensible and unimpressive; Gemini 2.5 Pro at
    $2.17 feels like ChatGPT. Recommend Flash as default with Pro available on
    allocation.
12. **Do we offer this to non-members at all?** Free public access strengthens
    the charitable case (doc 05, Option A) and is the main cost risk. The credit
    ledger has to handle anonymous or lightly-authenticated public users too,
    or abuse is unbounded.

## Needs doing, not deciding

**Turn off Cloudflare Web Analytics for the `blaha.io` zone.** Cloudflare injects
`static.cloudflareinsights.com/beacon.min.js` into HTML for browser requests
across the whole zone. It is **invisible to `curl`** without a browser
User-Agent, which is why it went unnoticed — and it made the privacy panel's "no
analytics" claim false for real visitors while looking true to anyone checking
the way an engineer would.

The page now states this plainly instead. To actually fix it: Cloudflare dashboard
→ the `blaha.io` zone → Analytics → Web Analytics, and disable the automatic
setup / RUM beacon. Needs Ben's dashboard access. Then restore the stronger
sentence.

Worth keeping as a lesson rather than just a task: the claim was checked with the
wrong tool, and the wrong tool said everything was fine. Anything this project
asserts about what it does *not* do should be verified the way a visitor
experiences it.

## Needs verification before quoting publicly

13. Cloud Run **instance-based** per-unit rates — could not verify; doc 03 marks
    it **[unverified]**.
14. Whether Vertex AI Gemini pricing matches the AI Studio prices in doc 03 —
    they are usually the same but are published separately.
15. Current Google for Nonprofits credit amount and eligibility (the $10,000
    figure is **[web]**, not from Google's own page).
16. Provider water and energy figures per unit of compute, and whether any of
    them are regional enough to say anything honest about El Paso specifically.
    This is the organization's signature claim; it cannot rest on a secondary
    source.

## Worth trying, low cost, no rush

17. Email Open WebUI enterprise sales *after* incorporation asking about a
    nonprofit rate or clause (ii) written permission (doc 02). Expect the answer
    to be no; the relationship is worth more than the branding.
18. Upstream the credit-ledger inlet filter (doc 02, doc 04). Useful to others,
    builds standing, and is a named route to branding permission.
19. Find a fiscal sponsor in El Paso or Texas (doc 05, Stage 1) so donations can
    be deductible months before the determination letter arrives.
