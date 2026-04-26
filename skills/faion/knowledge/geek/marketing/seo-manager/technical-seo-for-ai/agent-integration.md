# Agent Integration — Technical SEO for AI

## When to use
- Launching a new site or major content section that needs to attract AI crawler citations
- Auditing an existing site for AI crawler compatibility (GPTBot, ClaudeBot, PerplexityBot)
- Implementing llms.txt, schema markup, or semantic HTML improvements in bulk across many pages
- After Google AI Overviews or Perplexity begin appearing for target queries but the site is not cited
- When technical SEO debt (poor URL structure, missing schema, no heading hierarchy) is blocking AI citation

## When NOT to use
- For paywalled or gated content that should not be crawled by AI systems
- When the primary goal is traditional Google SERP ranking only (overlap exists, but priorities differ)
- When content is thin or low-authority — technical fixes cannot overcome content quality gaps
- For JavaScript-only SPAs where crawlability is fundamentally broken (fix rendering first)

## Where it fails / limitations
- llms.txt is a voluntary signal — AI crawlers are not required to respect it
- Schema markup improves citation probability but does not guarantee AI Overview inclusion
- Core Web Vitals improvements take weeks to reflect in crawl frequency changes
- AI crawler behavior is not fully documented and changes without notice
- Entity clarity requires manual content review — agents cannot reliably infer domain-specific entity relationships

## Agentic workflow
A Claude subagent can audit a site's technical SEO for AI by reading the sitemap, sampling page HTML for heading hierarchy and schema presence, checking robots.txt and llms.txt existence, and outputting a structured gap report. Schema generation (Article, Author, FAQ JSON-LD) is well-suited to agent automation given its templated nature. Content freshness updates (dateModified, statistics refresh) can be batched across pages by an agent with Write access. Human review is required before deploying llms.txt rules and schema changes to production.

### Recommended subagents
- `faion` — load seo-manager methodology for schema templates and llms.txt structure
- general Bash subagent — curl-based crawl sampling, robots.txt fetch, sitemap parsing

### Prompt pattern
```
Audit the following URLs for AI-SEO compliance:
<urls>{{urls}}</urls>
Check: (1) heading hierarchy H1→H2→H3, (2) schema markup presence (Article/FAQ/Author),
(3) llms.txt at domain root, (4) robots.txt AI crawler rules.
Output a JSON report with field: { url, issues: [], schema_types_found: [] }
```

```
Generate JSON-LD Article schema for this page:
Title: {{title}}, Author: {{author}}, Credentials: {{credentials}},
DatePublished: {{date}}, DateModified: {{date}}, Description: {{desc}}
Return only the <script type="application/ld+json"> block, no explanation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | Fetch robots.txt, llms.txt, page HTML for analysis | system package |
| `htmlq` | CSS selector queries on HTML from CLI | `cargo install htmlq` / https://github.com/mgdm/htmlq |
| `jq` | Parse and validate JSON-LD schema blocks | `apt install jq` |
| `lighthouse` | Core Web Vitals audit, structured data validation | `npm i -g lighthouse` / https://developer.chrome.com/docs/lighthouse |
| `xmllint` | Validate sitemap XML | `apt install libxml2-utils` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Search Console | SaaS | Partial — API available | AI Overview data since June 2025; use API for impression/click data |
| Semrush AI Toolkit | SaaS | No direct API | AI visibility tracking; export CSV for agent ingestion |
| Otterly.AI | SaaS | No | Dedicated AI citation monitoring; manual review required |
| Profound | SaaS | No | AI search analytics; enterprise pricing |
| Schema.org Validator | OSS/web | Yes — via HTTP POST | `https://validator.schema.org/` accepts JSON-LD for validation |
| llmstxt.org | Reference | Yes — read spec | Canonical llms.txt specification and format reference |

## Templates & scripts
See `templates.md` for llms.txt and JSON-LD schema templates.

Inline: bulk schema injection audit script (≤50 lines):
```bash
#!/bin/bash
# Check schema presence across sitemap URLs
SITEMAP_URL="${1:?Usage: $0 <sitemap_url>}"
URLS=$(curl -s "$SITEMAP_URL" | grep -oP '(?<=<loc>)[^<]+')

for url in $URLS; do
  html=$(curl -s --max-time 5 "$url")
  has_schema=$(echo "$html" | grep -c 'application/ld+json' || true)
  has_h1=$(echo "$html" | grep -ciP '<h1[ >]' || true)
  has_datemod=$(echo "$html" | grep -c 'dateModified' || true)
  echo "{\"url\":\"$url\",\"schema_blocks\":$has_schema,\"h1_count\":$has_h1,\"has_dateModified\":$has_datemod}"
done
```

## Best practices
- Place the direct answer to a query in the first 1-2 sentences after the matching heading — AI extraction pulls the nearest text after a matched heading
- Use FAQ schema for any page containing Q&A sections; this alone accounts for measurable citation lift
- Set both `datePublished` and `dateModified` in schema — freshness within 30 days yields 3.2x more AI citations
- Keep llms.txt under 100 lines; AI crawlers parse it as a hint file, not a full directive
- Block admin, account, and checkout paths in robots.txt AI crawler sections to conserve crawl budget for content pages
- Audit heading hierarchy programmatically — nested H2→H4 jumps break AI entity extraction
- Never place critical facts only in images or JavaScript-rendered elements — AI crawlers rely on static HTML

## AI-agent gotchas
- Schema generation is reliable but agents may hallucinate `@type` values not in Schema.org — always validate output against `https://validator.schema.org/`
- Agents cannot determine if content is semantically accurate or up-to-date; human fact-check is mandatory before dateModified is updated
- llms.txt `Disallow` directives affect voluntary compliance only — agent should flag sensitive paths but human decides which paths to protect
- Bulk schema injection via agent risks duplicate `<script type="application/ld+json">` blocks if page already has partial schema — agents must check before inserting
- Core Web Vitals measurement requires a browser agent (Lighthouse, Playwright); text-only agents cannot assess INP or CLS

## References
- https://llmstxt.org/ — llms.txt specification
- https://schema.org/ — Schema.org vocabulary reference
- https://developers.google.com/search/docs/appearance/structured-data — Google structured data guidelines
- https://support.google.com/websearch/answer/13451556 — Google AI Overviews documentation
- https://www.perplexity.ai/publishers — Perplexity publisher guidance
- https://developer.chrome.com/docs/lighthouse — Lighthouse audit tool
