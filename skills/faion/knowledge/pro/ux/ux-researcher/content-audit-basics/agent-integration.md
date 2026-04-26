# Agent Integration — Content Audit (Basics)

## When to use
- Pre-redesign or migration: build a complete URL inventory with quality scores before scope decisions.
- SEO/content strategy reset: combine crawl data + analytics + LLM quality scoring to decide keep/update/consolidate/remove.
- Quarterly content governance: rolling audits of high-traffic clusters with automated freshness checks.
- Site consolidation (M&A, multi-brand merge): de-duplicate near-identical pages across domains.

## When NOT to use
- Site under ~50 pages: a manual spreadsheet review is faster than tooling setup.
- Content does not yet exist (greenfield): use content modeling, not auditing.
- You only need analytics performance: GA4/GSC views suffice — no inventory needed.
- Pre-launch QA of a single page batch: use editorial review, not audit methodology.

## Where it fails / limitations
- Crawlers miss gated content, JS-rendered SPAs without prerendering, PDFs behind auth, and intranet pages.
- LLM quality scoring drifts across runs: same page can get 3 vs 4 unless you fix temperature=0 and a stable rubric prompt.
- Agents cannot judge brand voice or strategic relevance reliably — humans must validate the keep/remove cutoff.
- Pageview data lags new content; <90-day-old pages will look "low traffic" and get falsely flagged for removal.
- Sitemap-only crawls miss orphan pages; combine with log-file or GSC-impressions inventory.

## Agentic workflow
Drive the audit as a pipeline: a crawler agent produces the URL inventory, an enrichment agent joins analytics + GSC + Ahrefs/Semrush data, an LLM scoring agent applies the rubric per URL in batches, and a synthesis agent writes the keep/update/remove recommendations. Human sign-off only on the final action column for any URL with >100 monthly sessions. Cache crawl + analytics outputs to a local SQLite or Parquet file so re-scoring iterations don't re-hit APIs.

### Recommended subagents
- `faion-ux-researcher-agent` — owns the rubric, scores Accuracy/Relevance/Quality, drafts the action column.
- `faion-seo-manager` (from `pro/marketing/seo-manager`) — joins Ahrefs/GSC traffic and keyword cannibalization signals.
- `faion-content-marketer` — writes the rewrite/consolidation briefs for the URLs marked "Update".
- `faion-data-analyst` style subagent — for statistical sampling when audit covers >5k URLs.

### Prompt pattern
```
You are auditing a single URL against this rubric:
{rubric_yaml}
Page text: {extracted_markdown}
Page metrics: {gsc_clicks, ga4_sessions, last_modified}
Return JSON: {accuracy:1-5, relevance:1-5, quality:1-5, action:"keep|update|consolidate|remove", reason:<=2 sentences}.
```
Use one prompt per URL, batched 50-100 in parallel; never feed the whole inventory in one context.

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Screaming Frog SEO Spider | URL crawl + on-page extraction; CLI mode for headless runs | https://www.screamingfrog.co.uk/seo-spider/ |
| sitemap-generator-cli | Produce sitemap input for crawlers | `npm i -g sitemap-generator-cli` |
| `wget --spider --recursive` | Fallback crawl for small sites | builtin |
| `lighthouse-ci` | Per-URL quality + perf signals | `npm i -g @lhci/cli` |
| `gsc-cli` / Search Console API | Pull impressions, clicks, queries per URL | https://developers.google.com/webmaster-tools |
| `ga4-data-api` Python client | Pull sessions, engagement, conversions | `pip install google-analytics-data` |
| `csvkit` | Join inventory + metrics CSVs locally | `pip install csvkit` |
| Trafilatura | Extract clean main-content text for LLM scoring | `pip install trafilatura` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Screaming Frog | SaaS (desktop) | Partial — CLI mode + scheduled exports | Best-in-class crawler; license required for >500 URLs |
| Sitebulb | SaaS | Partial — has CLI/API in Enterprise | Visualization useful for stakeholder reports |
| ContentKing (Conductor) | SaaS | Yes — REST API | Continuous monitoring; good for governance phase |
| Ahrefs | SaaS | Yes — API for Site Explorer | Backlink + keyword join; rate-limited |
| Semrush | SaaS | Yes — API | Site Audit + Position Tracking |
| GSC (Search Console) | SaaS | Yes — official API | Free; pull impressions/clicks per URL |
| GA4 | SaaS | Yes — Data API | Free; per-page sessions + engagement |
| Airtable / Google Sheets | SaaS | Yes — both have APIs | Final inventory store + stakeholder review surface |
| Trafilatura / Readability | OSS | Yes | Pre-processing for LLM scoring |

