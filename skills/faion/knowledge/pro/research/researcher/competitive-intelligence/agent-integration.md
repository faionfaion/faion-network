# Agent Integration — Competitive Intelligence

## When to use
- Live B2B/SaaS market where competitors ship weekly and pricing changes often.
- Sales team needs current battlecards (deal cycle > 30 days exposes stale data fast).
- Product roadmap decisions blocked on feature parity or differentiation gaps.
- Funding round, M&A, or executive hire signals need to surface within 24h.
- You already have 3+ named direct competitors plus stable URLs to track.

## When NOT to use
- Pre-PMF or category-creation phase — competitors are not the bottleneck, customer interviews are.
- < 5 known competitors — manual quarterly snapshot beats infrastructure overhead.
- Highly regulated/closed markets (defense, sealed bids) where public signals are noise.
- Personal projects with no GTM motion — output has no consumer.
- When the team will not act on alerts (CI without a sales/product action loop is theater).

## Where it fails / limitations
- Hallucinated synthesis: LLMs invent competitor features when scraped page is paywalled or JS-rendered and returns empty body. Always require source citation per claim.
- Pricing pages hidden behind "Contact Sales" — daily monitors generate false silence; cross-check G2/Capterra and customer reviews instead.
- Translation drift in non-English markets — Crayon/Klue auto-translate loses nuance; use Valona for multilingual.
- Regulatory limits: scraping LinkedIn at scale violates ToS; LinkedIn API is gated. Use Phantombuster/Apify with proxy rotation and honor robots.txt or pay for Crunchbase/AlphaSense API.
- Survivorship bias in win-rate claims (16% → 45%) — usually conflates CI rollout with sales enablement and pricing changes.
- Battlecard rot: 2-week-old battlecard with confident tone is worse than no battlecard. TTL must be enforced.

## Agentic workflow
Run a daily collector agent that pulls deltas from website, pricing, hiring, reviews, news, and social into a normalized event store. A weekly synthesizer agent clusters events per competitor, scores threat (low/med/high), and writes a digest. A sales-facing battlecard agent regenerates per-competitor cards on every high-severity event so reps always pull fresh from CRM/Slack. Keep humans in the loop on threat scoring and any claim that mentions a named customer.

### Recommended subagents
- `ci-collector` — Haiku. Polls a YAML watchlist (URLs, keywords, RSS, review sites). Emits normalized JSON events. No reasoning, no synthesis.
- `ci-classifier` — Haiku/Sonnet. Tags each event: pricing | feature | hire | funding | review | content. Discards noise.
- `ci-synthesizer` — Sonnet. Clusters week-of events per competitor, drafts digest with cited sources.
- `ci-threat-analyst` — Opus. Generates threat assessment, "so what" recommendations, scenario planning. Run weekly or on funding/M&A signals.
- `ci-battlecard-writer` — Sonnet. Regenerates per-competitor battlecards from latest digest + win/loss notes. Output to Salesforce, Highspot, or Slack.
- `ci-fact-checker` — Sonnet. Adversarial pass: every claim must cite a fetched URL with a date; flags unsupported claims.

### Prompt pattern
Collector (XML, structured output):
```
<task>collect</task>
<watchlist>{{ yaml_watchlist }}</watchlist>
<since>{{ last_run_iso }}</since>
<output_schema>{events:[{competitor,signal_type,url,fetched_at,raw_excerpt,delta_summary}]}</output_schema>
<rules>NO inference. NO summarization beyond delta. If page unreachable, emit error event.</rules>
```

Threat analyst (XML):
```
<role>CI threat analyst</role>
<digest>{{ weekly_digest }}</digest>
<our_positioning>{{ positioning_md }}</our_positioning>
<deliverable>threat_score (1-5), evidence (>=3 cited events), recommended_action, decision_owner</deliverable>
<constraint>Cite event_id for every factual claim. If evidence < 3, return INSUFFICIENT_DATA.</constraint>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `crayon` API | Battlecards, signals, intel digests | crayon.co/api (enterprise contract) |
| `klue` API | Win/loss, battlecards, distribution | klue.com/developers |
| `kompyte` (Semrush) API | Real-time site change tracking | semrush.com/kompyte |
| `crunchbase` API | Funding, M&A, leadership | data.crunchbase.com (paid) |
| `alphasense` API | Filings, transcripts, expert calls | alpha-sense.com/api (enterprise) |
| `ahrefs` / `semrush` API | SEO/SEM moves, top pages, keyword shifts | ahrefs.com/api, semrush.com/api |
| `g2` Buyer Intent API | Review velocity, intent signals | g2.com/products/api |
| `apify` actors | Headless scrape (G2, LinkedIn, Product Hunt) | apify.com (pay-per-run) |
| `firecrawl` / `jina reader` | LLM-ready page extraction with JS render | firecrawl.dev, r.jina.ai |
| `visualping` | Diff alerts on rendered pages | visualping.io (webhook) |
| `phantombuster` | LinkedIn hiring/post phantoms | phantombuster.com |
| `rss-parser` (npm) / `feedparser` (py) | Newsroom + blog ingestion | trivial install |
| `playwright` | Custom JS-rendered scrape when API gaps | playwright.dev |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Crayon | CI suite | Partial — REST API | Battlecard auto-update. Closed taxonomy. |
| Klue | CI suite | Partial — REST API | Strong distribution to Salesforce/Slack. |
| Contify Athena | Agentic CI | Native agent layer | 2025 release; unstructured-content reasoning. |
| AlphaSense | Multi-source intel | Yes — API + summaries | Filings/transcripts; expensive. |
| Kompyte (Semrush) | Real-time tracker | Yes — webhook + API | Best for site/SEO deltas at scale. |
| Valona Intelligence | Multilingual CI | Limited API | Useful for EU/APAC competitors. |
| Visualping | Page diff | Yes — webhook | Cheap; raw signal, no synthesis. |
| Crunchbase | Firmographic DB | Yes — REST | Funding/M&A truth source. |
| G2 / Capterra | Reviews | G2 has API; Capterra scrape-only | Customer-voice signal. |
| Product Hunt | Launch radar | Yes — GraphQL API | Daily competitor/category launches. |
| LinkedIn (Sales Nav) | Hiring/people | Hostile to bots | Use Phantombuster/Bright Data, respect ToS. |
| Apollo / ZoomInfo | Org charts, hiring | Yes — API | Detect new VPs, sales team scaling. |
| Owler | Light CI | RSS-grade API | Good free signal layer. |
| BuiltWith / Wappalyzer | Tech stack | Yes — API | Detect infra/SaaS migrations. |
| App Annie / Sensor Tower | Mobile intel | Yes — API | If mobile competitor. |

## Templates & scripts
Inline collector loop (Python, Claude Agent SDK style, < 50 lines):

```python
# ci_collector.py — schedule via cron hourly
import json, hashlib, pathlib, datetime, httpx, yaml

