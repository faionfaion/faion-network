# Polish (pl) translation rules

**V2 doctrine — translate by default; tight English whitelist. Polish tech speech keeps more anglicisms than fr/es naturally, but the V2 whitelist is still narrower than v1.**

## Voice transfer

- "Ty" / "Wy" / "Pan/Pani" — Polish is register-sensitive.
- Default for indie-tech audience: "ty" (informal singular). Switch to "Pan/Pani" only if brief explicitly requests formal.
- Polish tech blogs use "ty" widely for indie-builder content.
- Confident, sharp, ironic. NOT corporate-Polish ("W niniejszym artykule").
- Voice reference: bulldogjob, jakdojade tech threads, Polish indie devs on Twitter.

## Address register

Default: **ty** (informal singular) dla indie-tech audience. **Pan/Pani** tylko gdy brief tego wymaga (formal context). "Wy" plural neutralne.

## Banned (calques + corporate-PL filler)

| EN calque | pl correct |
|-----------|-----------|
| "robić sens" | "mieć sens" |
| "wziąć pod uwagę" | "uwzględnić" |
| "na końcu dnia" | "w ostateczności" / "ostatecznie" |
| "w długim okresie" | "w dłuższej perspektywie" |
| "actionable" → "praktyczny" / "konkretny" | OK |
| "W niniejszym artykule" | banned — corporate filler |
| "Zachęcamy do" | banned — corporate filler |
| "Bez wątpienia" | sparsam — easily overused |
| "Warto zauważyć" | banned — empty meta |

## V2 anglicism policy — translate by default

Polski jest pełen tech-anglicyzmów, ale V2 zwęża whitelist. Domyślnie tłumacz — anglicyzm tylko gdy jest naprawdę zakorzeniony.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Akronimy branżowe — brak pl odpowiednika |
| runway, churn, burn rate | Metryki SaaS — konwencja społeczności indie |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — brak pl odpowiednika |
| framework, stack, deploy (jako termin techniczny) | Głęboko zakorzenione w polskim tech-żargonie |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — v1 zostawiała zbyt wiele angielskiego)

| English | pl target |
|---------|-----------|
| feature | funkcja / funkcjonalność |
| workflow | przepływ pracy / proces |
| pattern | wzorzec |
| ship (verb) | wypuścić / wydać / shippować (kolokwialne OK w voice) |
| deploy (verb) | wdrożyć / zdeployować (slang OK) |
| burnout | wypalenie zawodowe |
| pivot (noun/verb) | zwrot / pivot (toleruje się, ale "zwrot" lepiej) |
| brokerage | konto maklerskie / dom maklerski |
| moonshot | ambitny strzał / wielki strzał |
| sanity check | podstawowa weryfikacja / sprawdzenie zdrowego rozsądku |
| handoff | przekazanie |
| half-step | pół kroku |
| trigger | wyzwalacz / trigger (toleruje się) |
| dashboard | panel / dashboard (toleruje się — zakorzenione) |
| optics | wizerunek / odbiór |
| haircut (= discount) | rabat / obcięcie |
| bookings | rezerwacje / zawarte kontrakty |
| onboarding | onboarding (OK — zakorzenione) / wdrożenie |
| post-mortem | post-mortem (industry term OK) |

**Zasada**: jeśli istnieje polskie słowo, które oddaje sens bez utraty precyzji, UŻYJ GO. v1 ciągnęła ku angielskiemu; reset.

## Anti-AI-tell po polsku — banned target-language moves

### Banned openings + meta

- "W niniejszym artykule..." / "W tym artykule przyjrzymy się"
- "Zanurzmy się w" / "Zagłębmy się w" / "Przejdźmy do"
- "Witamy w świecie X"
- "Warto zauważyć, że..." / "Warto wspomnieć, że" / "Należy podkreślić"
- "Jak zobaczymy" / "Jak zostanie pokazane poniżej"
- "W dzisiejszych czasach" / "W obecnych realiach"
- "Zachęcamy do" / "Zapraszamy do"

### Banned closers

- "Podsumowując" / "Na zakończenie" / "Kończąc"
- "Reasumując"
- "Mamy nadzieję, że ten artykuł był pomocny"

