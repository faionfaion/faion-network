# Agent Integration — Continuous Discovery (Market-Researcher Angle)

> Sibling `pro/research/researcher/continuous-discovery/agent-integration.md` covers the user-/product-discovery (Teresa Torres) angle. This file covers the market-researcher angle: rolling market scans, early-signal detection, continuous competitor + pricing monitoring.

## When to use

- A live category where competitors ship weekly (AI tooling, dev tools, fintech, creator SaaS) and a 6-month-old market map is already wrong.
- Pricing-sensitive segments (PLG SaaS, marketplaces) where competitor price/packaging changes erode conversion within days.
- GTM teams that need a weekly "what changed in the market" digest without burning a senior analyst.
- Funded categories where new entrants (YC batches, ProductHunt launches, Stripe Atlas filings) appear faster than a quarterly TAM refresh can catch.
- Geo expansion plays where local competitors and regulatory shifts (DSA, EU AI Act, state-level US privacy) materially move the SOM monthly.
- Solopreneur stacks operating like a one-person research firm — the only way to keep a monitoring matrix alive is via cron + agents.
- Post-launch defense: detecting the moment a fast-follower clones your wedge, before churn shows up in the funnel.

## When NOT to use

- Pre-PMF zero-to-one with no defined competitive set — start with `market-research-tam-sam-som` and `competitor-analysis` once, not a rolling scan.
- Slow-moving regulated categories (medtech devices, defense, classical banking) where the market half-life is measured in years.
- Compliance-bound enterprise sales with 12–18 month cycles — quarterly market snapshots beat noisy weekly diffs.
- Single-customer custom-software work — there is no "market" to scan; switch to account-level intelligence.
- When the team will not act on signals — a continuously scanned market that nobody reads becomes a research graveyard and burns tokens.
- Crisis mode (active outage, churn cliff, lawsuit) — pause the scan, focus humans on the incident, resume after stabilization.

## Where it fails / limitations

- Source decay: SaaS competitors disable RSS, hide changelogs behind login, or move to gated Slack — the scan rots silently. Require a quarterly source-health audit.
- LLMs hallucinate competitor pricing pages and changelog entries when scrapes fail — every row needs a fetched-at timestamp + raw HTML hash, otherwise a "$49 → $99 price hike" can be fabricated.
- Signal volume without prioritization buries real moves under noise (every blog post becomes "competitor activity"). Severity scoring is mandatory.
- Scrape ToS / IP risk: aggressive crawling of G2, Capterra, LinkedIn, Glassdoor, Crunchbase invites blocks and legal letters. Use official APIs, RSS, and SerpAPI/Tavily-style aggregators with proper attribution.
- Geo blindness: a US-centric scan misses APAC/EU competitors; require segment-tagged source lists.
- Pricing pages A/B-test by region/cookie — single-shot scrapes give a misleading reading. Capture multiple geo + logged-out perspectives.
- No-news bias: agents anchor on "something must have changed" and fabricate diffs from cosmetic edits (font/CSS). Diff content blocks, not raw HTML.
- Without a clear "Outcome" the scan tracks 40 competitors instead of the 5 that move your SOM — agents cheerfully expand scope unless capped.

## Agentic workflow

```
Daily   → market-pulse (haiku)            → market-pulse-<date>.md
Daily   → competitor-changelog-watcher    → competitor-changes.md (append)
Daily   → pricing-watcher (haiku)         → pricing-snapshots/<date>/
Weekly  → review-mining (sonnet)          → review-themes.md (G2/Capterra/Reddit)
Weekly  → funding-news-watcher (haiku)    → funding-events.md
Weekly  → ad-creative-watcher (sonnet)    → ad-library/<vendor>/<date>/
Weekly  → seo-serp-watcher (haiku)        → serp-deltas.md
Bi-week → market-synthesizer (opus)       → market-map.md, threat-board.md
Monthly → market-strategist (opus)        → market-memo.md, kill/double-down list
Quarterly → tam-refresh (opus)            → tam-sam-som.md (versioned)
```

