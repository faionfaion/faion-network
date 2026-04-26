# Agent Integration — Google Search Ads

## When to use
- Programmatic Search campaign management at scale: bulk RSA generation, search-term mining, negative-keyword sweeps, quality-score audits.
- Continuous SQR (search-query report) hygiene — agent runs daily, surfaces wasted spend, and proposes negatives for human approval.
- Keyword research pipelines: agent calls `KeywordPlanIdeaService` for seed lists and ranks ideas by predicted ROI.
- A/B testing RSA variants under Google Ads Experiments where agents create variants, monitor stat-sig, and roll out the winner.

## When NOT to use
- The first 14–21 days of a Smart Bidding campaign — agents that "fix" CPC mid-learning kill performance.
- Hyper-niche brand campaigns with <10 keywords and <$50/day; the API overhead is not worth it.
- Strategy decisions like "what's our brand voice" or "what's our offer" — humans drive these; agents execute downstream.
- Direct replacement for a skilled PPC manager auditing edge cases (policy strikes, suspicious traffic, competitor scraping).

## Where it fails / limitations
- Match-type semantics changed: "Broad" now relies heavily on AI close-variant matching and pulls irrelevant queries into your data. Agents must monitor SQRs aggressively.
- Quality Score is computed lazily by Google; mutating bids/keywords doesn't immediately reflect new QS — agents that read-after-write can see stale numbers for hours.
- `KeywordPlanIdeaService` returns ranged metrics (e.g. "1k–10k searches/mo"); agents that treat the midpoint as truth budget incorrectly.
- Smart Bidding strategies (Target CPA, Maximize Conversions) override most manual bid changes — agent setting `cpc_bid_micros` on a Target CPA campaign is a no-op.
- Negative-keyword lists have a 5,000-keyword limit per list, 20 lists per account; agents that mass-add negatives must shard.
- Responsive Search Ads (RSA) hide which combo served — A/B agents must use Google Ads Experiments, not naive ad-vs-ad CTR comparisons.
- DSA (Dynamic Search Ads) target by website crawl; an agent updating the page without notifying the campaign can starve impressions or generate junk.

## Agentic workflow
A Search agent runs three loops: (1) keyword discovery — pull KeywordPlanner ideas + SQR mining, propose new keywords/negatives; (2) ad refresh — generate RSA assets via LLM, validate length/policy, schedule for human approval; (3) hygiene — daily QS audit, low-CTR keyword pause, broken-URL check via the `final_urls` field. Always batch reads via `search_stream` and writes via `mutate_*` operations of ≤5,000 ops. Wrap every mutation in a dry-run preview that the human approves.

### Recommended subagents
- `faion-ads-agent` — Google Ads execution agent (shared with Display/Shopping/PMax).
- `faion-sdd-executor-agent` — gates code that wires search reports into product analytics.
- A copy-generation sub-agent (sonnet/opus) for headline/description drafts, separate from the executor that writes to API.

### Prompt pattern
```
System: You are the Search-ads agent. Headlines ≤30 chars, descriptions
        ≤90 chars (validate before POST). Never directly mutate bids on a
        Smart Bidding campaign. For new negatives, only propose; do not
        push without a unified-diff approval.
User:   Audit campaign 9876 for last 14 days: list keywords with QS<5
        and CTR<1%, propose pause + 5 alternative keyword ideas each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | API client | `pip install google-ads` |
| Google Ads Editor | Bulk offline edits / diff | https://ads.google.com/intl/en/home/tools/ads-editor/ |
| Google Keyword Planner (UI / API) | Search-volume + bid ranges | inside Google Ads |
| `seoreviewtools-keyword-density` / similar | Local keyword grouping helpers | various |
| Google Ads Scripts | In-product JS automation as fallback | https://developers.google.com/google-ads/scripts |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads (Search) | SaaS | Yes (API) | Core surface for keyword-targeted ads. |
| Google Search Console | SaaS | Yes (API) | Cross-reference paid + organic queries. |
| Bing / Microsoft Ads | SaaS | Yes (own API) | Mirror Google Search campaigns; same agent pattern. |
| SEMrush / Ahrefs | SaaS | Yes (API) | Competitor keyword + ad-copy research. |
| BigQuery + GA4 export | SaaS | Yes (SQL) | Cross-channel attribution and SQR enrichment. |
| Optmyzr / Adzooma | SaaS | Yes (API) | Pre-built PPC automations agents can call instead of writing from scratch. |

## Templates & scripts
See `templates.md` for keyword and ad templates. Inline RSA validator the agent should run before any creative POST:

```python
# rsa_validate.py — enforce Google's RSA character limits and pinning
HEADLINE_MAX = 30
DESC_MAX = 90

def validate_rsa(headlines: list[str], descriptions: list[str]) -> dict:
    errors = []
    if not (3 <= len(headlines) <= 15):
        errors.append("RSA needs 3–15 headlines")
    if not (2 <= len(descriptions) <= 4):
        errors.append("RSA needs 2–4 descriptions")
    for i, h in enumerate(headlines):
        if len(h) > HEADLINE_MAX:
            errors.append(f"H{i+1} '{h}' is {len(h)} chars (>30)")
    for i, d in enumerate(descriptions):
        if len(d) > DESC_MAX:
            errors.append(f"D{i+1} '{d}' is {len(d)} chars (>90)")
    return {"ok": not errors, "errors": errors}
```

## Best practices
- Use phrase + exact match for high-intent keywords; reserve broad match only with Smart Bidding + tight negatives.
- One theme per ad group, 10–20 keywords; resist the temptation to dump 200 keywords into one group.
- Pin only what the brand requires (legal disclaimers as H3, etc.) — over-pinning prevents Google from optimizing combinations.
- Ad-strength "Excellent" requires unique headlines + diverse messaging; agents that paste the same selling point 5 times never hit it.
- Run a `search_term_view` query at least weekly; SQRs reveal both new keyword candidates and negatives.
- Set up `auto_pause_poor_performers` automation (see `google-ads-reporting`) but with high impression thresholds (5k+) to avoid premature kills.
- Use Google Ads Experiments (campaign drafts) for any non-trivial bid-strategy or RSA test — naive split-testing on Search is unreliable.

## AI-agent gotchas
- LLMs invent keywords that violate Google policy (trademark, sensitive content). Run the proposed list against a denylist before inserting.
- Bid mutation on Smart Bidding: agents that compute "set CPC to $X" silently no-op when the campaign is on Target CPA / Max Conv.
- Match-type encoding: API uses enum names (`BROAD`, `PHRASE`, `EXACT`); agents emitting `"Broad Match"` in YAML break the writer.
- DSA "Dynamic" headlines are auto-generated from the landing page; agents writing static creative for DSA campaigns waste effort.
- Negative-keyword conflicts: agents that add a negative duplicating an existing positive keyword can pause the keyword in subtle ways. Cross-check before insert.
- Final URL drift: agents that update landing pages must update `final_urls` AND check tracking-template parameters; otherwise UTMs break silently.
- Human-in-loop checkpoint: any change to bid strategy, raising budget >25%, switching match types in bulk, removing more than 5 keywords from one group.

## References
- Search Campaign guide — https://support.google.com/google-ads/answer/1722047
- Responsive Search Ads — https://support.google.com/google-ads/answer/7684791
- Keyword match types — https://support.google.com/google-ads/answer/7478529
- Smart Bidding — https://support.google.com/google-ads/answer/7065882
- Google Ads Experiments — https://support.google.com/google-ads/answer/6318732
