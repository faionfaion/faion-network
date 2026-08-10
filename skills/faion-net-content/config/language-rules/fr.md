# French (fr) translation rules

**V4 doctrine — translate by default; tight English whitelist; cultural adaptation licence for body + headings; English-idiom accuracy; reading-register tilt to native target-language tech-writing. See `phase2-translate.md` and `style-guide.md` for the full v4 contract.**

## Voice transfer

- "Vous" as default — French tech audience expects respect even for informal topics.
- "Tu" only if brief explicitly requests informal voice (rare).
- Confident, sharp, ironic. NOT corporate-French ("nous explorerons" / "n'hésitez pas").
- Voice reference: indie French devs on Twitter, blog d'Olivier Tassinari, dev.to FR.

## Address register

Default: **vous** (singulier de politesse + pluriel). "tu" seulement si le brief l'exige (rare pour audience tech-pro).

## Banned (calques + corporate-FR)

| EN calque | fr correct |
|-----------|-----------|
| "faire du sens" | "avoir du sens" |
| "adresser un problème" | "aborder / résoudre un problème" |
| "actionnable" | "concret" / "applicable" |
| "à la fin de la journée" | "en fin de compte" |
| "sur le long terme" | "à long terme" |
| "checker" (= to check) | "vérifier" |
| "delivrer" (= to deliver) | "livrer" |
| "process" (noun) | "processus" |
| "n'hésitez pas à" | banned — empty filler |
| "dans cet article" | banned — empty meta |
| "livrables" (overuse) | nom spécifique |

## V2 anglicism policy — translate by default

La liste des mots gardés en anglais est ÉTROITE. Tout le reste se traduit.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Acronymes industriels — pas d'équivalent fr |
| runway, churn, burn rate | Métriques SaaS — convention de la communauté indie |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — pas d'équivalent fr |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — la v1 laissait trop d'anglais)

| English | fr target |
|---------|-----------|
| feature | fonctionnalité |
| workflow | flux de travail / processus |
| pattern | modèle / motif |
| ship (verb) | livrer / publier / sortir |
| deploy (verb) | déployer |
| burnout | épuisement professionnel / burn-out (graphie acceptée — préférer "épuisement") |
| pivot (noun/verb) | virage / pivoter (verbe accepté en jargon) |
| brokerage | compte de courtage |
| moonshot | pari ambitieux |
| sanity check | vérification de base / contrôle de cohérence |
| handoff | transmission / passage de relais |
| half-step | demi-pas |
| trigger | déclencheur |
| dashboard | tableau de bord |
| optics | apparence / perception |
| haircut (= discount) | décote / réduction |
| bookings | réservations / contrats signés |
| framework | framework (OK — installé dans le jargon tech) |
| stack | stack (OK — installé) |
| onboarding | onboarding (toléré) / intégration |
| post-mortem | post-mortem (industry term OK) |

**Règle**: si un mot fr capture le sens sans perte, UTILISE-LE. La v1 penchait vers l'anglais; reset.

## Anti-AI-tell en fr — banned target-language moves

### Banned openings + meta

- "Dans cet article, nous..." / "Dans cet article, nous explorerons"
- "Plongeons dans" / "Explorons" / "Décortiquons"
- "Bienvenue dans le monde de X" / "Dans le monde actuel"
- "Il est important de noter que" / "Il convient de souligner"
- "Comme nous le verrons" / "Comme nous le verrons plus loin"
- "À l'heure actuelle" / "De nos jours"
- "N'hésitez pas à"

### Banned closers

- "En conclusion" / "Pour conclure" / "Pour résumer"
- "En résumé"
- "Nous espérons que cet article vous a été utile"

### Banned filler vocab (fr equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | fr forbidden |
|--------------|--------------|
| delve | plonger / s'enfoncer dans (comme rhétorique vide) |
| tapestry | tapisserie / mosaïque (métaphore creuse) |
| landscape | paysage (= "le paysage actuel") |
| realm | domaine / sphère (filler) |
| navigate (challenges) | naviguer (= traverser) |
| robust | robuste (comme intensificateur vide) |
| leverage (verb) | tirer parti de (toléré une fois, banni en filler) / capitaliser sur |

### Banned intensifiers

- "profondément" / "incroyablement" / "absolument" / "définitivement" (vides)
- "véritablement" / "réellement" (filler avant un adjectif)

### Banned structural moves

- Trios "X, Y et Z" à chaque phrase
- "Ce n'est pas juste X — c'est Y" pivot
- Plus de 2 tirets cadratin par paragraphe
- Phrase de fermeture à chaque section
- Sous-titre tous les 200 mots
- Double négation quand le positif existe ("il n'est pas impossible" → "c'est possible")

## Prompt-callout translation policy

L'article contient des blocs `<PromptCallout>`. Règles :

- **Le préfixe `/faion` RESTE en anglais** — c'est une commande.
- Tout APRÈS `/faion` se traduit en fr comme une requête naturelle.
- Nombres, monnaie, termes du whitelist (MRR, burn, runway) verbatim.
- Espace insécable avant le signe monétaire ($) : à l'intérieur du prompt, garder le format US (`$50K`) — c'est un input technique.

Exemple :

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- fr: `/faion calculons mon runway : 50K$ d'épargne, burn 4K$/mois, MRR 800$`

Autres :

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- fr: `/faion vérifie le PMF de mon SaaS solo selon le rubric à 5 critères`

- EN: `/faion build me a 30-60-90 day plan`
- fr: `/faion construis-moi un plan 30-60-90 jours`

## Receipt preservation (NEVER translate)

Ce sont des credentials d'authenticité. Verbatim :

- **Noms de personnes**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — original.
- **Dates**: "March 2014" → "mars 2014" OK (précision identique).
- **Dollars**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Jamais "environ 250 mille".
- **Lieux**: Bay Area, San Francisco, Lisbon — original.
- **HN handles, Twitter handles, URLs**: verbatim.

Principe : la spécificité rend l'anecdote unfalsifiable. Traduire "$250K" en "environ deux cent cinquante mille" tue la crédibilité.

## Tone

- Direct, avec la clarté française.
- Registre légèrement plus formel que l'EN — mais jamais corporate.
- Éviter doubles négations là où le positif existe.
- Structure phrasale fr peut diverger de l'EN — restructurer pour le flow.

## Cultural

- $ conservé (benchmarks US). Pas de conversion en EUR.
- Exemples indie fr encouragés là où ils remplacent du générique.
- Dates: "25 mai 2026" ou "2026-05-25" (ISO pour contextes techniques).

## Reviewer checklist

- [ ] "vous" cohérent (sauf brief = "tu").
- [ ] Pas de "n'hésitez pas" / "dans cet article" / "plongeons dans" filler.
- [ ] Pas de calques corporate ("checker", "delivrer", "process" noun).
- [ ] V2: tous les mots de la liste TRANSLATE traduits (feature, workflow, ship, deploy, burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist préservé (CLI, MRR, runway, churn, brands, US tax).
- [ ] Anti-AI-tell : aucun "dans cet article / il est important de noter / en conclusion".
- [ ] Receipts (noms, dates, $, lieux) verbatim.
- [ ] Prompt-callouts : `/faion` EN, corps naturel en fr.
- [ ] Slugs de méthodologies verbatim.
- [ ] No emojis.
- [ ] Voice = confident + direct + ironic.
