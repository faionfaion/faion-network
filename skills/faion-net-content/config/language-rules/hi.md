# Hindi (hi) translation rules

**V2 doctrine — translate Hindi connective tissue aggressively; preserve English ONLY for whitelist + natural code-switch vocabulary.**

## Voice transfer

- Indian tech audience is heavily bilingual. Code-switch is natural and expected.
- Default: Hindi for connective tissue + argumentation; English for technical terms.
- "आप" (formal you) as default for blog content; "तुम" only if brief explicitly requests casual.
- Confident, sharp. NOT corporate-Hindi ("इस लेख में हम").

## Address register

Default: **आप** (formal-neutral, blog-standard for indie-tech audience). "तुम" only if brief explicitly requests casual register (rare for Faion content).

## Code-switching policy (most important)

This is the dominant decision. Calibrate carefully:

| Keep in English | Translate to Hindi |
|-----------------|---------------------|
| Industry acronyms (whitelist below) | Connectives, prepositions, verbs |
| Brand names | Common verbs ("करना", "होना") |
| Product names | Pronouns, articles |
| Code blocks + commands | Conjunctions ("लेकिन", "इसलिए") |
| Methodology slugs | Adjectives describing concepts (where natural) |
| File paths | Time references (आज, कल, अब) |
| | Pain-point descriptions when Hindi carries better |
| | Emotional/experiential vocabulary (burnout, frustration, doubt) |

The article should READ like an Indian indie-dev would naturally talk — Hindi sentence skeletons with English tech vocabulary embedded.

## V2 anglicism policy — tighter even for hi

Despite natural code-switch tolerance, V2 narrows the English-allowed set. Default: prefer Hindi for non-technical English words that have a clean Hindi equivalent.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Industry acronyms — no hi equivalent |
| runway, churn, burn rate | SaaS metrics — community convention |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — no hi equivalent |
| feature, framework, stack, deploy, ship, dashboard, trigger, pattern, workflow, onboarding, post-mortem | Naturally code-switched in Indian tech English-Hindi speech — KEEP in English even though other languages translate them |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — even hi has these in Hindi)

| English | hi target |
|---------|-----------|
| burnout | जलन / थकावट (या "burnout" — code-switch tolerated, prefer Hindi for emotional weight) |
| pivot (noun/verb) | दिशा बदलना / मोड़ |
| brokerage | ब्रोकरेज खाता / दलाली |
| moonshot | बड़ा दांव / महत्वाकांक्षी प्रयोग |
| sanity check | सामान्य जाँच / सही-गलत की जाँच |
| handoff | सौंपना / हस्तांतरण |
| half-step | आधा कदम |
| optics | दिखावा / धारणा |
| haircut (= discount) | छूट / कटौती |
| bookings | बुकिंग्स / तय हुए सौदे |

**Rule**: technical English in Indian tech speech is natural — keep it. But emotional/experiential words (burnout, pivot, optics) carry MORE punch in Hindi for an Indian reader. Tilt to Hindi there.

## Banned

- **Pure-Sanskrit Hindi for tech content** (sounds like government press release).
- **Pure-English with Hindi connectives only** (= broken translation, not natural code-switch).
- **Roman script for Hindi words (Hinglish romanisation)** — use Devanagari ("करना", not "karna") in article body. Exception: speakable shell commands.

## Anti-AI-tell in hi — banned target-language moves

### Banned openings + meta

- "इस लेख में हम..." / "इस लेख में आइए"
- "आइए गहराई से समझें" / "आइए डुबकी लगाएं" (literal "let's dive")
- "X की दुनिया में आपका स्वागत है"
- "ध्यान देने योग्य बात है कि..." / "यह उल्लेखनीय है कि"
- "जैसा कि हम आगे देखेंगे" / "जैसा कि हम देखेंगे"
- "आज के दौर में" / "वर्तमान समय में"

### Banned closers

- "निष्कर्ष के तौर पर" / "अंत में" / "समाप्ति पर"
- "सारांश में"
- "हमें उम्मीद है कि यह लेख आपके लिए उपयोगी रहा"

