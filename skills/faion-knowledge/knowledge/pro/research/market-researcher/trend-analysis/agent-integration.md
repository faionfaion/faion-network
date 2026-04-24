# Agent Integration — Trend Analysis (Market Researcher)

> Sister file: `pro/research/researcher/trend-analysis/agent-integration.md` covers the
> generalist signal-collection pipeline (HN, Product Hunt, GitHub, Google Trends).
> This file focuses on the **market-researcher angle**: industry analyst reports,
> macroeconomic indicators, and regulatory shifts that move whole-market structure.

## When to use
- Pre-investment / vertical-selection: deciding to enter a regulated category (fintech, health, crypto, energy, AI infra) where the policy clock dominates the product clock.
- Annual strategic planning: mapping CAGR + concentration + regulatory pipeline against a 3-year revenue plan.
- M&A / partnership scan: spotting that an incumbent's moat is eroding because a new EU/US rule is opening the market.
- Repricing existing offer: macro shift (rates, FX, energy, labour cost) moves customer willingness-to-pay; trend report grounds the new tier.
- Investor / board memo: the methodology produces the "market context" slide with cited Gartner/IDC/IMF rows, not vibes.

## When NOT to use
- Pure dev-tool / open-source category trends — researcher variant (HN/PH/GitHub) is faster and cheaper there.
- Day-to-day content topic ranking — analyst-report cadence is quarterly, not weekly.
- Pre-revenue idea screening — at idea stage, customer interviews beat IDC reports.
- Narrow local-language B2B niches — Gartner/Forrester rarely cover < $500M segments outside US/EU.
- When the goal is "find the next viral product" — analyst reports are explicitly lagging; TikTok/Reddit are the right inputs.

## Where it fails / limitations
- **Analyst-report lag.** Gartner Hype Cycle, Forrester Wave, IDC MarketScape trail real inflection by 12-24 months; treat them as confirming evidence, not leading.
- **Definition drift.** Two reports on "AI agents" may use incompatible TAM definitions (one counts API revenue, another counts seats); never sum across vendors.
- **Paywalled primary sources.** Most McKinsey/BCG/Bain reports the agent finds are summaries of summaries — actual numbers behind login. Cite the original PDF or mark as "secondary".
- **Regulatory-pipeline blindness.** EU AI Act, MiCA, DMA, GDPR-2 reshape markets before any KPI moves; a trend pipeline that only watches metrics misses the inflection.
- **Macro-decoupling.** A category's CAGR can rise while the macro (rates, FX, GDP) drags the addressable buyer count down — STEEP without quant macro overlay misses this.
- **Survivorship in vendor lists.** Magic Quadrants drop dead vendors silently; longitudinal "share of voice" must be computed across multiple report years to spot exits.
- **LLM stat fabrication.** "The X market is projected to reach $Y by 202Z at A% CAGR" is the highest-confidence-lowest-grounding sentence an LLM produces. Force source URL + page number on every numeric row.
- **Translation noise.** Non-English regulatory texts (EU directives, China MIIT, UA НКЦПФР) are routinely mis-summarised by agents; pin a `lang=en|orig` field and prefer official translations.

## Agentic workflow
Run as a quarterly cycle, not on demand. The orchestrator splits into four parallel collectors: (1) **macro-collector** pulls IMF/World Bank/OECD/central-bank series via FRED-style APIs; (2) **analyst-report collector** ingests PDFs/HTML from Gartner/Forrester/IDC/McKinsey/BCG/CB Insights/Statista (where licensed) plus free reprints; (3) **regulatory collector** watches EUR-Lex, US Federal Register, FCA/SEC/FTC, SEC EDGAR 10-K risk-factor diffs, plus per-jurisdiction trackers; (4) **incumbent-momentum collector** pulls 10-K/10-Q segment revenue, hiring deltas (LinkedIn / BuiltIn), and earnings-call transcripts. A `synthesizer` agent normalises into the STEEP grid with explicit macro and regulatory cells, a `quant-validator` reconciles overlapping market-size claims into a single sourced range, and a `regulatory-impact-scorer` translates rule changes into a stage-shift signal (will this push the trend earlier/later, or kill it). Every numeric cell must carry `{value, unit, year, source_url, source_type, page}`.

