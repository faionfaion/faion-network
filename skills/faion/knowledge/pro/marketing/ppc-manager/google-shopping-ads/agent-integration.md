# Agent Integration — Google Shopping Ads

## When to use
- E-commerce brands with a structured product catalog (SKUs, GTINs, brand, category, images, price).
- Direct-response retail campaigns where shoppers compare products across vendors before buying.
- Migrating legacy Smart Shopping campaigns into modern Standard Shopping or PMax-with-feed.
- Scenarios needing per-product bid control (Standard Shopping) — PMax cannot do this.
- Multi-country expansion with localized feeds (per-country language, currency, shipping).

## When NOT to use
- Lead-gen, services, B2B, info-products — Shopping requires a product feed and physical/digital good.
- Catalogs <50 SKUs — overhead of feed maintenance > value.
- Items violating Google policies (supplements, weapons, certain apparel) — feed disapprovals stall everything.
- Inventory turning over weekly with no ERP-driven feed — stale price/availability triggers Merchant Center suspension.

## Where it fails / limitations
- Merchant Center suspensions (misrepresentation, policy, price/availability mismatch) effectively zero out Shopping until appealed — appeals can take 1-3 weeks.
- Feed quality dictates 80% of performance: poor titles/categories = no impressions regardless of bids.
- Shopping has no headlines or descriptions — you compete on title, price, image. Less creative leverage than Search.
- API for Merchant Center (Content API for Shopping) is separate from Google Ads API; agents need both with separate auth flows.
- Shopping campaigns use product IDs not keywords; "negative keywords" exist but are limited; product partitions (listing groups) are the real targeting tool.
- PMax is silently consuming Standard Shopping budget where both run in same account on same products — priority settings matter.

## Agentic workflow
A subagent owns the full feed-to-campaign loop: ingest product catalog → transform to Google feed schema → upload via Content API → monitor disapprovals/warnings → create campaign + ad-group + product partitions → daily product-performance audit → bid by product cluster. Human-in-loop: title/description rewrites for low-impression products, policy-disapproval appeals, target ROAS changes. Critical pre-flight: validate feed BEFORE creating campaigns — campaigns referencing a broken feed waste setup time.

### Recommended subagents
- A `merchant-center-feed-builder` subagent — pulls from Shopify/Magento/PIM, transforms to GMC schema, validates required attributes, uploads via Content API.
- A `shopping-feed-doctor` — daily audit: list disapprovals, classify (title issue / image issue / GTIN missing / price mismatch), propose fix, queue for human approval.
- `faion-ads-agent` — owns campaign + partition + bidding ops via Google Ads API.
- `faion-sdd-executor-agent` (existing) — runs feed migration as SDD task with QA gates ("0 disapprovals on 95% of SKUs").

### Prompt pattern
```
You are a Shopping title optimizer.
Input: SKU rows {id, current_title, brand, category, attributes}.
Generate optimized titles ≤150 chars following pattern:
[Brand] [Product Type] [Color/Size/Material] [Model/Variant] [Key Feature]
Avoid promotional copy ("BEST", "SALE"), all-caps, and special chars.
Output: {sku_id, new_title, rationale, confidence: 0-1}.
```

```
Diagnose Merchant Center disapprovals.
Input: GMC item-level issues report.
For each issue: {issue_code, affected_sku, recommended_action, can_auto_fix: bool}.
Auto-fixable: missing GTIN, image too small, currency missing.
Manual: misrepresentation, restricted product, price mismatch.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | Shopping campaign + partition ops | `pip install google-ads` |
| Content API for Shopping (Python client) | Feed upload, item insertion, account ops | `pip install google-api-python-client` |
| `gcloud` BigQuery transfer | Daily import of Shopping performance + feed status | cloud.google.com/bigquery-transfer |
| Google Ads Editor | Bulk Shopping product-group edits offline | ads.google.com/intl/en/home/tools/ads-editor |
| Feedonomics CLI / API | Feed transformation as a service | feedonomics.com |
| `xmllint` / `jq` | Validate XML / JSON feeds before upload | OS package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Merchant Center | SaaS native | Yes — Content API | Required platform |
| Shopify Google channel | SaaS | Yes — auto-feed | Auto-syncs catalog to GMC |
| WooCommerce Product Feed Pro | OSS plugin | Limited | Generates feed file; agent fetches |
| Feedonomics | SaaS | Yes — API | Enterprise feed management |
| DataFeedWatch | SaaS | Yes — API | Feed transformation rules |
| Channable | SaaS | Yes — API | Multi-channel feeds (Google, Bing, Meta, TikTok) |
| Productsup | SaaS | Yes | Enterprise PIM/feed |
| Adriel / Triple Whale | SaaS | Yes | Performance reporting + ROAS |

## Templates & scripts
The README contains drop-in functions for `create_shopping_campaign`, `create_product_ad_group`, `create_product_partition`, and `get_shopping_product_report`. See `templates.md` and `examples.md` for setup variants.

Inline feed-validator example (Content API):

```python
# feed_status_audit.py
from googleapiclient.discovery import build
from google.oauth2 import service_account