### Banned filler vocab (hi equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | hi forbidden |
|--------------|--------------|
| delve | गहराई में जाना / डुबकी लगाना (as filler rhetoric) |
| tapestry | ताना-बाना (as metaphor cliché) |
| landscape | परिदृश्य (as filler — "वर्तमान परिदृश्य") |
| realm | क्षेत्र / दायरा (as filler) |
| navigate (challenges) | नेविगेट करना / रास्ता तय करना (as filler) |
| robust | मज़बूत (as empty intensifier) / सशक्त (as filler) |
| leverage (verb) | फायदा उठाना / लाभ उठाना (as filler verb) |

### Banned intensifiers

- "अत्यंत" / "अविश्वसनीय रूप से" / "बेहद" / "नितांत" (empty)
- "वास्तव में" / "सचमुच" (as filler before adjective)

### Banned structural moves

- "X, Y और Z" tricolon in every sentence
- "यह केवल X नहीं है — यह Y है" pivot
- More than 2 dashes per paragraph
- Closing sentence in every section
- Subheading every 200 words

## Prompt-callout translation policy

The article contains `<PromptCallout>` blocks. Rules:

- **`/faion` prefix STAYS in English** — it's a command.
- Everything AFTER `/faion` translates to hi as a natural request. Natural code-switch is welcomed here.
- Numbers, currency, whitelist terms (MRR, burn, runway, savings) verbatim.

Example:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- hi: `/faion चलिए मेरा runway calculate करते हैं: $50K savings, $4K/month burn, $800 MRR`

Others:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- hi: `/faion मेरे solo SaaS का PMF 5-criterion rubric के साथ check करो`

- EN: `/faion build me a 30-60-90 day plan`
- hi: `/faion मेरे लिए एक 30-60-90 दिन का plan बनाओ`

Note: in prompts the code-switch density is HIGHER than in article prose. The prompt is a command; sounding like real Indian dev speech is the priority.

## Receipt preservation (NEVER translate)

ये authenticity के credentials हैं। Verbatim:

- **People names**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — original (Roman script even in Devanagari prose).
- **Dates**: "March 2014" → "मार्च 2014" OK (precision identical).
- **Dollar amounts**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Never "लगभग 250 हज़ार".
- **Places**: Bay Area, San Francisco, Lisbon — original (Roman script).
- **HN handles, Twitter handles, URLs**: verbatim.

Principle: specificity makes the anecdote unfalsifiable. Translating "$250K" as "लगभग ढाई लाख डॉलर" loses precision and credibility.

## Tone

- Direct + warm. Indian tech blogs (Inc42, YourStory technical content, indie founders).
- Imperative voice ("कीजिए" formal, "करो" casual) for instructions — match register to "आप".
- Avoid English "let's" → restructure naturally; use "चलिए" (formal) only when it fits.

## Numbers

- Lakh/crore acceptable in commentary when Indian-context numbers; for receipt numbers ($250K, etc.) keep US format.
- $ in headers/examples stays as USD.

## Sentence structure

- Hindi SOV (subject-object-verb) — restructure English SVO sentences.
- Postpositions, not prepositions.
- Don't translate English clause structure word-for-word; rewrite into natural Hindi flow.

## Cultural

- $ kept (US benchmarks); occasionally pair with INR equivalent if INR-context relevant.
- Indian indie examples encouraged (Indian indie SaaS founders, Razorpay-era stories, Bootstrapped India).
- Dates: "25 मई 2026" or "2026-05-25" (ISO for technical contexts).

## Reviewer checklist

- [ ] Code-switch ratio feels natural (neither pure-Sanskrit nor pure-English-with-connectives).
- [ ] "आप" / "तुम" consistent.
- [ ] Devanagari script for Hindi words (not romanised).
- [ ] V2: emotional/experiential English (burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, optics, haircut, bookings) considered for Hindi where punch lands harder.
- [ ] Whitelist preserved (CLI, MRR, runway, churn, brands, US tax + naturally code-switched tech vocab).
- [ ] Anti-AI-tell: no "इस लेख में हम / आइए गहराई से समझें / ध्यान देने योग्य बात है / निष्कर्ष के तौर पर".
- [ ] Receipts (names, dates, $, places) verbatim in Roman script for names/places.
- [ ] Prompt-callouts: `/faion` EN, body natural Indian code-switched hi.
- [ ] Methodology slugs verbatim.
- [ ] No emojis.
- [ ] Voice = direct + warm + confident.
