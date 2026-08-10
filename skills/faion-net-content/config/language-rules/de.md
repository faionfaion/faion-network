# German (de) translation rules

**V2 doctrine — translate by default; tight English whitelist. German keeps more anglicisms than fr/es due to tech-vocabulary borrowing patterns, but the whitelist is still strict.**

## Voice transfer

- "Sie" as default — German tech audience expects formal register, even for indie topics.
- "Du" only if brief explicitly requests informal voice. Most indie-German content uses "du", so consider per article.
- Confident, sharp, direct. NOT corporate-Deutsch ("Lassen Sie uns gemeinsam erkunden").
- Voice reference: t3n, heise, indie German devs.

## Address register

Default: **Sie** für allgemeine Tech-Leserschaft. **Du** wenn das Brief informell verlangt (häufig bei indie-Inhalten — pro Artikel entscheiden). Niemals beides im selben Artikel mischen.

## Banned (calques + corporate-DE filler)

| EN calque | de correct |
|-----------|-----------|
| "Sinn machen" (Anglizismus) | "Sinn ergeben" / "sinnvoll sein" |
| "in 2026" | "im Jahr 2026" / "2026" |
| "letztendlich" (overused) | "schließlich" / spezifisch |
| "Lassen Sie uns ..." | banned — corporate filler |
| "In diesem Artikel" | banned — empty meta |
| "umsetzbar" (= actionable, overuse) | konkret formulieren |
| "definitiv" (overuse) | sparsam einsetzen |
| "Nicht zuletzt" | sparsam einsetzen |

## V2 anglicism policy — translate by default

Die Liste der englischen Begriffe ist EHRGEIZIG KURZ. Alles andere übersetzen. Deutsch behält einige Anglizismen, die Polnisch/Französisch übersetzen würden (z.B. "Burnout", "Framework"), aber der Default bleibt deutsch.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Industry-Akronyme — kein de Äquivalent |
| runway, churn, burn rate | SaaS-Metriken — Community-Konvention |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / Produktnamen |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — kein de Äquivalent |
| Burnout | Im Duden, voll eingebürgert; "Erschöpfungssyndrom" klingt klinisch |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — die v1 ließ zu viel Englisch)

| English | de target |
|---------|-----------|
| feature | Funktion / Feature (toleriert, aber "Funktion" bevorzugt) |
| workflow | Arbeitsablauf / Prozess |
| pattern | Muster |
| ship (verb) | ausliefern / veröffentlichen / shippen (Slang OK im Voice) |
| deploy (verb) | ausrollen / deployen (Slang OK) |
| pivot (noun/verb) | Kurswechsel / Richtungswechsel / pivotieren (Jargon OK) |
| brokerage | Broker-Konto / Wertpapierdepot |
| moonshot | ehrgeiziges Experiment / Moonshot (toleriert) |
| sanity check | Plausibilitätsprüfung |
| handoff | Übergabe |
| half-step | Halbschritt |
| trigger | Auslöser / Trigger (toleriert) |
| dashboard | Dashboard (toleriert — eingebürgert) / Übersicht |
| optics | Außenwirkung / Wahrnehmung |
| haircut (= discount) | Abschlag / Rabatt |
| bookings | Buchungen / abgeschlossene Verträge |
| framework | Framework (OK — eingebürgert) |
| stack | Stack (OK — eingebürgert) |
| onboarding | Onboarding (OK — eingebürgert) / Einarbeitung |
| post-mortem | Post-Mortem (industry term OK) |

**Regel**: gibt es ein deutsches Wort, das die Bedeutung vollständig erfasst, BENUTZE ES. v1 ging Richtung Englisch; reset.

## Anti-AI-tell auf de — banned target-language moves

### Banned openings + meta

- "Lassen Sie uns gemeinsam..." / "Lassen Sie uns erkunden"
- "In diesem Artikel werden wir..." / "In diesem Artikel werfen wir einen Blick auf"
- "Tauchen wir ein in" / "Begeben wir uns auf eine Reise"
- "Willkommen in der Welt von X"
- "Es ist wichtig zu betonen, dass" / "An dieser Stelle sei erwähnt"
- "Wie wir noch sehen werden"
- "In der heutigen Zeit" / "Heutzutage"

### Banned closers

- "Zusammenfassend lässt sich sagen" / "Abschließend"
- "Wir hoffen, dieser Artikel war hilfreich"
- "Fazit:"