All outputs live under `.aidocs/market-intel/`. The synthesizer reads the week's diffs and updates a versioned `market-map.md` + `threat-board.md`. Cheap models for collection, sonnet for structured review/ad analysis, opus only for bi-weekly synthesis and quarterly refresh.

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `market-pulse` | haiku | Daily | Tavily/SerpAPI top-of-day for category keywords, Google News RSS, HN front page | 10-bullet daily digest tagged by competitor |
| `competitor-changelog-watcher` | haiku | Daily | Public changelog URLs, RSS, GitHub releases, Twitter/X handles | Per-competitor diff with severity 1–5 |
| `pricing-watcher` | haiku | Daily | Pricing pages (logged-out + 2–3 geos) | Diff vs prior snapshot, $-delta, packaging-delta |
| `review-mining` | sonnet | Weekly | G2/Capterra/TrustRadius/Reddit/AppStore review APIs | Theme cluster (gain/pain/switch reason), N≥5 rule |
| `funding-news-watcher` | haiku | Weekly | Crunchbase API, PitchBook RSS, TechCrunch tag feeds, OpenCorporates | Funding event list with stage/amount/investors |
| `ad-creative-watcher` | sonnet | Weekly | Meta Ad Library API, TikTok Creative Center, LinkedIn Ad Library | Active creatives + messaging hooks per competitor |
| `seo-serp-watcher` | haiku | Weekly | Ahrefs/SEMrush API, DataForSEO, your tracked keywords | Rank deltas, new pages indexed, BOFU keyword shifts |
| `marketplace-watcher` | haiku | Weekly | ProductHunt API, AppSumo RSS, YC Launch RSS, Stripe Atlas filings | New entrants list with category match score |
| `market-synthesizer` | opus | Bi-weekly | All of above + last `market-map.md` | Updated market map, threat board, opportunity list |
| `market-strategist` | opus | Monthly | All synth outputs + sales-CRM win/loss | Strategic memo: kill/double-down/watch buckets |
| `tam-refresh` | opus | Quarterly | Latest market reports, public filings, customer counts | Versioned TAM/SAM/SOM with delta vs last quarter |

### Prompt pattern

```
<role>You are {agent}. Continuous market scanning practitioner.</role>
<inputs>
  <since>{ISO8601 last-run timestamp}</since>
  <competitors>{path to competitor-registry.json}</competitors>
  <market_map>{path to market-map.md}</market_map>
  <category_keywords>{list}</category_keywords>
</inputs>
<rules>
  - Tag every observation with: source_url, fetched_at, competitor_id,
    signal_type (changelog|pricing|review|funding|ad|serp|launch),
    severity (1-5), confidence (0-1).
  - Reject any change that lacks a source_url + raw-content hash.
  - Cosmetic-only diffs (CSS, copy reorder) → severity 0, do not surface.
  - Pricing changes require >=2 geo snapshots before flagging.
  - For new entrants, score category match (0-1); discard <0.6.
  - Output JSON matching {schema_path}, plus markdown digest <= 60 lines.
</rules>
<task>{cadence-specific instruction}</task>
```

Wire via Claude Agent SDK with structured outputs (Pydantic/Zod schema enforced) — see `feedback_agent_output` in NERO memory.

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Orchestrate cadence subagents via slash commands (`/market-daily`, `/market-weekly`, `/market-synth`) | docs.anthropic.com/claude/code |
| `gh` | Pull competitor GitHub releases / repo activity for OSS competitors | cli.github.com |
| `tavily` API CLI | Agent-native web search, low-noise output | tavily.com/docs |
| `serpapi` / `dataforseo` | Structured SERP + News results | serpapi.com / dataforseo.com |
| `playwright` / `crawl4ai` | Render JS-heavy pricing & changelog pages | playwright.dev / crawl4ai.com |
| `httpx` + `selectolax` | Cheap static-page scraping with HTML diffing | github.com/projectdiscovery/httpx |
| `feedparser` (Python) | RSS/Atom changelog ingestion | pypi.org/project/feedparser |
| `gh-rss`, `releases.atom` | Built-in RSS for any GitHub repo | `https://github.com/<repo>/releases.atom` |
| `crunchbase` API | Funding + org data | data.crunchbase.com/docs |
| `ahrefs` / `semrush` / `dataforseo` | Keyword + rank monitoring | ahrefs.com/api / semrush.com/api |
| Meta Ad Library API | Active competitor ads | facebook.com/ads/library/api |
| `producthunt` API | New entrant detection | api.producthunt.com |
| `wayback-cdx` | Verify historical pricing claims | archive.org/help/wayback-api |
| `diff-match-patch` | Robust block-level diffing for changelog pages | github.com/google/diff-match-patch |
| `slack` webhook / `tg-send` | Push weekly digest to product/GTM channel | NERO `~/bin/tg-send` |
| `cron` / `systemd-timer` / `launchd` | Schedule cadence agents | `loop` skill / `schedule` skill |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Tavily | SaaS | Yes (REST, agent-tuned) | Cleanest signal for daily market-pulse |
| Exa.ai | SaaS | Yes (REST) | Semantic search, good for new entrant discovery |
| SerpAPI / DataForSEO | SaaS | Yes (REST) | Structured Google/Bing/News SERP |
| Crunchbase | SaaS | Yes (REST) | Funding + org data; rate-limited |
| PitchBook | SaaS | Limited | Costly; mostly enterprise |
| Similarweb / Semrush / Ahrefs | SaaS | Yes (REST) | Traffic + SERP signals |
| Sensor Tower / data.ai | SaaS | Yes (REST) | Mobile install + revenue estimates |
| Meta Ad Library | OSS API | Yes | Free, but auth + rate limits |
| TikTok Creative Center | SaaS | Limited | Web-only; scrape with care |
| Klue / Crayon / Kompyte / Contify | SaaS | Yes (REST + webhooks) | Compete-intel platforms; API surfaces curated alerts |
| Visualping / Distill.io / ChangeTower | SaaS | Yes (REST + webhooks) | Page-change detection if you don't want to host scrapers |
| Feedly Leo | SaaS | Yes (REST) | AI-curated competitor + market feeds |
| Owler | SaaS | Yes (REST) | Funding + news aggregation |
| Crayon Connect / Klue Cards | SaaS | Yes | Pre-packaged battlecards + diffs |
| Notion / Airtable | SaaS | Yes (REST) | Cheap home for `market-map.md` + `threat-board.md` |
| PostHog | OSS/SaaS | Yes (REST) | Cross-reference your funnel against signal events |
| Apollo.io / ZoomInfo | SaaS | Limited | Headcount/role-change signals; ToS sensitive |
| OpenCorporates | OSS API | Yes | Public filings, jurisdiction expansions |

