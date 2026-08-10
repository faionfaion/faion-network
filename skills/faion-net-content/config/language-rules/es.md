# Spanish (es) translation rules

Default variant: **Neutral Latin American Spanish**. Confirm via brief if European Spanish requested. **V4 doctrine — translate by default; tight English whitelist; cultural adaptation licence for body + headings; English-idiom accuracy; reading-register tilt to native target-language tech-writing. See `phase2-translate.md` and `style-guide.md` for the full v4 contract.**

## Voice transfer

- "Tú" as default address (informal, LatAm + younger Spain). Never "usted" for indie-tech audience.
- Confident, direct. Latin American tech-blog voice.
- Irony preserved. Corporate-ES filler banned.

## Address register

Default: **tú** (informal singular, neutro LatAm). "ustedes" para plural (LatAm). Evitar "vos" (Argentina/Uruguay — demasiado regional). Evitar "vosotros" (España — demasiado regional).

## Banned (calques + corporate-ES filler)

| EN calque | es correct |
|-----------|-----------|
| "hacer sentido" | "tener sentido" |
| "al final del día" | "al fin y al cabo" |
| "en el largo plazo" | "a largo plazo" |
| "accionable" (= actionable) | "práctico" / "concreto" |
| "entregables" (= deliverables) | sustantivo específico |
| "apalancar" (= leverage as verb) | reescribir — calque corporativo |
| "vamos a explorar" / "vamos a desentrañar" | banned — filler corporativo |
| "en este artículo veremos" | banned — meta vacío |

## V2 anglicism policy — translate by default

La lista de palabras conservadas en inglés es ESTRECHA. Lo demás se traduce.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Acrónimos sin equivalente es |
| runway, churn, burn rate | Métricas SaaS — convención comunitaria |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — sin equivalente |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — la v1 dejaba demasiado inglés)

| English | es target |
|---------|-----------|
| feature | característica / funcionalidad |
| workflow | flujo de trabajo / proceso |
| pattern | patrón |
| ship (verb) | lanzar / publicar |
| deploy (verb) | desplegar (preferido) / hacer deploy (jerga OK en voice) |
| burnout | agotamiento / desgaste |
| pivot (noun/verb) | giro / pivotar (verbo aceptado) |
| brokerage | corredora / cuenta de corretaje |
| moonshot | apuesta ambiciosa / tiro a la luna |
| sanity check | verificación básica / chequeo de sensatez |
| handoff | traspaso / entrega |
| half-step | medio paso |
| trigger | desencadenante / disparador / trigger (tolerado) |
| dashboard | panel / tablero (preferido) — "dashboard" tolerado |
| optics | percepción / apariencia |
| haircut (= discount) | recorte / descuento |
| bookings | reservas / contratos firmados |
| framework | framework (OK — instalado en jerga tech) |
| stack | stack (OK — instalado) |
| onboarding | onboarding (OK — instalado) / incorporación |
| post-mortem | post-mortem (industry term OK) / autopsia |

**Regla**: si existe palabra es que captura el sentido sin pérdida, ÚSALA. v1 erraba hacia inglés; reset.

## Anti-AI-tell en es — banned target-language moves

### Banned openings + meta

- "En este artículo veremos" / "En este artículo exploraremos"
- "Vamos a explorar" / "Vamos a sumergirnos" / "Vamos a desentrañar"
- "Bienvenido al mundo de X" / "En el mundo actual"
- "Es importante destacar que" / "Cabe destacar que" / "Vale la pena mencionar"
- "Como veremos a continuación"
- "Actualmente, en el panorama..."
- "Hoy en día"

### Banned closers

- "En conclusión" / "Para concluir" / "Concluyendo"
- "En resumen" / "Resumiendo"
- "Esperamos que este artículo te haya sido útil"

### Banned filler vocab (es equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | es forbidden |
|--------------|--------------|
| delve | profundizar / adentrarse (como retórica vacía) |
| tapestry | tapiz / mosaico (metáfora) |
| landscape | panorama / escenario (como filler — "el panorama actual") |
| realm | ámbito / esfera / reino (filler) |
| navigate (challenges) | navegar (= enfrentar) |
| robust | robusto (como intensificador vacío) |
| leverage (verb) | apalancar (calque prohibido) |

### Banned intensifiers

- "profundamente" / "increíblemente" / "absolutamente" / "definitivamente" (vacíos)
- "verdaderamente" / "realmente" (como filler ante adjetivo)

### Banned structural moves

- Tríos "X, Y y Z" en cada frase
- "No es solo X — es Y" pivot
- Más de 2 guiones largos por párrafo
- Frase de cierre en cada sección
- Subtítulo cada 200 palabras

## Prompt-callout translation policy

El artículo contiene bloques `<PromptCallout>`. Reglas:

- **Prefijo `/faion` PERMANECE en inglés** — es comando.
- Todo DESPUÉS de `/faion` se traduce al es como petición natural.
- Números, moneda, términos del whitelist (MRR, burn, runway) verbatim.

Ejemplo:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- es: `/faion calculemos mi runway: $50K en ahorros, $4K/mes de burn, MRR $800`

Otros:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- es: `/faion revisa el PMF de mi SaaS solo con el rubric de 5 criterios`

- EN: `/faion build me a 30-60-90 day plan`
- es: `/faion arma un plan de 30-60-90 días para mí`

## Receipt preservation (NEVER translate)

Son credenciales de autenticidad. Verbatim:

- **Nombres de personas**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — original.
- **Fechas**: "March 2014" → "marzo de 2014" OK (precisión idéntica).
- **Dólares**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Nunca "unos 250 mil".
- **Lugares**: Bay Area, San Francisco, Lisbon — original.
- **HN handles, Twitter handles, URLs**: verbatim.

Principio: la especificidad hace que la anécdota sea unfalsifiable. Traducir "$250K" como "alrededor de doscientos cincuenta mil" mata la credibilidad.

## Tone

- Directo + cálido. Evitar regionalismos LatAm que no viajan ("chévere", "padrísimo").
- Oraciones pueden ser ligeramente más largas que en EN; preservar el flujo.
- Blogs de referencia: Platzi, indie LatAm devs en Twitter.

## Cultural

- $ kept (benchmarks de US).
- Ejemplos indie LatAm encouraged cuando reemplazan los genéricos.
- Fechas: "2026-05-25" o "25 de mayo de 2026".

## Reviewer checklist

- [ ] Sin "usted" formal.
- [ ] Sin regionalismos ("chévere", "vos", "vosotros").
- [ ] Sin calques corporativos ("accionable", "apalancar").
- [ ] V2: todas las palabras de la lista TRANSLATE traducidas (feature, workflow, ship, deploy, burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist preservado (CLI, MRR, runway, churn, brands, US tax).
- [ ] Anti-AI-tell: nada de "en este artículo / vamos a explorar / es importante destacar / en conclusión".
- [ ] Receipts (nombres, fechas, $, lugares) verbatim.
- [ ] Prompt-callouts: `/faion` EN, cuerpo natural en es.
- [ ] Slugs de metodologías verbatim.
- [ ] No emojis.
- [ ] Voice = confident + direct + warm.