def audit_feed(merchant_id, sa_path):
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=["https://www.googleapis.com/auth/content"])
    svc = build("content", "v2.1", credentials=creds)
    req = svc.productstatuses().list(merchantId=merchant_id, maxResults=250)
    issues = {"disapproved": [], "warnings": []}
    while req:
        resp = req.execute()
        for p in resp.get("resources", []):
            for d in p.get("destinationStatuses", []):
                if d.get("status") == "disapproved":
                    issues["disapproved"].append({"sku": p["productId"],
                                                   "issues": p.get("itemLevelIssues", [])})
        req = svc.productstatuses().list_next(req, resp)
    return issues
```

## Best practices
- Treat the feed as the campaign — 80% of optimization is feed quality (titles, images, categories), not bids.
- Front-load the most search-relevant terms in the first 60 chars of the product title (mobile truncation).
- Use Google Product Category + GTIN — both materially improve impression eligibility.
- Structure campaigns by product margin tier or category, not arbitrarily — bidding strategy needs clusters with similar ROAS targets.
- Use campaign priority (Low/Medium/High) when running multiple Shopping campaigns over the same SKUs to control inventory overlap.
- Negative keywords at campaign level for brand-vs-non-brand split.
- Run the feed through GMC's "Diagnostics" daily; small per-SKU issues snowball into account suspensions.
- Update price/availability at least daily; ideally via real-time feed updates (Content API `products.insert` with `price.value`).
- Don't pause and unpause Shopping campaigns frequently — disrupts auction history.

## AI-agent gotchas
- Two separate APIs: Content API (Merchant Center) uses different auth scopes than Google Ads API; agents must manage two service-account credentials.
- Product IDs in Content API are hex IDs like `online:en:US:SKU123` — NOT just the SKU; agents must construct full ID with channel/locale/country prefix.
- `customer_id` in Google Ads (PMax/Shopping campaigns) ≠ `merchant_id` in Content API — use both, don't conflate.
- Shopping campaign `shopping_setting.merchant_id` is required at creation; cannot be added later.
- Listing group (product partition) trees must be MECE — every SKU in exactly one node. Agents creating partitions must always end with an "everything else" subdivision or campaign won't run.
- Image hashes are case-sensitive and trailing whitespace breaks them.
- GMC suspension can cascade: one critical policy issue suspends the entire account, taking down PMax + Shopping simultaneously.
- Feed upload is async; `productstatuses.get` reflects current state, not the just-uploaded state for ~30 min.
- API quota: Content API has separate quota from Google Ads API; bulk feed uploads can starve campaign-management calls.
- Currency micros: `price.value` is a string like "29.99" with separate `price.currency`; NOT micros like Google Ads.
- Multi-country campaigns: each country requires its own feed and shipping settings; agents must verify shipping coverage per country before launching.

## References
- Content API for Shopping: https://developers.google.com/shopping-content/guides/quickstart
- Google Ads API Shopping campaigns: https://developers.google.com/google-ads/api/docs/campaigns/shopping/overview
- Product data spec: https://support.google.com/merchants/answer/7052112
- Feed best practices: https://support.google.com/merchants/answer/188494
- Product partitions reference: https://developers.google.com/google-ads/api/docs/shopping-ads/product-partition-trees
- GMC policy guidelines: https://support.google.com/merchants/topic/7259406