### Recommended subagents
- `faion-market-researcher-agent` — primary orchestrator; owns the STEEP+score+regulatory rubric and the final memo.
- `faion-research-agent` (mode: `market` / `competitors`) — dispatches the four-collector fan-out; handles output file writing to `.aidocs/product_docs/market-research.md`.
- `analyst-report-extractor` (sonnet, long-context) — parses PDF reports, returns `{market_size, cagr, segment, year, source_page}` rows only.
- `regulatory-watch-agent` (sonnet) — monitors EUR-Lex / Federal Register / SEC RSS; outputs `{rule_id, jurisdiction, stage:proposal|enacted|in_force, effective_date, market_impact}`.
- `macro-collector` (haiku) — pulls FRED / World Bank / Eurostat series; returns time-series JSON, no narrative.
- `quant-validator` (sonnet) — reconciles conflicting CAGR / TAM claims, computes range and confidence, refuses single-source rows.
- `counter-signal-critic` (sonnet) — searches for downward macro indicators, regulatory blockers, prior-cycle failures.
- `personal-fit-scorer` (haiku) — applies operator's capital, jurisdiction, and licence constraints (e.g., "we cannot serve EU regulated entities") before recommendation.

### Prompt pattern
```
You are the macro-trend orchestrator for trend "{TREND}" in markets {MARKETS}.
Output ONLY this JSON. Reject any row missing source_url + year.
{
  "trend": "...",
  "category": "fad|trend|megatrend|shift",
  "stage": "innovator|early|mainstream|decline",
  "market_size": [{"segment":"","tam_usd":0,"cagr_pct":0,"year":0,"source_url":"","source_type":"gartner|idc|forrester|mckinsey|statista|10k|other","page":0,"confidence":"high|med|low"}],
  "macro": [{"indicator":"","value":0,"unit":"","yoy_pct":0,"region":"","source_url":""}],
  "regulatory": [{"rule_id":"","jurisdiction":"","stage":"proposal|enacted|in_force","effective_date":"","market_impact":"accelerator|drag|killer|neutral","source_url":""}],
  "incumbents": [{"name":"","segment_share_pct":0,"yoy_revenue_pct":0,"hiring_delta_90d":0,"source_url":""}],
  "steep": {"social":"","tech":"","econ":"","env":"","political":""},
  "score": {"growth":1-5,"stage":1-5,"concentration":1-5,"regulatory_clarity":1-5,"macro_tailwind":1-5,"fit":1-5,"weighted":0-5},
  "counter_signals": ["..."],
  "recommendation": "pursue|monitor|skip",
  "next_review": "YYYY-MM-DD"
}
```

```
You are the regulatory-impact scorer. Given trend "{TREND}", jurisdictions {JURIS},
and the current rule pipeline, classify each rule's effect on market structure:
- accelerator: rule expands addressable demand or removes incumbent moat
- drag: rule increases compliance cost but does not block entry
- killer: rule effectively bans the practice or imposes prohibitive cost
- neutral: cosmetic
Return JSON rows with rule_id, effective_date, classification, and 1-sentence rationale citing the rule's article number.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fredapi` | St. Louis Fed FRED macro series (rates, GDP, CPI, employment) | `pip install fredapi`; key at fred.stlouisfed.org |
| `wbdata` / `wbgapi` | World Bank indicators by country/series | `pip install wbgapi` |
| `eurostat` (R / Python `eurostat`) | EU statistical office, 9000+ series | `pip install eurostat` |
| `oecd` (SDMX) | OECD macro + sector series via SDMX | `pip install pandasdmx` |
| `pyimf` / SDMX | IMF WEO / IFS macro series | imf.org/external/datamapper/api |
| `eur-lex` API | EU regulation full-text + metadata | eur-lex.europa.eu/content/help/data-reuse/webservice.html |
| `federalregister-api` | US proposed/final rules with full diff | federalregister.gov/developers |
| `sec-edgar-downloader` | 10-K / 10-Q / 8-K filings, risk-factor diffs | `pip install sec-edgar-downloader` |
| `secedgar` (rank-and-filed) | EDGAR full-text search, segment revenue extraction | github.com/coyo-ai/secedgar |
| `regulations.gov` API | US comment-period public dockets | api.regulations.gov |
| `gov.uk` Find a Regulation | UK rule tracker | api.gov.uk |
| `crunchbase` REST API | Funding-round signal for incumbent momentum | data.crunchbase.com |
| `pitchbook` API (paid) | Late-stage / private comps, transactions | pitchbook.com/api |
| `cbinsights` (paid) | Industry deep-dives, market maps | cbinsights.com/research |
| `statista` API (enterprise) | Pre-built market-size charts with citation | statista.com/api |
| `ourworldindata` (CSV mirrors) | Open macro + climate + health series | ourworldindata.org |
| `tavily` / `exa` / `perplexity` API | Cited LLM search; ideal for analyst-report grounding | docs.tavily.com / exa.ai / docs.perplexity.ai |
| `WebFetch` (Claude Code) | Native PDF / HTML pull for analyst reports | Claude Code built-in |
| `pdfplumber` / `unstructured` | Extract tables from analyst PDFs | `pip install pdfplumber unstructured` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Gartner | Paid analyst | PDF + entitlement-gated API | Magic Quadrant, Hype Cycle — authoritative, lagging |
| Forrester | Paid analyst | PDF + Wave reports | Best for B2B SaaS quadrants |
| IDC | Paid analyst | API on enterprise tier | Strongest for hardware / IT spend |
| McKinsey / BCG / Bain | Free summaries + paid full | Public PDFs reusable | Treat as directional, never primary stats |
| CB Insights | Paid | Reports + API | Funding + market maps + earnings-call NLP |
| Statista | Paid | API on enterprise | Pre-charted market sizes; cite original where possible |
| PitchBook | Enterprise | Yes | Deal flow + private comps |
| S&P Capital IQ | Enterprise | Yes | Industry classifications + financials |
| FRED (St. Louis Fed) | Free | Yes (key) | US + global macro time series |
| World Bank Open Data | Free | Yes | Country-level series, GNI, governance |
| Eurostat | Free | Yes (REST/SDMX) | EU sector + labour + trade |
| OECD.Stat | Free | Yes (SDMX) | Cross-country macro + tax |
| IMF Data | Free | Yes | WEO, IFS, FSI |
| EUR-Lex | Free | Yes | EU regulation full-text + status |
| Federal Register | Free | Yes | US proposed + final rules + comments |
| SEC EDGAR | Free | Yes | 10-K/Q/8-K, segment revenue, risk factors |
| Regulations.gov | Free | Yes | US dockets and public comments |
| Companies House (UK) | Free | Yes | UK filings |
| Bundesanzeiger (DE) | Free | Limited | German official journal |
| Crunchbase | Paid | Yes | Funding + acquisition + headcount |
| LinkedIn Talent Insights | Paid | Scraper-only on free | Hiring trend by skill / company / geo |
| BuiltWith | Paid | Yes | Tech-stack adoption — incumbent moat erosion |
| AlphaSense | Paid | Yes | Earnings-call + filings NLP search |
| Sentieo / Aiera | Paid | Yes | Transcript + filings semantic search |

