# Agent Integration — Zero-Click Search Adaptation

## When to use
- Organic traffic declining while search impressions hold steady (classic zero-click symptom)
- AI Overviews appearing for core keywords, suppressing CTR
- Client explicitly targeting AI citation rate as a KPI alongside traffic
- Content strategy pivot from traffic-first to brand/authority-first
- Evaluating whether a page should answer directly vs. redirect to deeper content

## When NOT to use
- Site has fewer than 500 monthly organic visits — fix indexing fundamentals first
- Domain is brand-new with no topical authority — invest in basic SEO before adaptation
- No analytics access to measure CTR and impression baselines — blind optimization
- Purely e-commerce product pages where transactional intent dominates (AI Overviews rarely appear)

## Where it fails / limitations
- AI citation tracking has no reliable public API — must infer from brand monitoring tools (Semrush, Ahrefs, BrightEdge)
- "Be the Source" requires original research; agents cannot fabricate data, only identify gaps and draft methodology
- Community-building tactics (Discord, Slack) require sustained human moderation — agent can scaffold, not sustain
- AI Overview appearance is non-deterministic; schema alone does not guarantee citation
- Results lag: citation improvements take 60-90 days minimum to surface in measurable signals

## Agentic workflow
A research-tier agent (Opus) analyzes GSC data exports, identifies pages where AI Overviews suppress CTR, and produces a prioritized opportunity list. A writing-tier agent (Sonnet) then drafts or rewrites content sections targeting featured-snippet and FAQ schema patterns. A data agent (Haiku) monitors brand mention feeds and tracks citation frequency changes weekly. Human reviews all published content before it goes live — agents do not push to CMS autonomously.

### Recommended subagents
- `faion-knowledge` (seo-manager/topical-authority) — builds topic cluster maps to identify citation-worthy content gaps
- `faion-knowledge` (seo-manager/google-ai-overviews-optimization) — paired methodology for schema and AIO-specific optimizations
- `faion-brainstorm` — ideation for original research angles that no competitor has covered

### Prompt pattern
```
Analyze the attached GSC export. Identify pages where:
- AI Overviews are confirmed present (CTR < 0.5%, impressions > 200/mo)
- Organic CTR dropped > 30% year-over-year
Return a ranked list of 10 pages with current CTR, impression count, and recommended adaptation tactic (FAQ schema / original data / long-tail pivot / featured snippet).
```

```
Draft a FAQ schema block for the following page excerpt targeting the query "<query>".
Each question must be answerable in one direct sentence. Output raw JSON-LD only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gsc-export` (unofficial) | Bulk-download Google Search Console data via API | `pip install google-search-console` |
| `ahrefs-cli` / API | AI Overview detection, CTR benchmarks | https://developers.ahrefs.com |
| `semrush` API | Brand mention tracking, citation monitoring | https://developer.semrush.com |
| `schema-validator` | Validate JSON-LD schema before publishing | https://validator.schema.org |
| `screaming-frog` | Crawl-and-audit structured data at scale | https://www.screamingfrog.co.uk/seo-spider |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Search Console | SaaS | Partial (API v1) | CTR and impression data; no AI Overview flag in API yet |
| Ahrefs | SaaS | Yes (REST API) | SERP feature detection, CTR benchmarking |
| Semrush | SaaS | Yes (REST API) | Brand monitoring, AI citation tracking dashboard |
| BrightEdge | SaaS | Yes (API) | Best AI Overview tracking, expensive |
| SparkToro | SaaS | No | Audience research; manual use only |
| Perplexity.ai | SaaS | Partial | Use for manual citation spot-checks; no programmatic access |
| Schema.org Validator | OSS | Yes | Validates JSON-LD; can be called via curl in CI |

## Templates & scripts
See `templates.md` for full content templates (FAQ schema, original research outline, AI citation monitoring report).

```bash
#!/bin/bash
# Check if a page's schema passes validation
# Usage: ./validate-schema.sh https://example.com/page
URL="${1:?Usage: validate-schema.sh <url>}"
curl -s "https://validator.schema.org/validate?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$URL'))")" \
  | python3 -c "import sys, json; d=json.load(sys.stdin); print('OK' if not d.get('errors') else d['errors'])"
```

## Best practices
- Update pages cited in AI Overviews within 30 days of data changing — freshness is a citation multiplier (3.2x)
- Add FAQ schema only to pages with genuine Q&A structure; stuffed FAQ blocks get ignored or penalized
- Track branded query volume monthly in GSC — rising branded searches are the leading indicator that zero-click adaptation is working before traffic recovers
- Original research with specific percentages and dates outperforms general best-practice content by citation rate; include publication date and methodology section
- On-SERP conversions (calls, directions, bookings) should be set up in Google Business Profile; these convert even when clicks don't happen
- Distinguish between zero-click loss (bad) and branded impression gain (good) — aggregate traffic decline can mask brand growth

## AI-agent gotchas
- Do not instruct agents to publish directly to CMS — schema errors or factual mistakes in AI-cited content spread fast; all content requires human approval before publication
- GSC API does not expose AI Overview presence; agents must cross-reference with manual spot-checks or third-party APIs (Ahrefs, Semrush) before declaring a keyword affected
- Agents will hallucinate statistics if asked to "find recent data" without a search tool; always provide actual GSC CSV exports as context rather than asking the agent to recall numbers
- Citation rate measurement is lagging by 60-90 days; agents must not treat short-term CTR drops as strategy failure
- Schema JSON-LD must be validated before committing to source; agents sometimes output invalid JSON; always run through schema.org validator

## References
- https://sparktoro.com/blog/less-than-half-of-google-searches-now-result-in-a-click/
- https://developers.google.com/search/docs/appearance/featured-snippets
- https://ahrefs.com/blog/featured-snippets-study/
- https://moz.com/zero-click-searches
- https://schema.org/FAQPage