## Templates & scripts
See `templates.md` for the full audit spreadsheet schema. Minimal pipeline sketch:

```python
# audit_pipeline.py — sketch, ~40 lines
import asyncio, csv, json, anthropic
from trafilatura import fetch_url, extract

RUBRIC = open("rubric.yaml").read()
client = anthropic.AsyncAnthropic()

async def score(url, metrics):
    html = fetch_url(url)
    text = extract(html) or ""
    msg = await client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        temperature=0,
        messages=[{"role":"user","content":
            f"Rubric:\n{RUBRIC}\nURL:{url}\nMetrics:{metrics}\nText:\n{text[:6000]}\n"
            "Return JSON only."}],
    )
    return url, json.loads(msg.content[0].text)

async def main(inventory_csv):
    rows = list(csv.DictReader(open(inventory_csv)))
    sem = asyncio.Semaphore(20)
    async def bound(r):
        async with sem:
            return await score(r["url"], {"sessions":r["sessions"],"clicks":r["clicks"]})
    results = await asyncio.gather(*[bound(r) for r in rows])
    with open("scored.jsonl","w") as f:
        for url, data in results:
            f.write(json.dumps({"url":url, **data})+"\n")

asyncio.run(main("inventory.csv"))
```

## Best practices
- Lock the rubric prompt (versioned file in repo) and the LLM model + temperature; otherwise scores are not comparable across audit cycles.
- Sample 5-10% of LLM scores for human review on every run — track inter-rater agreement (Cohen's kappa target >0.6) before trusting at scale.
- Join three data sources before scoring: crawl (existence + structure), GSC (search demand), GA4 (in-product behavior). Auditing crawl-only produces SEO blind spots.
- Keep the inventory keyed by URL hash, not URL string — redirects + trailing slashes will double-count otherwise.
- Treat "consolidate" as a distinct action from "remove" — agents tend to over-classify low-traffic pages as remove when canonical merge is the better play.
- Output the action column as a recommendation, not a decision. The audit ships when humans sign off the high-stakes rows.

## AI-agent gotchas
- Token budget: feeding full HTML blows context. Always pre-extract main content (Trafilatura/Readability) and cap at ~6k chars per URL.
- Hallucinated quality scores on empty/404 pages: include an explicit `if text == "": return action=remove, reason="empty"` guard before LLM call.
- LLM cannot see images; pages whose value is visual (galleries, infographics) get falsely scored as "low quality". Flag image-heavy pages and route to human review.
- Determinism: even at temperature=0, batches across days drift. Pin the SDK and model version, log them per row, and re-score the full set when models change — don't mix.
- Privacy: gated/PII content must be excluded before sending to any LLM. Add a robots-style allowlist check upstream of the scoring agent.
- Cost: 50k URLs * ~5k tokens * Opus pricing is significant. Use Haiku for first-pass triage, escalate only borderline (score 2-4) URLs to Opus.

## References
- Land, Paula — *Content Audits and Inventories* (Rockley Group)
- Halvorson, Kristina — *Content Strategy for the Web*
- Nielsen Norman Group — Content Audits: https://www.nngroup.com/articles/content-audits/
- Moz — How to Conduct a Content Audit: https://moz.com/blog/content-audit
- Anthropic — Prompt caching for batch scoring: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