## Templates & scripts
See the existing `templates.md` (Trend Report + Monthly Dashboard). Inline a market-structure-focused collector that adds macro + regulatory rows on top of the researcher-variant signals:

```python
# market_trend_signals.py — macro + regulatory + filings collector (~45 lines)
import os, json, datetime as dt, requests
from fredapi import Fred

FRED = Fred(api_key=os.environ["FRED_API_KEY"])

def macro(series_ids: list[str]) -> list[dict]:
    out = []
    for sid in series_ids:
        s = FRED.get_series(sid).dropna()
        if s.empty: continue
        last, prev = s.iloc[-1], s.iloc[-13] if len(s) > 13 else s.iloc[0]
        yoy = None if prev == 0 else round((last - prev) / prev * 100, 2)
        out.append({"series": sid, "last": float(last), "yoy_pct": yoy,
                    "source_url": f"https://fred.stlouisfed.org/series/{sid}"})
    return out

def federal_register(term: str, days: int = 90) -> list[dict]:
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    r = requests.get("https://www.federalregister.gov/api/v1/documents",
                     params={"conditions[term]": term,
                             "conditions[publication_date][gte]": since,
                             "per_page": 20}).json()
    return [{"rule_id": d["document_number"], "title": d["title"],
             "stage": d["type"], "effective_date": d.get("effective_on"),
             "source_url": d["html_url"]} for d in r.get("results", [])]

def eur_lex(term: str) -> list[dict]:
    # public SOAP endpoint omitted; use search HTML as fallback
    r = requests.get("https://eur-lex.europa.eu/search.html",
                     params={"qid": "1", "text": term, "scope": "EURLEX",
                             "type": "quick", "DTS_DOM": "EU_LAW"}).text
    return [{"source_url": "https://eur-lex.europa.eu/", "term": term,
             "raw_html_bytes": len(r)}]  # downstream parser extracts CELEX ids

def collect(term: str, fred_series: list[str]) -> dict:
    return {"term": term, "ts": dt.datetime.utcnow().isoformat(),
            "macro": macro(fred_series),
            "regulatory_us": federal_register(term),
            "regulatory_eu": eur_lex(term)}

if __name__ == "__main__":
    import sys
    print(json.dumps(collect(sys.argv[1], sys.argv[2].split(",")), indent=2))
```