## Templates & scripts

Daily competitor changelog + pricing watcher (Claude Agent SDK pseudocode, ~45 lines):

```python
from claude_agent_sdk import Agent, tool
from datetime import datetime, timedelta
from hashlib import sha256
import json, pathlib

@tool
def fetch_changelog(url: str) -> dict: ...
@tool
def fetch_pricing(url: str, geos: list[str]) -> list[dict]: ...
@tool
def diff_block(prev: str, curr: str) -> dict: ...
@tool
def append_jsonl(path: str, row: dict) -> None: ...

watcher = Agent(
    model="claude-haiku-4-7",
    system=open("prompts/market-changelog-watcher.xml").read(),
    tools=[fetch_changelog, fetch_pricing, diff_block, append_jsonl],
    output_schema=MarketSignal,  # Pydantic
)

since = (datetime.utcnow() - timedelta(hours=24)).isoformat()
registry = json.loads(pathlib.Path(".aidocs/market-intel/competitor-registry.json").read_text())
for c in registry["competitors"]:
    res = watcher.run(
        f"Competitor {c['id']}. Changelog={c['changelog_url']} "
        f"Pricing={c['pricing_url']} Geos={c['geos']} Since={since}. "
        f"Reject cosmetic-only diffs. Hash raw HTML, attach fetched_at."
    )
    for row in res.signals:
        row["raw_hash"] = sha256(row["raw"].encode()).hexdigest()
        append_jsonl(".aidocs/market-intel/signals.jsonl", row)
```

Competitor registry schema (`.aidocs/market-intel/competitor-registry.json`):

```json
{
  "competitors": [{
    "id": "comp_xxx",
    "name": "Acme",
    "tier": "direct|indirect|substitute",
    "changelog_url": "https://...",
    "pricing_url": "https://...",
    "geos": ["us-en", "de-de", "ua-uk"],
    "review_sources": ["g2:acme", "capterra:acme", "reddit:r/saas"],
    "tracking_keywords": ["..."],
    "last_audited": "ISO"
  }]
}
```

Cron schedule (`crontab -e`):

```
*/30 6-22 * * *  /usr/local/bin/claude run /market-pulse-quick
0 7 * * *        /usr/local/bin/claude run /market-daily
0 8 * * 1        /usr/local/bin/claude run /market-weekly
0 9 1,15 * *     /usr/local/bin/claude run /market-synth
0 10 1 * *       /usr/local/bin/claude run /market-strategist
0 11 1 1,4,7,10 * /usr/local/bin/claude run /tam-refresh
```

## Best practices