### Banned filler vocab (pl equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | pl forbidden |
|--------------|--------------|
| delve | zagłębiać się / zanurzać się (jako pusta retoryka) |
| tapestry | gobelin / mozaika (jako metafora) |
| landscape | krajobraz / pejzaż (jako filler — "obecny krajobraz") |
| realm | sfera / dziedzina (jako filler) |
| navigate (challenges) | nawigować (= radzić sobie) jako filler |
| robust | solidny / mocny (jako pusty intensifier) |
| leverage (verb) | wykorzystać / lewarować (jako filler) |

### Banned intensifiers

- "głęboko" / "niewiarygodnie" / "absolutnie" / "definitywnie" (puste)
- "naprawdę" / "rzeczywiście" (jako filler przed przymiotnikiem)

### Banned structural moves

- Tria "X, Y i Z" w każdym zdaniu
- "To nie tylko X — to Y" pivot
- Więcej niż 2 myślniki na akapit
- Zdanie zamykające w każdej sekcji
- Podtytuł co 200 słów
- Strona bierna gdy aktywna działa

## Prompt-callout translation policy

Artykuł zawiera bloki `<PromptCallout>`. Zasady:

- **Przedrostek `/faion` POZOSTAJE po angielsku** — to komenda.
- Wszystko PO `/faion` tłumaczy się na polski jako naturalne polecenie.
- Liczby, waluta, terminy z whitelist (MRR, burn, runway) verbatim.

Przykład:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- pl: `/faion policzmy mój runway: $50K oszczędności, $4K/mc burn, MRR $800`

Inne:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- pl: `/faion sprawdź PMF mojego solowego SaaSa według rubrica 5 kryteriów`

- EN: `/faion build me a 30-60-90 day plan`
- pl: `/faion zbuduj mi plan 30-60-90 dni`

## Receipt preservation (NEVER translate)

To są credentials autentyczności. Verbatim:

- **Imiona osób**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — oryginał.
- **Daty**: "March 2014" → "marzec 2014" OK (precyzja identyczna).
- **Kwoty w dolarach**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Nigdy "około 250 tysięcy".
- **Miejsca**: Bay Area, San Francisco, Lisbon — oryginał.
- **HN handles, Twitter handles, URLs**: verbatim.

Zasada: specyficzność czyni anegdotę unfalsifiable. Tłumaczenie "$250K" jako "około ćwierć miliona" zabija wiarygodność.

## Tone

- Direct, sharp. Polish humour OK gdy pasuje (polscy indie devs cenią suchą ironię).
- Polskie zdania mogą być dłuższe od EN ze względu na fleksję; zachować flow.
- Zdrobnienia — unikać dla tech content (brzmi protekcjonalnie).
- Diakrytyki — poprawne ą, ć, ę, ł, ń, ó, ś, ź, ż obowiązkowe. Żadnego "Polish-ascii".

## Grammatical attention

- Polski ma rodzaj w czasie przeszłym — pisać neutralnie gdzie się da, w przeciwnym wypadku używać 2. osoby ("zrobisz" zamiast "zrobiłem").
- Zgodność przypadków (mianownik, biernik, dopełniacz itd.) — częsty błąd ESL tłumaczy.

## Cultural

- $ zachowany (US benchmarks).
- Polskie przykłady indie zalecane gdy zastępują generyczne (polscy indie SaaS founders, Bootstrapped Poland).
- Daty: "25 maja 2026" lub "2026-05-25" (ISO dla kontekstów technicznych).

## Reviewer checklist

- [ ] "ty" lub "Pan/Pani" konsekwentnie (zgodnie z briefem).
- [ ] Diakrytyki poprawne wszędzie.
- [ ] Brak "W niniejszym artykule" / "Zachęcamy do" / "Warto zauważyć" filler.
- [ ] Brak "robić sens" calque.
- [ ] V2: wszystkie słowa z listy TRANSLATE przetłumaczone (feature, workflow, ship, deploy, burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist zachowany (CLI, MRR, runway, churn, framework, stack, brands, US tax).
- [ ] Anti-AI-tell: żadne "zanurzmy się / warto zauważyć / podsumowując".
- [ ] Receipts (imiona, daty, $, miejsca) verbatim.
- [ ] Prompt-callouts: `/faion` EN, treść naturalna po polsku.
- [ ] Slugi metodologii verbatim.
- [ ] Rodzaj w czasie przeszłym obsłużony (neutralnie lub 2. osoba).
- [ ] No emojis.
- [ ] Voice = direct + sharp + dry.