## Best practices
- **Triangulate market size from ≥3 sources before publishing a number.** Single-source TAMs are the #1 reason investor memos fall apart; record range + confidence, not a point estimate.
- **Track regulatory pipeline as a separate axis from STEEP-Political.** Stage (proposal / enacted / in-force) and effective_date drive the entry-window decision more than CAGR.
- **Diff 10-K risk factors year-over-year for incumbents.** New language about a trend in risk factors is the strongest cheap signal that incumbents fear it.
- **Pin source_type on every row.** Primary (vendor 10-K, regulator) > Tier-1 analyst (Gartner/IDC) > Tier-2 (Statista summary) > Press. Score rows by tier when reconciling.
- **Use earnings-call transcripts for stage timing.** Go from "we are evaluating" → "we are piloting" → "we are deploying at scale" across calls is the cleanest stage indicator available.
- **Maintain a regulatory calendar memory file.** Effective dates for EU AI Act / MiCA / DSA obligations move every 6 months; cache the schedule and re-poll quarterly.
- **Currency- and inflation-normalise.** A "$10B → $25B by 2030" row in nominal dollars at 4% inflation collapses to $20B real; deflate before comparing across reports.
- **Personal-fit filter must include licensing.** A regulated category (broker-dealer, healthcare, gambling) with great trend strength is unreachable without licences — gate on this before scoring.
- **Two-quarter sanity gap on regulatory shifts.** Never pivot the company on a proposed rule; wait for enacted-or-better stage.

## AI-agent gotchas
- **Numeric hallucination at scale.** Analyst-report parsing is the #1 source of fake CAGRs. Force `{value, unit, year, page, source_url}` schema; reject any row without a page number when the source is a PDF.
- **Stale training-data masquerading as "current report".** Without WebFetch, the agent will cite a 2022 Gartner Hype Cycle as "this year's"; always check `current_date` against `report_publish_date`.
- **Definition collisions.** Agent silently sums incompatible TAMs ("AI software" + "AI services" + "AI hardware") into a triple-counted number. Require segment definitions to be quoted verbatim from each source.
- **Regulatory-stage confusion.** Agents conflate "introduced", "passed committee", "enacted", "in force" — pin the explicit stage enum and require the relevant article/section reference.
- **Single-jurisdiction blind spot.** Defaults to US sources; the EU rule pipeline often leads. Force a `jurisdictions` list in the orchestrator prompt.
- **Currency-and-unit drift.** "$2B" vs "EUR 2 bn" vs "₩2조" vs "$2 trillion" — normalize at collector layer with explicit `unit` field.
- **Earnings-call cherry-picking.** LLMs surface only the bullish quote. Require a balanced sample: top-3 positive + top-3 cautionary mentions per call.
- **Counter-signal omission.** Default tone is bullish; mandate the counter-signal critic and reject any final report missing ≥3 cooling indicators.
- **Token blowup on PDFs.** Never feed a 200-page McKinsey report to the synthesizer. Use `pdfplumber` to extract only the tables + executive summary first.
- **Rate-limit / paywall masquerade.** When Gartner blocks an extractor, the agent often returns a generic LLM hallucination instead of an error. Surface "blocked-by-paywall" as a hard failure, not silent degradation.
- **Geographic mis-attribution.** "EU growth" reports often quote EU+UK or EU+EFTA; require explicit country list in every regional row.

## References
- https://fred.stlouisfed.org/docs/api/fred/ — FRED API for macro series.
- https://data.worldbank.org/ — World Bank indicators.
- https://ec.europa.eu/eurostat — Eurostat statistics.
- https://stats.oecd.org/ — OECD.Stat (SDMX).
- https://eur-lex.europa.eu/ — EU legal framework full-text + status.
- https://www.federalregister.gov/developers/api/v1 — US Federal Register API.
- https://www.sec.gov/edgar/sec-api-documentation — SEC EDGAR data.
- https://www.gartner.com/en/research/methodologies/gartner-hype-cycle — Hype Cycle methodology.
- https://www.forrester.com/policies/forrester-wave-methodology/ — Forrester Wave methodology.
- https://www.idc.com/research/marketscape — IDC MarketScape.
- https://www.cbinsights.com/research/ — CB Insights market maps + reports.
- https://www.statista.com/aboutus/our-research-commitment — Statista methodology + sourcing.
- https://www.imf.org/en/Publications/WEO — IMF WEO macro forecasts.
- https://www.bis.org/statistics/ — BIS cross-border banking + FX.
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai — EU AI Act tracker.
- https://www.esma.europa.eu/policy-activities/mica — MiCA tracker.
- https://corpgov.law.harvard.edu/ — Harvard governance forum (10-K risk-factor analyses).