- Pin one strategic Outcome (e.g. "defend SMB SOM in EU") before any scan; without it agents track 40 competitors instead of the 5 that matter.
- Maintain a versioned `competitor-registry.json` — additions/removals via PR, never silent edits; ties signals to a stable `competitor_id`.
- Capture pricing from at least 2 geos + logged-out + incognito; otherwise A/B tests look like price changes.
- Hash raw HTML/PDF of every signal source; future re-checks against the hash catch silent CMS edits and Wayback discrepancies.
- Diff content blocks, not full DOM — boilerplate (nav, footer, cookie banners) generates 90% of false-positive diffs.
- Severity rubric is mandatory: 5 = pricing/packaging move; 4 = positioning shift / new ICP; 3 = new feature in core wedge; 2 = peripheral feature; 1 = blog/PR; 0 = cosmetic.
- Cross-reference signals with your own funnel (PostHog/GA4) — competitor launch + your sign-up dip is a real threat; competitor launch + flat funnel is noise.
- Quarterly `tam-refresh` must compare against last version with explicit delta + driver narrative; refuse to overwrite history.
- Tie market signals to GTM action: every severity-≥4 row must produce a "respond / monitor / ignore" decision within one weekly cycle, written into `threat-board.md`.
- Token budget: cap weekly synth at ~30k tokens, monthly strategist at ~80k, quarterly TAM at ~150k; otherwise opus costs balloon.
- Scrape politely: rotate UA, respect robots.txt, throttle to 1 req/2s per host, prefer official APIs/RSS where they exist.
- Keep a `dead-source.md` log: when a source goes 30 days without change OR returns errors 3 runs in a row, escalate to human audit.
- Versioned `market-map.md` (one file per quarter) lets the strategist diff Q-over-Q rather than re-derive each time.

## AI-agent gotchas

- LLMs hallucinate competitor pricing and changelog entries when scrapes fail — enforce a `source_url + fetched_at + raw_hash` triple in the schema and reject completions missing any field.
- "$49 → $99" sounds dramatic; without the geo + cookie context it may be the same price differently presented. Require ≥2 geo confirmations before flagging.
- Agents trained on generic content drift into "industry analyst" voice — strip vague predictions, require evidence rows for every claim.
- Daily haiku watchers will overwrite shared files if not append-only — use atomic JSONL append + lock file, never `Write` on shared logs.
- Bi-weekly synth with full week's signals can exceed context — pre-summarize per-day with haiku, feed summaries to opus.
- Review-mining hallucinates sentiment from headlines — require quote-level evidence (verbatim text + source URL) before any "competitor X has churn" claim.
- Subagents that write to Notion/Airtable via API can dup rows on retry — require idempotency key (hash of `competitor_id + signal_type + raw_hash`).
- Privacy / ToS: avoid LinkedIn / Glassdoor scraping; use Apollo/ZoomInfo via official API or skip those signals.
- "New entrant" agents over-trigger on rebrands of existing players — match on domain + founders + funding history, not just name.
- Translation drift: non-English changelogs translated by haiku lose nuance — for severity-≥4 events, force a sonnet re-read with translation memory.
- Cosmetic CSS changes register as full-page diffs — use a content-block extractor (readability/trafilatura) before diffing.
- Long-running cron agents accumulate state drift; have `market-strategist` run a monthly schema-validation pass over `competitor-registry.json` + `signals.jsonl`.
- PII in scraped content (e.g. customer logos, support transcripts on review sites) — strip before feeding to non-ZDR endpoints.
- Recency bias: agents weight last-week signals over multi-quarter trends; the bi-weekly synth must explicitly reweight against `market-map.md` history.
- "Validation" framing creeps in — this scan informs decisions, it does not "validate" them. Ban the word in synthesizer prompts.

## References

- Sibling user-discovery angle: `../../researcher/continuous-discovery/agent-integration.md`
- Sibling methodology: `../competitive-intelligence/README.md`
- Sibling methodology: `../competitor-analysis/README.md`
- Sibling methodology: `../market-research-tam-sam-som/README.md`
- Sibling methodology: `../trend-analysis/README.md`
- Klue, Crayon, Kompyte, Contify product docs (2025–2026) — competitive-intelligence platform patterns.
- Tavily, Exa.ai, SerpAPI docs — agent-native web search.
- Meta Ad Library API, TikTok Creative Center docs — ad-creative monitoring.
- Crunchbase, PitchBook, Owler API docs — funding/news streams.
- Anthropic Claude Agent SDK docs — agents, structured outputs, scheduled triggers.
- "Continuous Competitive Intelligence" practice notes (Klue, Crayon blogs 2025).
- NERO memory: `feedback_agent_output` (XML prompts + structured outputs), `feedback_self_evolution` (rolling improvement of pipelines).
