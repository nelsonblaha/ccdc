# Binational scope: serving Ciudad Juárez

> **Not legal advice**, and this half needs a *Mexican* lawyer in addition to the
> Texas one. Research to make you a prepared client.

## Why the name changed

**El Paso Community Data Center → Chuco Community Data Center /
Centro Comunitario de Datos de Chuco.** The acronym survives translation, which
is why this pairing and not a more literal one.

Three things the new name does that the old one didn't:

1. **"El Chuco" is binational.** It comes out of Pachuco culture, which was never
   confined to one side of the river. "El Paso" names a US municipality; "Chuco"
   names a place people on both sides recognize.
2. **It cannot be mistaken for city government** — the objection that already
   came up twice about "governed by El Paso." No one thinks a nickname is a
   municipal department.
3. It is the name locals actually use, which matters for an organization whose
   whole claim is that it belongs to locals.

The site footer notes, in both languages, that the nickname is used with
affection and not on anyone's authority.

## The question splits cleanly

Everything about extending to Juárez sits on one side or the other of a single
line: **do we have a physical or legal presence in Mexico?**

| | Serving Juárez residents over the internet | Hardware or staff in Juárez |
|---|---|---|
| US charitable status | fine | fine |
| Deductibility of donations | unaffected | unaffected |
| Mexican entity required | no | **yes** (an *A.C.*) |
| Mexican tax registration | no | yes; possibly *donataria autorizada* |
| Import duties on equipment | no | yes |
| Books | one set | two, plus transfer pricing |
| Verdict | **do it from day one** | **defer** |

### The US side is genuinely a non-issue

- A 501(c)(3) **may serve foreign beneficiaries.** There is no requirement that a
  charitable class be domestic, and "residents of the El Paso–Ciudad Juárez
  metropolitan area" is a valid class — a charitable class may consist of all
  individuals in a city, county, or state (doc 05), and nothing restricts that
  to US geography. **[web]**
- **Deductibility is unaffected**, because it depends on the recipient
  *organization* being domestic, not on where it spends. **[web]**
- The rule people worry about — **"discretion and control,"** the anti-conduit
  doctrine — only engages when a US charity **grants money to a foreign
  organization** **[web]**. If CCDC operates the service itself and Juárez
  residents log in, that is direct program delivery and the doctrine never
  applies. **Do not fund a Juárez NGO to do it for us** unless someone has
  actually read those rules; that is the version that creates exposure.
- Administrative additions: **Schedule F** on the Form 990 for foreign activity
  above the threshold, and OFAC screening. Mexico is not sanctioned; screening is
  a procedure, not a project.

### The Mexican side is the actual work, and it changed in 2025

Do not plan against the law as it stood two years ago:

- The **new LFPDPPP** (Ley Federal de Protección de Datos Personales en Posesión
  de los Particulares) was published **20 March 2025** and took effect the next
  day, repealing the 2010 law. **[web]**
- **INAI is dissolved.** A December 2024 constitutional decree moved its
  functions to the **Secretaría Anticorrupción y Buen Gobierno**, an
  executive-branch ministry rather than an autonomous regulator. **[web]**
- The new law **expands data subject rights and adds accountability for
  AI-driven decision-making** **[web]** — which is us, specifically.
- Fines run **100 to 320,000 UMA**, higher for sensitive data. **[web]**

⚠️ **Unresolved and important: I could not confirm whether the new law reaches a
service operated from US servers.** Extraterritorial scope is the pivotal
question — it decides whether any of the above is our problem at all — and it
needs a Mexican privacy lawyer, not a search result. Treat every compliance
estimate below as conditional on that answer.

If we are in scope, the work is: a Spanish-language **aviso de privacidad**,
honoring **ARCO rights** (acceso, rectificación, cancelación, oposición), and
disclosing cross-border transfer. Weeks, not years.

There is also an irony worth naming rather than hiding: an organization whose
pitch is *independent* accountability would, on the Mexican side, be regulated by
a body that is no longer independent. That doesn't stop anything. It does make
the compliance posture less predictable than it was, and it is the kind of thing
we should say out loud given what we say about everyone else.

## Why this strengthens the mission

Not sentiment — argument. The **Rio Grande / Río Bravo** and the **Hueco Bolson
aquifer** are shared, as is the airshed. A data center's draw on either is a
binational fact regardless of how anyone treats it.

So an organization premised on local accountability for water and power that drew
its own line at the river would be arguing a **visibly weaker version of its own
case**, and the first hostile question in a public meeting writes itself. The
binational framing isn't an expansion of scope; it's what makes the water
argument coherent.

## Consequences already landed

- **The site is bilingual.** `site/index.html` (en) and `site/es/index.html` (es),
  sharing `site/style.css` and `site/script.js` so the two cannot drift visually
  or behaviorally. Switcher in the header of each, `hreflang` alternates, and
  `/es/gracias` alongside `/thanks`.
- **The signup endpoint is localized.** One endpoint; the form posts a `lang`
  field, errors return in that language, and `lang` is recorded on each signup —
  so we learn what language the list actually speaks.
- **No Accept-Language auto-redirect**, deliberately. A visitor who picked a
  language by clicking should not be overridden by their browser's settings, and
  auto-redirects break shared links.
- Free tier is stated as "anyone with an El Paso **or Juárez** ID," and the
  roadmap's step 06 says free access for residents **on both sides of the river**.
- Step 11 (own the hardware) still says **El Paso** specifically. That is not an
  oversight — it is where the equipment can sit without triggering the right-hand
  column of the table above.

## Consequences with deadlines

1. **The purpose clause, before Form 202 is filed** (roadmap step 03). If Juárez
   is in scope, the certificate of formation should say so at filing —
   e.g. "residents of the El Paso–Ciudad Juárez binational metropolitan area."
   Retrofitting means amending the certificate at exactly the moment amendments
   are hardest (doc 05). **This is now a third thing that must be decided before
   incorporation**, alongside the charity-vs-cooperative fork and the price
   ladder.
2. **The Spanish text needs a native review before it does real work.** It was
   written for a border-Mexican register — *caja popular*, *río Bravo*,
   *socios*, *tú* rather than *usted*, and `mil millones` for "billion" (never
   *billón*, which is 10¹² in Spanish and would overstate Meta's investment by
   a thousandfold). It is careful, and it is still not a native speaker's ear.
   Quotes translated from English are **marked as translations**, with the
   original English linked.
3. **Ask a Mexican lawyer the extraterritorial question** before any Juárez
   outreach that collects data at scale.
