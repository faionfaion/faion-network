# Portuguese (pt) translation rules

Default variant: **Brazilian Portuguese (pt-BR)**. Confirm via brief if European Portuguese requested. **V4 doctrine — translate by default; tight English whitelist; cultural adaptation licence for body + headings; English-idiom accuracy; reading-register tilt to native target-language tech-writing. See `phase2-translate.md` and `style-guide.md` for the full v4 contract.**

## Voice transfer

- Confident, direct, sharp. Brazilian tech-blog voice (TabNews, indie devs on Twitter).
- "Você" as default address; never "tu" (regional). Drop the formal "o senhor / a senhora".
- Irony preserved. Calques + corporate-PT register removed.

## Address register

Default: **você** (singular, informal-neutral). "vocês" para plural. Nunca "tu/vós" (regional pt-PT). Nunca "o senhor".

## Banned (calques from English)

| EN calque | pt-BR correct |
|-----------|---------------|
| "endereçar um problema" | "abordar / resolver um problema" |
| "no final do dia" | "no fim das contas" |
| "no longo prazo" | "a longo prazo" |
| "alavancar" (= leverage as verb) | reescrever — corporate calque |
| "entregáveis" | "entregas" ou substantivo específico |
| "fazer sentido" (overuse) | OK em pt — checar repetição |
| "acionável" | "prático" / "concreto" |
| "stackholder" | "stakeholder" (keep English) |

## V2 anglicism policy — translate by default

A lista de coisas mantidas em inglês é APERTADA. O resto traduz.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Industry acronyms — no pt equivalent |
| runway, churn, burn rate | SaaS metrics — convenção da comunidade indie |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — no pt equivalent |
| slug-format, file paths, command names, code blocks | Verbatim |

### TRANSLATE (V2 — old practice kept too much English)

| English | pt-BR target |
|---------|--------------|
| feature | recurso / funcionalidade |
| workflow | fluxo de trabalho / processo |
| pattern | padrão |
| ship (verb) | lançar / publicar |
| deploy (verb) | implantar / fazer deploy (slang OK no voice) |
| burnout | esgotamento (preferido) — "burnout" tolerado mas reescrever quando possível |
| pivot (noun/verb) | virada / pivotar (verbo prijatelj OK) |
| brokerage | corretora |
| moonshot | aposta ambiciosa / tiro de longo alcance |
| sanity check | verificação básica / sanity check (tolerado, mas reescrever) |
| handoff | passagem / repasse |
| half-step | meio passo |
| trigger | gatilho |
| dashboard | painel / dashboard (OK — instalado) |
| optics | aparência / percepção |
| haircut (= discount) | corte / desconto |
| bookings | reservas / contratos fechados |
| framework | framework (OK — instalado) |
| stack | stack (OK — instalado) |
| onboarding | onboarding (OK — instalado) ou integração |
| post-mortem | post-mortem (industry term OK) |

**Regra**: se existe palavra pt que captura o sentido sem perda, USE. v1 errava para o inglês; reset.

## Anti-AI-tell em pt — banned target-language moves

### Banned openings + meta

- "Neste artigo vamos..." / "Neste artigo exploraremos"
- "Vamos explorar" / "Vamos mergulhar" / "Vamos desbravar"
- "Bem-vindo ao mundo de X" / "No mundo de hoje"
- "É importante notar que..." / "É importante destacar"
- "Como veremos a seguir" / "Como será mostrado abaixo"
- "Atualmente, no cenário..." / "Nos dias atuais"
- "Vale a pena mencionar"

### Banned closers

- "Em conclusão" / "Concluindo" / "Para concluir"
- "Em resumo" / "Resumindo"
- "Esperamos que este artigo tenha sido útil"

### Banned filler vocab (pt-BR equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | pt forbidden |
|--------------|--------------|
| delve | mergulhar / aprofundar-se (como retórica) |
| tapestry | tapeçaria / mosaico (metáfora) |
| landscape | cenário / panorama (como filler — "o cenário atual") |
| realm | esfera / âmbito / domínio (filler) |
| navigate (challenges) | navegar (= enfrentar) / orientar-se |
| robust | robusto (como intensificador vazio) |
| leverage (verb) | alavancar (calque proibido) |

### Banned intensifiers

- "profundamente" / "incrivelmente" / "absolutamente" / "definitivamente" (esvaziados)
- "verdadeiramente" / "realmente" (como filler antes de adjetivo)

### Banned structural moves

- Trios "X, Y e Z" em cada frase
- "Não é só X — é Y" pivot
- Mais que 2 travessões por parágrafo
- Frase de fechamento em cada seção
- Subtítulo a cada 200 palavras

## Prompt-callout translation policy

Artigo contém blocos `<PromptCallout>`. Regras:

- **Prefixo `/faion` PERMANECE em inglês** — é comando.
- Tudo APÓS `/faion` traduz para pt-BR como pedido natural.
- Números, moeda, termos do whitelist (MRR, burn, runway) ficam verbatim.

Exemplo:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- pt-BR: `/faion vamos calcular meu runway: $50K em economias, burn $4K/mês, MRR $800`

Outros:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- pt-BR: `/faion verifica o PMF do meu SaaS solo pelo rubric de 5 critérios`

- EN: `/faion build me a 30-60-90 day plan`
- pt-BR: `/faion monta pra mim um plano de 30-60-90 dias`

## Receipt preservation (NEVER translate)

São credenciais de autenticidade. Verbatim:

- **Nomes de pessoas**: Patrick McKenzie, Pieter Levels, Sahil Lavingia, Tobias Lütke — original.
- **Datas**: "March 2014" → "março de 2014" OK (número idêntico); manter precisão.
- **Dólares**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Nunca "uns 250 mil".
- **Lugares**: Bay Area, San Francisco, Lisbon — original.
- **HN handles, Twitter handles, URLs**: verbatim.

Princípio: especificidade torna a anedota unfalsifiable. Traduzir "$250K" como "cerca de duzentos e cinquenta mil" mata a credibilidade.

## Tone

- Brazilian register: warm but direct. Não corporate.
- "A gente" sparingly (informal); "nós" para nós-plural quando preciso.
- Frases mais curtas que no EN. Quebrar compostas EN em 2 pt-BR.

## Cultural

- $ kept (US benchmarks).
- Exemplos indie brasileiros encorajados quando substituem genéricos (founders brasileiros indie SaaS relevantes).
- Datas: "2026-05-25" ou "25 de maio de 2026".

## Reviewer checklist

- [ ] Sem "o senhor" formal.
- [ ] Sem calques corporate ("alavancar", "endereçar", "acionável").
- [ ] V2: todas as palavras da lista TRANSLATE traduzidas (feature, workflow, ship, deploy, burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist preservado (CLI, MRR, runway, churn, brands, US tax).
- [ ] Anti-AI-tell: nenhum "neste artigo / vamos explorar / é importante notar / em conclusão".
- [ ] Receipts (nomes, datas, $, lugares) verbatim.
- [ ] Prompt-callouts: `/faion` EN, corpo natural em pt-BR.
- [ ] Slugs de metodologias verbatim.
- [ ] No emojis.
- [ ] Voice = confident + direct.