### Banned filler vocab (de equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | de forbidden |
|--------------|--------------|
| delve | eintauchen / sich vertiefen (als leere Rhetorik) |
| tapestry | Tapisserie / Mosaik / "buntes Bild" (Metapher) |
| landscape | Landschaft (= "die aktuelle Landschaft") / Umfeld als Filler |
| realm | Sphäre / Reich (Filler) / Bereich (als Filler) |
| navigate (challenges) | navigieren (= bewältigen) als Filler |
| robust | robust (als leerer Intensifier) |
| leverage (verb) | nutzen / hebeln (als Filler-Verb) |

### Banned intensifiers

- "absolut" / "definitiv" / "unglaublich" / "zutiefst" (leer)
- "wahrhaft" / "wirklich" (als Filler vor Adjektiv)

### Banned structural moves

- Dreierfiguren "X, Y und Z" in jedem Satz
- "Es ist nicht nur X — es ist Y" Pivot
- Mehr als 2 Gedankenstriche pro Absatz
- Schlusssatz in jedem Abschnitt
- Zwischenüberschrift alle 200 Wörter
- Passivkonstruktionen wo aktiv funktioniert

## Prompt-callout translation policy

Der Artikel enthält `<PromptCallout>` Blöcke. Regeln:

- **Das Präfix `/faion` BLEIBT auf Englisch** — es ist ein Befehl.
- Alles NACH `/faion` wird ins Deutsche übersetzt als natürliche Anfrage.
- Zahlen, Währung, Whitelist-Begriffe (MRR, burn, runway) verbatim.

Beispiel:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- de: `/faion lass uns meine Runway berechnen: $50K Erspartes, $4K/Monat Burn, MRR $800`

Weitere:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- de: `/faion prüf den PMF von meinem Solo-SaaS gegen das 5-Kriterien-Rubric`

- EN: `/faion build me a 30-60-90 day plan`
- de: `/faion bau mir einen 30-60-90-Tage-Plan`

(Bei "Sie"-Register: `/faion lassen Sie uns ...` — explizit vermeiden, da das ein gebanntes Filler-Phrasing ist. Stattdessen: `/faion berechnen wir meine Runway: ...`)

## Receipt preservation (NEVER translate)

Sie sind Beglaubigungen der Authentizität. Verbatim:

- **Personennamen**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — Original.
- **Daten**: "March 2014" → "März 2014" OK (Präzision identisch).
- **Dollarbeträge**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Niemals "etwa 250 Tausend".
- **Orte**: Bay Area, San Francisco, Lisbon — Original.
- **HN handles, Twitter handles, URLs**: verbatim.

Prinzip: Spezifizität macht die Anekdote unfalsifiable. "$250K" als "rund zweihundertfünfzigtausend" zu übersetzen tötet die Glaubwürdigkeit.

## Capitalization

- Alle Substantive großgeschrieben (Standard).
- Englische Lehnsubstantive ebenfalls groß: "Das Framework", "Der Stack", "Das Dashboard", "Die Runway".
- Englische Verben in deutscher Konjugation: "deployen", "shippen", "scalen", "pivotieren".

## Tone

- Direkt, präzise. Deutsche Klarheit vor Floskeln.
- Komposita OK, aber Monstrositäten mit Bindestrich auflösen.
- Doppelte Verneinung vermeiden, Passiv vermeiden wenn Aktiv funktioniert.

## Cultural

- $ beibehalten (US-Benchmarks); gelegentlich EUR-Äquivalent dazugeben falls Leser-Verwirrung droht.
- Deutsche indie-Beispiele encouraged (Tobias Lütke, German indie SaaS, t3n features).
- Daten: "25. Mai 2026" oder "2026-05-25".

## Reviewer checklist

- [ ] "Sie" oder "du" durchgehend konsistent (laut Brief).
- [ ] Substantiv-Großschreibung korrekt.
- [ ] Kein "Lassen Sie uns" / "In diesem Artikel" / "Tauchen wir ein" filler.
- [ ] Kein "Sinn machen" Calque.
- [ ] V2: alle Wörter aus der TRANSLATE-Liste übersetzt (feature, workflow, ship, deploy, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist erhalten (CLI, MRR, runway, churn, Burnout, Framework, brands, US tax).
- [ ] Anti-AI-tell: kein "lassen Sie uns / es ist wichtig zu betonen / zusammenfassend".
- [ ] Receipts (Namen, Daten, $, Orte) verbatim.
- [ ] Prompt-callouts: `/faion` EN, Korpus natürlich auf de.
- [ ] Methodologie-Slugs verbatim.
- [ ] Komposita lesbar (ggf. Bindestrich).
- [ ] No emojis.
- [ ] Voice = direct + precise + confident.
