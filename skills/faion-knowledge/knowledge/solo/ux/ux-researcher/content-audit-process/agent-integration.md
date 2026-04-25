# Agent Integration — Content Audit Process

## When to use
- Before a site migration: need a complete inventory of what exists and what moves
- When SEO performance has dropped and you suspect duplicate or thin content
- When a redesign requires decisions about which content to keep, update, or cut
- When a new content strategy is being set and the team does not know the baseline
- Quarterly or semi-annual governance reviews for mature content-heavy sites

## When NOT to use
- For sites with fewer than 50 pages — manual review is faster than setting up tooling
- When the only goal is traffic analysis — use analytics directly, not a full audit
- When no one owns the resulting action items — audits without ownership produce spreadsheets, not change
- Immediately after a major launch when content is still stabilizing

## Where it fails / limitations
- Automated crawlers miss gated content, dynamically rendered pages (JS SPAs), PDFs behind login, and content in iframes
- Quality scoring is subjective when multiple evaluators apply criteria differently — calibration sessions are often skipped
- Large audits (1000+ pages) produce spreadsheets too large for a single agent context window; chunking is required
- Analytics data from the past 90 days may not represent seasonal content performance
- Audits surface problems but do not write the content — the remediation work is often underestimated by 3–5x

## Agentic workflow
A Claude subagent works well for the evaluation phase: given a batch of URLs with their titles, descriptions, word counts, and analytics metrics, the agent can apply the scoring rubric (accuracy, relevance, quality, SEO, accessibility) and return an action recommendation (keep/update/consolidate/rewrite/remove) with a rationale. Batch size should be capped at 50–100 items per agent call to keep context manageable. The crawl and inventory steps must be done with dedicated tools before the agent is invoked.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet) — batch evaluation of content items against rubric criteria
- `faion-sdd-executor-agent` — structured task execution for the remediation plan that follows the audit

### Prompt pattern
```
You are a content auditor. For each URL below, evaluate the content against these criteria and return a JSON array.

Criteria (score 1–5):
- accuracy: Is the information current and factually correct based on the excerpt?
- relevance: Does it serve the target audience described?
- quality: Is it well-written, free of jargon, appropriately detailed?
- action: one of keep | update | consolidate | rewrite | remove

Input format: [{ url, title, meta_description, word_count, pageviews_90d, excerpt }]
Output format: [{ url, scores: { accuracy, relevance, quality }, action, rationale }]

Content batch: [JSON]
Target audience: [description]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `screaming-frog` | Crawl site, export URL list with metadata | Desktop app / [screamingfrog.co.uk](https://www.screamingfrog.co.uk/seo-spider/) |
| `sitebulb` | Crawl + visual audit reports | Desktop app / [sitebulb.com](https://sitebulb.com) |
| `wget --spider` | Lightweight recursive link discovery | Built-in on Linux; `wget --spider -r -nd -nv [URL]` |
| `ahrefs-cli` (via API) | Pull organic traffic data per URL | [ahrefs.com/api](https://ahrefs.com/api) |
| `ga4-cli` (unofficial) | Export GA4 pageview data to CSV | `pip install ga4py` / [GA4 Data API](https://developers.google.com/analytics/devguides/reporting/data/v1) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Screaming Frog | SaaS/desktop | Partial — CSV export | Agent reads export; cannot drive the UI |
| ContentKing | SaaS | Yes — REST API | Real-time content monitoring; API returns page data |
| Ahrefs | SaaS | Yes — REST API | Organic traffic, backlinks, top pages per domain |
| Google Search Console | SaaS | Yes — API | Impressions, clicks, avg position per URL |
| GatherContent | SaaS | Yes — API | Content workflow and migration planning |
| Notion / Google Sheets | SaaS | Yes | Agent writes audit results to a shared spreadsheet via API |

## Templates & scripts
See `README.md` for the Report Template and evaluation criteria table.

Script — pull GA4 pageviews for a list of URLs and append to CSV:
```python
#!/usr/bin/env python3
"""
Usage: python ga4_pageviews.py --property 123456789 --urls urls.txt --days 90
Requires: pip install google-analytics-data
Set GOOGLE_APPLICATION_CREDENTIALS to service account JSON path.
"""
import argparse, csv, sys
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension, FilterExpression, Filter

def fetch(property_id, urls, days):
    client = BetaAnalyticsDataClient()
    results = {}
    for url in urls:
        req = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
            dimension_filter=FilterExpression(
                filter=Filter(field_name="pagePath", string_filter=Filter.StringFilter(value=url))
            ),
        )
        resp = client.run_report(req)
        views = int(resp.rows[0].metric_values[0].value) if resp.rows else 0
        results[url] = views
    return results

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--property", required=True)
    ap.add_argument("--urls", required=True)
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()
    urls = [l.strip() for l in open(args.urls) if l.strip()]
    data = fetch(args.property, urls, args.days)
    w = csv.writer(sys.stdout)
    w.writerow(["url", "pageviews"])
    for url, views in data.items():
        w.writerow([url, views])
```

## Best practices
- Calibrate quality scoring with two reviewers on a sample of 20 items before the full audit — prevents scoring drift
- Separate inventory (what exists) from evaluation (what to do) — mixing them in one pass produces inconsistent results
- Anchor "keep" decisions to traffic thresholds and business goals, not opinion: define the threshold before starting
- Assign a single owner to each "update" and "rewrite" action at report time — unassigned items are never done
- Archive removed content to a staging environment before deletion; broken inbound links surface within days
- Run the crawl at off-peak hours if the site has rate limiting or a CDN with aggressive bot detection

## AI-agent gotchas
- Agent context window limits batching: a 1000-page audit must be split into chunks of 50–100 rows with the rubric repeated per chunk
- Agents evaluate excerpts, not full pages — the excerpt must include the H1, first 200 words, and any key claims for the score to be meaningful
- Quality and accuracy scores are inherently subjective; treat agent output as a first draft, not a final verdict
- Agents do not have access to live analytics — pass pre-exported metrics as structured data in the prompt
- Consolidation recommendations require understanding which pages cover the same topic: agent needs a keyword or topic field to identify duplicates; URL and title alone are insufficient
- Do not ask the agent to both evaluate and rewrite in one call — evaluation quality degrades when generation is mixed in

## References
- [Content Audit Guide — NNG](https://www.nngroup.com/articles/content-audits/)
- [Content Harmony Step-by-Step Audit](https://www.contentharmony.com/blog/content-audit-guide/)
- [GA4 Data API Reference](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [ContentKing API Docs](https://www.contentkingapp.com/support/api/)
- [GatherContent Content Strategy Toolkit](https://gathercontent.com/content-strategy-toolkit)
