# Agent Integration — Meta Targeting & Audiences

## When to use
- Programmatic build/refresh of Meta Custom Audiences from CRM, pixel, or warehouse data on a schedule.
- Auto-generating Lookalike audiences (1 / 2-3 / 5-10%) when a source segment crosses the 1k-seed threshold.
- Maintaining exclusion audiences (recent purchasers, paid trials, churned) so prospecting ad sets do not double-charge.
- Building structured audience-test campaigns (3-5 ad sets, identical creative) and waiting for statistical significance before promoting winners.
- Reconciling audience size/overlap reports across Meta Ads Manager + a data warehouse (BigQuery / Snowflake).

## When NOT to use
- Tiny budgets (<$30/day) where Advantage+ broad targeting will outperform manual segmentation. Skip the methodology, run one Advantage+ ad set.
- Highly regulated verticals (housing, employment, credit, health) — Meta enforces Special Ad Category which disables most demographic, ZIP, and custom-audience features. Manual review required, no agent automation.
- First 50 conversions of a new pixel — too little data for lookalikes. Wait until source seed is statistically meaningful.
- B2B niche where the entire TAM is <500k people on Meta. LinkedIn/Google are better channels.

## Where it fails / limitations
- iOS 14.5+ ATT erodes pixel-only retargeting; without CAPI + offline conversions, custom audiences shrink 30-60%. Agents that only manage pixel events will silently degrade.
- Lookalike quality drops sharply when source <1k or source skewed (e.g. 90% one country). Agent must sanity-check source distribution before creating LAL.
- Audience overlap >25% inside one campaign causes Meta to suppress one ad set. Agent must run Audience Overlap report and dedupe before launch.
- Advantage+ Audience often ignores manual exclusions when "Audience suggestion" is enabled — agent must verify exclusions stuck after each save.
- Custom Audience minimum (1k) is enforced silently — uploads below threshold appear "Ready" but never deliver.

## Agentic workflow
A Claude subagent orchestrates audience hygiene as a recurring job: pull source segments from the warehouse, validate seed size and distribution, call the Marketing API to upsert Custom Audiences (hashed PII), trigger Lookalike creation, and write back audience IDs + sizes to a registry table. A second pass diffs current vs. desired audience state and applies changes idempotently. Human-in-the-loop only on first creation of a new lookalike family or when overlap >25% triggers a review.

### Recommended subagents
- `faion-ads-agent` (defined in methodology frontmatter) — owns the Meta Marketing API surface for audiences and ad sets.
- `faion-sdd-executor-agent` — wraps audience-refresh tasks as SDD tasks with quality gates (size threshold, overlap check, exclusion verification).
- `password-scrubber-agent` — scrubs hashed-PII payloads from logs before they reach disk or the model context.

### Prompt pattern
```
Goal: refresh Meta Custom Audience CA_purchasers_180d from warehouse table dwh.fact_orders.
Constraints: hash email+phone with SHA-256 lowercase trim; chunk to 10k rows; replace, not append.
Verify: api returns audience_id; size > 1000; overlap with CA_acquisition_excl < 5%.
On fail: stop; emit alert; do NOT auto-create LAL.
```

```
Goal: build LAL family from CA_purchasers_180d.
Pre-check: source size >= 2000; country mix top-1 share <70%.
Action: create LAL 1%, 2-3%, 5-10% in primary country; tag with source_id.
Output: registry row {audience_id, size, source_id, created_at}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` (Python SDK) | Marketing API: audiences, ad sets, insights | `pip install facebook-business` — https://developers.facebook.com/docs/marketing-apis |
| `mozilla/node-fbsdk` | Node Marketing API client | `npm i facebook-nodejs-business-sdk` |
| `aiotg-ads` / direct `httpx` calls | Lightweight async Marketing API client when SDK is overkill | Marketing API REST docs |
| `gauntlt` + `meta-ads-cli` (community) | Bulk audience CRUD from CSV | https://github.com/CartoDB/meta-ads-cli |
| `dbt` | Build source segments in warehouse before sync | https://docs.getdbt.com |
| `Hightouch` / `Census` CLI | Reverse-ETL warehouse → Meta Custom Audiences | https://hightouch.com/docs/cli, https://docs.getcensus.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Marketing API | First-party API | Yes | Token + system user. Rate limits per app+account. |
| Meta Conversions API (CAPI) | First-party API | Yes | Required to recover post-iOS pixel loss. Pair with `event_id` dedupe. |
| Hightouch | SaaS reverse-ETL | Yes | Declarative syncs; agent can edit YAML/CLI; built-in hashing. |
| Census | SaaS reverse-ETL | Yes | Same role as Hightouch; CLI + API. |
| Segment Personas | SaaS CDP | Partial | Audience builder UI, API for sync; agent can trigger but not author segments easily. |
| Meta Ad Library | Free web tool | Read-only | Competitor audience signals; scrape via Playwright if needed. |
| Supermetrics / Funnel.io | SaaS connector | Yes | Pull insights to BQ/Sheets for performance attribution. |

