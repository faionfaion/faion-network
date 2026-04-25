# Agent Integration — Google Ads API Basics

## When to use
- Programmatic Google Ads management at scale: bulk campaign edits, scheduled reports, MCC operations across 5+ accounts.
- Automating account audits (budget pacing, status checks, naming-convention enforcement).
- Wiring Google Ads data into internal dashboards, alerting, or experimentation pipelines.
- Onboarding new advertiser accounts (boilerplate campaign skeletons, tracking checks, refresh-token issuance).

## When NOT to use
- Single-account hobby spend under ~$500/month — Google Ads UI plus auto-rules is cheaper than building API plumbing.
- One-off creative/copy decisions where human judgement dominates and there's no batching benefit.
- Smart Bidding tuning during the 2–3 week learning phase — let the algorithm finish before agents start nudging bids.
- Anything that needs developer-token Standard Access if you only have Test or Basic — apply for the upgrade first.

## Where it fails / limitations
- Developer-token Basic Access caps at 15,000 ops/day; bulk migrations or hourly polling will get throttled.
- API versions deprecate every ~9 months (e.g., v17 → v18 → v19). Hard-coded version strings break agents on rollover.
- `customer.id` is NOT the same as `login_customer_id` (MCC); confusing them returns `USER_PERMISSION_DENIED`.
- Refresh tokens silently expire after 6 months of inactivity or after credential rotation — long-lived agents need re-auth flows.
- Campaign mutations require `update_mask` field paths in proto-plus; missing the mask silently drops fields.
- Cost values are `cost_micros` (1/1,000,000 of currency) — divide by `1_000_000` before display to humans.

## Agentic workflow
Run a single sub-agent that loads YAML credentials from a secrets manager, calls a thin wrapper around `GoogleAdsClient`, and emits structured JSON back to the orchestrator. Wrap every mutation in a dry-run preview that lists the diff (fields, old → new) for human approval before commit. Use GAQL search queries for read paths and batched `mutate_*` operations (≤5,000 per request) for write paths. Cache the result of `list_accessible_customers()` per session so the agent doesn't re-fetch the MCC tree on every turn.

### Recommended subagents
- `faion-ads-agent` (referenced by methodology metadata) — owns Google Ads / Meta Ads API calls, holds credentials.
- `faion-sdd-executor-agent` — wraps any change behind a quality gate when wiring into product code.
- `password-scrubber-agent` — run before commits to redact developer tokens / refresh tokens that may leak via logs.

### Prompt pattern
```
System: You are the ads-execution agent. Use GAQL for reads; never SELECT *.
        For mutations, ALWAYS produce a unified-diff preview first, then wait
        for {APPROVE|REJECT}. Treat micros correctly. Refuse if customer_id
        is missing the MCC login_customer_id when needed.
User:   Pause all keywords with >1000 impressions and 0 conversions across
        accounts [12345, 67890]. Dry-run first.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | Official Python client (proto-plus) | `pip install google-ads`, https://github.com/googleads/google-ads-python |
| Google Ads Editor | Desktop bulk edit (offline → upload) | https://ads.google.com/intl/en/home/tools/ads-editor/ |
| `gcloud` CLI | OAuth + service-account creation | https://cloud.google.com/sdk |
| `oauth2l` | Generate refresh tokens via CLI | https://github.com/google/oauth2l |
| `googleads-dotnet`, `google-ads-php`, `google-ads-ruby` | Same API, other runtimes | https://developers.google.com/google-ads/api/docs/client-libs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads API | SaaS API | Yes (REST + gRPC) | Requires developer token + OAuth refresh token. |
| Google Cloud Console | SaaS | Yes (project setup) | Where you create OAuth client IDs and service accounts. |
| Google Ads Scripts | SaaS (in-product JS) | Partial | Useful for in-platform automation when you cannot host code. |
| Supermetrics / Funnel.io | SaaS connectors | Yes (REST) | Pre-built ETL into BigQuery / Sheets if you want to skip raw API. |
| BigQuery Data Transfer Service | SaaS | Yes | Daily Google Ads schema → BQ; agents query SQL instead of GAQL. |

## Templates & scripts
See `templates.md` for credential YAML and campaign skeletons. Inline minimal sanity-check script (use as a smoke test before any agent run):

```python
# health_check.py — verify auth + MCC visibility before agent work
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def health_check(yaml_path: str) -> dict:
    client = GoogleAdsClient.load_from_storage(yaml_path)
    customer_service = client.get_service("CustomerService")
    try:
        accessible = customer_service.list_accessible_customers()
        ids = [r.split("/")[-1] for r in accessible.resource_names]
        return {"ok": True, "accessible_customer_ids": ids}
    except GoogleAdsException as ex:
        return {
            "ok": False,
            "request_id": ex.request_id,
            "errors": [e.message for e in ex.failure.errors],
        }

if __name__ == "__main__":
    import json, sys
    print(json.dumps(health_check(sys.argv[1]), indent=2))
```

## Best practices
- Pin the API version in client config (`api_version="v18"`) and bump deliberately, not implicitly.
- Use `search_stream` for any query expected to return >10k rows; the unary `search` will OOM.
- Always `SELECT` explicit fields — GAQL has no `SELECT *` and listing fewer fields cuts payload meaningfully.
- Keep MCC tree discovery out of hot paths — cache `list_accessible_customers()` result for the agent session.
- Store `developer_token`, `client_secret`, `refresh_token` in env vars or 1Password / Vault; never the YAML in repo.
- Idempotency: tag every mutation with a `tracking_url_template` parameter or label so re-runs are detectable.
- For multi-account agents, spawn one client per `login_customer_id`; mutating across MCCs in one client is error-prone.

## AI-agent gotchas
- LLMs frequently hallucinate `cost` instead of `cost_micros`; assert in code that values look right (cost > 1e6 likely already micros).
- Models confuse Google Ads API (advertising) with Google Analytics Data API (reporting) — they have separate auth and resources.
- Agents producing GAQL often forget the `WHERE segments.date BETWEEN ... AND ...` clause and pull lifetime data, blowing the quota.
- Refresh-token rotation: an agent that "fixes" auth by minting a new refresh token without revoking the old one can leave dangling credentials.
- Human-in-loop checkpoint: any `mutate_*` that touches >100 resources, changes campaign status to `ENABLED`, or modifies budget should require explicit confirmation.
- When parsing enum values from responses, use `.name` not raw int — agents otherwise emit numeric statuses ("2") to humans.

## References
- Google Ads API docs — https://developers.google.com/google-ads/api/docs/start
- google-ads-python client — https://github.com/googleads/google-ads-python
- GAQL reference — https://developers.google.com/google-ads/api/docs/query/overview
- API versioning policy — https://developers.google.com/google-ads/api/docs/release-notes
- OAuth 2.0 for Google APIs — https://developers.google.com/identity/protocols/oauth2
