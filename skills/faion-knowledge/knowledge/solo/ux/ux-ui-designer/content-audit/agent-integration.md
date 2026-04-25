# Agent Integration — Content Audit

## When to use
- Pre-redesign inventory: agent crawls a site and produces a structured content catalog before UX work begins
- Evaluating content quality at scale: agent scores hundreds of pages against defined criteria (accuracy, relevance, quality) faster than manual review
- Migration planning: mapping old URLs to keep/redirect/remove decisions before a CMS migration
- SEO-driven content pruning: combining crawl data + analytics to identify low-traffic, low-quality pages for removal
- Ongoing governance: running a rolling audit on a subset of pages (e.g., all blog posts older than 18 months)

## When NOT to use
- New sites or products with under 50 pages — a spreadsheet and manual review is faster
- When the primary goal is information architecture redesign (content audit catalogs; IA redesign requires card sorting and tree testing separately)
- Highly regulated content (medical, legal) where agent quality judgments must not substitute for subject-matter expert review
- When analytics access is unavailable — a quantitative audit without traffic data produces low-value remove/keep decisions

## Where it fails / limitations
- Agent cannot crawl authenticated (gated) content, dynamic JavaScript-rendered pages, or PDFs without explicit tooling setup
- Quality scoring (accuracy, relevance) is subjective; agent scores based on content text alone — lacks domain expertise for specialized topics
- Large sites (10k+ pages) require chunked batches; agent context limits prevent single-pass analysis of entire crawl output
- Agent has no access to CMS metadata (publish date, author, review schedule) unless exported and provided explicitly

## Agentic workflow
A Claude subagent receives a CSV/TSV export from Screaming Frog (or similar crawler) containing URL, title, word count, status code, and last-modified date. It applies the evaluation criteria framework (accuracy/relevance/quality 1-5 scale) to each page based on title and any available meta content, then outputs a scored spreadsheet with Keep/Update/Remove/Archive actions. A second pass cross-references against Google Analytics pageview data (exported CSV) to validate decisions against actual usage.

### Recommended subagents
- `faion-sdd-executor-agent` — run the audit as a structured SDD task with defined input/output contracts
- General Claude subagent with analyst role — score content batches against provided evaluation criteria

### Prompt pattern
```
You are a content auditor. Evaluate each page below against these criteria (score 1-5):
- Accuracy: Is the content factually current and correct based on the title/topic?
- Relevance: Does this content serve the site's primary user needs?
- Quality: Is the writing clear, complete, and well-structured?

For each page return: URL | Title | Accuracy | Relevance | Quality | Avg | Action (Keep/Update/Rewrite/Remove)
Action thresholds: Avg >= 4.0 → Keep; 3.0-3.9 → Update; 2.0-2.9 → Rewrite; < 2.0 → Remove.
Flag any pages where you cannot assess accuracy due to insufficient information.

Pages to evaluate:
[paste CSV rows]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Screaming Frog SEO Spider | Full site crawl → CSV export (URL, title, word count, status, canonical, etc.) | Desktop app (free up to 500 URLs) / https://www.screamingfrog.co.uk/seo-spider/ |
| Sitebulb CLI | Crawl with structured JSON output; better for scripted pipelines | https://sitebulb.com (paid) |
| wget --spider | Lightweight URL discovery for small sites | `wget --spider -r -nd --delete-after <url>` |
| csvkit | CLI tools for filtering, joining, and transforming audit CSVs | `pip install csvkit` / https://csvkit.readthedocs.io |
| Google Analytics Data API | Pull pageview/engagement metrics programmatically | `pip install google-analytics-data` / https://developers.google.com/analytics/devguides/reporting/data/v1 |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Screaming Frog | SaaS/desktop | Partial (CSV export) | No REST API; export crawl results as CSV and feed to agent |
| Ahrefs | SaaS | Partial (API, paid) | Site audit endpoint; returns crawl issues, broken links, thin content flags |
| Semrush | SaaS | Partial (API, paid) | Site Audit API; content score per page available |
| ContentKing | SaaS | Yes (API) | Real-time crawl + content change monitoring; REST API for programmatic access |
| Google Search Console | SaaS | Yes (API) | Search performance data (clicks, impressions, CTR) per URL; excellent complement to crawl data |
| Airtable | SaaS | Yes (API) | Ideal as audit database backend; agent can write scored rows via Airtable REST API |
| Notion | SaaS | Yes (API) | Alternative audit tracking; Notion API allows row creation per audited page |

## Templates & scripts
See `templates.md` for the full Content Audit Spreadsheet column definitions and Evaluation Criteria scoring guide. Below is a shell script to merge a Screaming Frog export with a Google Analytics export:

```bash
#!/usr/bin/env bash
# merge-audit.sh — join crawler output with GA pageview data
# Requires: csvkit (pip install csvkit)
# Usage: bash merge-audit.sh crawl.csv ga-pageviews.csv output.csv
CRAWL="${1:?Usage: $0 <crawl.csv> <ga.csv> <output.csv>}"
GA="${2:?}"
OUT="${3:-audit-merged.csv}"

# Normalize URL column names (Screaming Frog uses "Address", GA uses "Page path")
csvcut -c "Address,Title 1,Word Count,Status Code,Last Modified" "$CRAWL" \
  | csvpy -S "
import sys, csv
r = csv.reader(sys.stdin)
h = next(r)
h[0] = 'url'
print(','.join(h))
for row in r:
    print(','.join(row))
" > /tmp/crawl-norm.csv

csvcut -c "Page path,Sessions" "$GA" \
  | csvpy -S "
import sys, csv
r = csv.reader(sys.stdin)
h = next(r)
h[0] = 'url'
print(','.join(h))
for row in r:
    print(','.join(row))
" > /tmp/ga-norm.csv

csvjoin -c url /tmp/crawl-norm.csv /tmp/ga-norm.csv > "$OUT"
echo "Merged audit written to $OUT"
```

## Best practices
- Export the crawl before starting any redesign or structural changes — the audit is a snapshot, not a live view
- Define evaluation criteria explicitly before scoring; let the agent score against written criteria, not implicit ones
- Batch large sites into topical groups (blog, product, help) and audit each group with domain-appropriate criteria
- Always cross-reference remove/archive decisions with inbound link data — a low-traffic page with high inbound links should be redirected, not deleted
- Document the audit in a versioned spreadsheet; keep it for at least one full content cycle to track governance effectiveness
- Assign a human owner to each "Update" action item — agent recommendations without human ownership stall

## AI-agent gotchas
- Agent accuracy scores on specialized content (technical docs, medical, legal) are unreliable without domain context; flag these for human expert review
- "Remove" recommendations carry SEO risk; always generate a redirect mapping before any deletion — agent should output redirect pairs, not just removal decisions
- Human-in-loop checkpoint: final Keep/Remove decisions must be approved by a content owner or PM, not executed automatically
- Agent may confidently score pages where it has only the URL/title and no body content — require agent to declare confidence level per row
- Context window limits mean the agent can process roughly 200-400 page rows per call; batch processing requires consistent scoring criteria across batches (prompt must remain identical)

## References
- https://www.nngroup.com/articles/content-audits/
- https://moz.com/blog/content-audit
- https://www.semrush.com/blog/content-audit/
- Paula Land, *Content Audits and Inventories* (XML Press)
- Kristina Halvorson & Melissa Rach, *Content Strategy for the Web* (2nd ed.)