## Templates & scripts
Below: idempotent custom-audience upsert via Marketing API. Hashes PII, chunks rows, returns audience id + size.

```python
import hashlib, os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience

def sha256(v: str) -> str:
    return hashlib.sha256(v.strip().lower().encode()).hexdigest()

def upsert_audience(name: str, emails: list[str], account_id: str) -> dict:
    FacebookAdsApi.init(access_token=os.environ["META_TOKEN"])
    acct = AdAccount(f"act_{account_id}")
    existing = {a["name"]: a for a in acct.get_custom_audiences(fields=["name", "id", "approximate_count_lower_bound"])}
    if name in existing:
        ca = CustomAudience(existing[name]["id"])
    else:
        ca = acct.create_custom_audience(params={
            "name": name, "subtype": "CUSTOM",
            "customer_file_source": "USER_PROVIDED_ONLY",
        })
    payload = [[sha256(e)] for e in emails if e]
    for i in range(0, len(payload), 10000):
        ca.create_user(params={"payload": {"schema": ["EMAIL_SHA256"], "data": payload[i:i+10000]}})
    refreshed = ca.api_get(fields=["approximate_count_lower_bound"])
    return {"id": ca["id"], "size_lb": refreshed["approximate_count_lower_bound"]}
```

See `templates.md` for the audience library and testing log.

## Best practices
- Hash PII client-side with the exact recipe Meta documents (lowercase, trim, SHA-256). Mismatched hashes silently drop match rate from ~70% to <10%.
- Pair every pixel event with a CAPI event using the same `event_id` for deduplication; without it, retargeting audiences halve post-iOS.
- Refresh seed audiences weekly, regenerate Lookalikes monthly. Stale LAL drifts off ICP.
- Always add a "purchasers 90-180d" exclusion to every prospecting ad set as a campaign-level default, not per ad set — humans forget; agents should enforce in code.
- Keep audience names schema-encoded: `<purpose>_<source>_<window>_<version>` (e.g. `LAL_purchasers_1pct_v3`). Lets the agent diff against a registry deterministically.
- Run Audience Overlap report before launch when running >3 ad sets in one campaign.

## AI-agent gotchas
- Marketing API errors return HTTP 200 with an error sub-object. Naive agents treat 200 as success and silently fail. Always inspect `error.code` / `error.subcode`.
- `CustomAudience` creation is async — `approximate_count_lower_bound` is `null` for up to 24h. Don't trigger LAL creation in the same run; queue it for a follow-up job.
- Special Ad Categories block lookalike + most targeting fields. The API accepts the create call then silently ignores fields. Agent must read back the audience and verify.
- Token rotation: long-lived system-user tokens still expire on permission changes. Build retry-on-190 (token expired) into the agent, but require human re-auth — never store user passwords.
- Meta deprecates targeting options without notice (e.g. detailed-targeting categories collapsed in 2022). Agent prompts that hardcode interest IDs break silently. Pin a quarterly review checkpoint where a human re-validates the targeting taxonomy.
- Don't let the agent run free on budget changes — gate any spend-affecting mutation behind a human approval step or a hard daily budget cap.

## References
- https://developers.facebook.com/docs/marketing-api/audiences
- https://developers.facebook.com/docs/marketing-api/audiences/guides/lookalike-audiences
- https://developers.facebook.com/docs/marketing-api/conversions-api
- https://www.facebook.com/business/help/633474486707199 (targeting options)
- https://www.facebook.com/business/help/1645682672415373 (Advantage+ Audience)
