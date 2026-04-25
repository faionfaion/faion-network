# Agent Integration — Google AI Overviews Optimization

## When to use
- Target queries show AI Overview panels but site content is not cited
- Launching content for Science, Technology, Health, or Computers & Electronics niches where AI Overview frequency is highest (17-26%)
- Running a content freshness audit — pages not updated within 30 days are losing citation opportunities
- Preparing content strategy for queries where 3-5 sources dominate AI Overview citations
- Setting up tracking infrastructure for AI Overview impression data in Google Search Console

## When NOT to use
- For YMYL (Your Money, Your Life) queries where Google applies strict authority requirements that take months to build — quick optimizations won't move citations
- When domain authority is too low to be considered by Google's citation algorithm — address off-page authority first
- For navigational queries (brand names, direct URLs) — AI Overviews rarely appear for navigational intent
- When the site is penalized or manually reviewed by Google

## Where it fails / limitations
- Google does not expose which content signals trigger AI Overview citation — optimization is probabilistic
- Citation frequency is volatile; pages get added and removed from AI Overviews without notice
- Google Search Console AI Overview data (available since June 2025) shows impressions/clicks but not which exact content was extracted
- Schema markup shows +28% citation improvement on average but results vary widely by niche and query type
- Content freshness (30-day update rule) is a strong signal but does not guarantee citation for older authoritative content

## Agentic workflow
A Claude subagent can systematically identify AI Overview candidates by analyzing target queries, auditing competitor citations, and generating optimized content structures. The agent handles content structure analysis (heading hierarchy, answer placement, FAQ extraction) and schema generation. Citation monitoring requires periodic re-checks via Search Console API or third-party tools — agents can schedule these checks and flag pages that drop out of citations. Human approval is required before publishing content changes and before schema modifications go to production.

### Recommended subagents
- `faion-knowledge` — load seo-manager/google-ai-overviews-optimization for optimization templates
- general research subagent — query SERP sampling to detect which queries show AI Overviews
- Bash subagent — Google Search Console API data retrieval and citation tracking

### Prompt pattern
```
Analyze this content page for Google AI Overview optimization:
<content>{{page_content}}</content>
Target query: {{query}}

Check:
1. Is the direct answer within 2 sentences of the relevant heading?
2. Does the page use Article + FAQ schema?
3. Is dateModified within 30 days?
4. Are all statistics cited with source and date?

Output: JSON with fields { issues: [], score: 0-100, priority_fixes: [] }
```

```
Rewrite this section for AI Overview extraction optimization.
Original: {{section_text}}
Target query: {{query}}
Requirements: answer first, ≤2 sentences, cite source, use plain language, avoid passive voice.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-search-console-api` | Fetch AI Overview impression data | https://developers.google.com/webmaster-tools/v1/api_reference_index |
| `curl` + `jq` | GSC API calls and JSON parsing | system packages |
| `lighthouse` | Page quality and structured data audit | `npm i -g lighthouse` |
| `python-semrush` | Semrush API client for AI visibility data | `pip install semrush` / https://pypi.org/project/semrush |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Search Console | SaaS | Yes — REST API | AI Overview clicks/impressions since June 2025; requires OAuth |
| Semrush AI Toolkit | SaaS | Partial — API | AI visibility tracking; position tracking for AI Overview-heavy queries |
| Otterly.AI | SaaS | No | Real-time AI citation monitoring; manual sampling UI |
| Profound | SaaS | No | Enterprise AI search analytics; CSV export for agent ingestion |
| BrightEdge | SaaS | No | AI Overview frequency research; enterprise only |
| Ahrefs | SaaS | Partial — API | SERP features tracking including AI Overviews |

## Templates & scripts
See `templates.md` for FAQ schema and content structure templates.

Google Search Console AI Overview data fetch (requires GSC API access):
```bash
#!/bin/bash
# Fetch AI Overview performance data from GSC API
# Requires: gcloud auth application-default login
SITE_URL="${1:?Usage: $0 <site_url> <start_date> <end_date>}"
START="${2:-2025-06-01}"
END="${3:-2025-12-31}"

ACCESS_TOKEN=$(gcloud auth application-default print-access-token)

curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITE_URL', safe=''))")/searchAnalytics/query" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"startDate\": \"$START\",
    \"endDate\": \"$END\",
    \"dimensions\": [\"query\", \"page\"],
    \"searchType\": \"discover\"
  }" | jq '.rows[] | {query: .keys[0], page: .keys[1], clicks: .clicks, impressions: .impressions}'
```

## Best practices
- Place the direct answer to each heading's implied question within the first 1-2 sentences below that heading — this is the primary extraction pattern Google's AI uses
- Update statistics and dates in content on a 30-day cycle; the freshness signal is the strongest controllable factor
- Use FAQ schema for any page with 5+ questions; FAQ schema is directly mapped to Google's Q&A extraction pipeline
- Build content in topical clusters rather than isolated pages — AI Overviews favor sites with demonstrated topical authority across a subject area
- Diversify citation sources by getting mentions from multiple high-authority domains in your niche; AI Overviews rarely cite sites that only reference themselves
- Write short paragraphs (3-4 sentences max) — AI extraction breaks down on dense paragraphs with embedded complex sentences
- Explicitly define every technical term on first use — entity clarity is the foundation of AI extraction quality

## AI-agent gotchas
- Agents can generate optimized content structure but cannot verify factual accuracy — all statistics and claims require human fact-check before publishing
- FAQ schema generation must match exactly what is visible on the page — agents sometimes generate schema that describes intended content, not actual content, causing validation failures
- Google's AI Overview composition algorithm is a black box; agent-generated "AI Overview likelihood scores" are approximations based on observable patterns, not ground truth
- Content freshness updates (changing dateModified) without actual content changes are detectable by Google and may be discounted
- Agents cannot reliably determine current SERP state for a query without a live search tool — AI Overview presence varies by location, login state, and query phrasing

## References
- https://support.google.com/websearch/answer/13451556 — Google AI Overviews documentation
- https://developers.google.com/search/blog — Google Search Central Blog
- https://developers.google.com/webmaster-tools/v1/api_reference_index — Google Search Console API
- https://www.brightedge.com/resources/research-reports — BrightEdge AI Overview frequency research
- https://searchengineland.com/library/google/google-ai-overviews — Search Engine Land AI Overviews coverage
- https://schema.org/Article — Article schema reference