WATCH = yaml.safe_load(open("watchlist.yaml"))
STATE = pathlib.Path(".ci_state"); STATE.mkdir(exist_ok=True)
EVENTS = pathlib.Path("events.ndjson")

def fetch(url: str) -> str:
    r = httpx.get(f"https://r.jina.ai/{url}", timeout=30)  # LLM-ready extract
    r.raise_for_status()
    return r.text

def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def emit(event: dict):
    event["ts"] = datetime.datetime.utcnow().isoformat() + "Z"
    with EVENTS.open("a") as f:
        f.write(json.dumps(event) + "\n")

for competitor in WATCH["competitors"]:
    for url in competitor["urls"]:
        try:
            body = fetch(url)
        except Exception as e:
            emit({"competitor": competitor["name"], "url": url, "error": str(e)})
            continue
        fp_path = STATE / hashlib.md5(url.encode()).hexdigest()
        prev = fp_path.read_text() if fp_path.exists() else ""
        cur = fingerprint(body)
        if cur != prev:
            emit({"competitor": competitor["name"], "url": url,
                  "signal_type": competitor.get("type", "site"),
                  "excerpt": body[:2000]})
            fp_path.write_text(cur)
```

`watchlist.yaml` is the only file humans edit. The synthesizer/threat-analyst read `events.ndjson` once per cycle.

## Best practices
- One event per delta, never aggregate inside the collector — keeps the audit trail clean.
- Force every LLM claim to carry an `event_id` reference; reject digests that fail the fact-checker pass.
- Calibrate threat scores against actual lost deals quarterly; recalibrate the prompt if score doesn't predict losses.
- Battlecard TTL ≤ 14 days. Stamp generation date prominently; sales reps trust dated artifacts.
- Separate "what changed" (Haiku, mechanical) from "so what" (Opus, judgment). Mixing them costs 10x and adds hallucination.
- Subscribe to competitor changelog/RSS first; scraping is the fallback. APIs > RSS > scrape > screenshot diff.
- Track yourself with the same pipeline. Catches what your own marketing site exposes to competitors.
- Keep a "do-not-track" list (legal, ex-employees, personal blogs) to avoid ToS and ethical issues.
- Run win/loss interviews monthly and feed transcripts back into battlecard prompts — review-site sentiment alone is a lagging indicator.

## AI-agent gotchas
- Empty-body trap: JS-rendered SPAs return shells; agent reports "no change" forever. Mitigation: Firecrawl/Jina reader or Playwright; alert on body-length variance > 80%.
- Cookie/paywall: SaaS pricing pages 302-redirect to login. Treat 30x/40x as a signal, not silence.
- Translation noise: site i18n switches based on geo IP; pin the locale via header to prevent fake "site-redesign" alarms.
- Citation hallucination: model invents URL `/pricing/enterprise` that never existed. Fact-checker must HEAD the URL before publishing.
- Recency bias: weekly digest over-weights last 2 days. Normalize event volume per day before clustering.
- Compounded summarization: digest-of-digest-of-digest loses the "so what". Always re-ground synthesizer prompts on raw events, not previous digests.
- Stop-words in change detection: HTML diff catches CSS/build-hash churn. Strip script/style tags and timestamps before fingerprinting.
- Rate limits + retries: agent loops on 429 burning tokens. Wrap fetches with exponential backoff and a circuit breaker.
- LinkedIn ToS: scraping can get the company account banned. Route through compliant providers; never use a personal cookie.
- Internal politics: a "high threat" assessment naming a partner can blow up deals. Add a redaction step + named-entity allowlist before distribution.
- Confirmation bias prompts: "Is competitor X a threat?" yields yes. Use neutral framing: "Score evidence-based threat 1-5; default 1".

## References
- https://www.crayon.co/blog/competitive-intelligence-best-practices
- https://klue.com/blog/competitive-enablement
- https://www.contify.com/athena (Agentic CI engine, 2025)
- https://www.alpha-sense.com/resources (multi-source intel)
- https://www.semrush.com/kompyte/
- https://www.firecrawl.dev/ (LLM-ready scrape)
- https://r.jina.ai (reader API)
- https://docs.apify.com (actors for G2/PH/LinkedIn)
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://www.g2.com/products/api/documentation
- https://data.crunchbase.com/docs
- https://www.product-hunt.com/v2/docs (GraphQL)
