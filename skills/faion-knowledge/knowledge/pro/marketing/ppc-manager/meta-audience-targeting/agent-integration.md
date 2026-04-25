# Agent Integration — Meta Audience Targeting

## When to use
- Building full-funnel audience structures for Facebook + Instagram (cold prospecting → warm retargeting → hot cart-abandoners).
- ABM-style campaigns using Custom Audience uploads (CRM exports, intent data).
- Lookalike Audience creation from purchaser/high-LTV cohorts to scale acquisition.
- Sophisticated exclusion strategies (suppress current customers, recent purchasers, frequency-fatigued users).
- Multi-country campaigns needing per-region lookalikes.
- Compliance-restricted ads (housing, employment, credit) requiring `special_ad_categories`.

## When NOT to use
- Tiny daily budgets (<$20/day) — narrow audiences starve, broad audiences are smarter.
- Low-traffic websites (<1k visitors/month) — Custom Audience seed too small for meaningful lookalikes.
- Markets with strong privacy regulation where customer-list uploads need explicit consent (EEA — must use customer-info upload with hashed PII + consent).
- Pure brand-awareness with no funnel — broad/Advantage+ audience often beats hand-built layered targeting on Meta now.

## Where it fails / limitations
- Detailed-targeting deprecation: Meta has removed thousands of interest/behavior categories (2022-2024); agents using interest IDs from old playbooks find them invalid.
- Custom Audience match rates: 50-80% typical; below this, pixel/CRM hashing or PII coverage is broken.
- Lookalike sizing: 1% audiences in small countries (e.g., Estonia) are too small to deliver; minimum source 100 users; ideal 1000-50,000.
- Special Ad Categories: housing/credit/employment campaigns lose age, gender, ZIP-radius, and lookalike creation — entire audience playbooks invalidated.
- Audience overlap: Meta now auto-merges overlapping audiences within a campaign — manual A/B tests may not isolate variables.
- Customer File source attribute (`USER_PROVIDED_ONLY` vs `BOTH_USER_AND_PARTNER_PROVIDED`) affects compliance; misclassification triggers takedowns.
- Engagement audiences (video viewers, page engagers) only retain up to 365 days, with 180 days being the practical limit.

## Agentic workflow
A subagent owns the audience lifecycle: classify CRM segments → hash PII → upload via Customer File API → wait for size estimate → build lookalikes → set up exclusion logic across campaigns. Daily: refresh dynamic seed audiences (purchasers last 90d), check size estimates, monitor lookalike-source freshness. Human-in-loop: PII consent verification, exclusion-list approval (don't accidentally exclude prospects), Special Ad Category sign-off. Hashing must be done client-side BEFORE upload — never send raw PII to Meta.

### Recommended subagents
- A `meta-audience-builder` — orchestrates Custom Audience creation, hashing pipeline, and lookalike spawning.
- A `pii-hasher` — strict-input, validated SHA-256 normalization (lowercase, trim, country-code phone) per Meta spec.
- A `audience-overlap-auditor` — uses `delivery_estimate` + `reachestimate` endpoints to detect cannibalization across active campaigns.
- `faion-ads-agent` — owns audience and targeting-spec mutations.
- `faion-sdd-executor-agent` (existing) — runs full-funnel setup as SDD feature with acceptance gates ("3 LAL + 4 WCAs + 2 CRM lists, all >match-rate threshold").

### Prompt pattern
```
You are a Meta audience-strategy planner.
Input: business model (saas|ecom|leadgen), avg conversion volume/month, geo, AOV.
Output JSON plan:
- prospecting_audiences: [{type, source, size_estimate, rationale}]
- retargeting_audiences: [...]
- exclusions: [{audience_name, applied_to: [campaign_types]}]
- testing_priorities: ranked list
Constrain: total active audiences ≤ 12 to keep delivery learning effective.
```

```
Validate PII hashing pipeline.
Input: 5 sample rows {email, phone, fname, country}.
Output:
- normalized: lowercase, trim, phone with country code, no special chars
- hashed: SHA-256 hex of normalized values
- format: matches Meta schema [EMAIL, FN, LN, PHONE, CT, ST, ZIP, COUNTRY]
Verify against Meta's reference hashes for canonical inputs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook_business` Python SDK | Audience CRUD, lookalike creation | `pip install facebook_business` |
| `curl` + Graph API | Direct customer file upload | preinstalled |
| `openssl dgst -sha256` | PII hashing in shell pipelines | preinstalled |
| Meta Audience Insights (UI) | Manual exploration; no API equivalent | facebook.com/ads/audience-insights |
| Conversions API Gateway | Server-side event ingest tied to audience match | github.com/facebookincubator/cb-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Ads Manager | SaaS native | Yes — full API | Standard |
| Segment / Rudderstack | SaaS / OSS | Yes — destination | Streams CRM events as audience signals |
| Hightouch / Census | SaaS | Yes | Reverse ETL warehouse → Meta audiences |
| Customer.io | SaaS | Yes | Audience sync from email lists |
| Klaviyo | SaaS | Yes | E-comm: auto-syncs purchaser cohorts |
| Branch / AppsFlyer | SaaS | Yes | Mobile attribution → app-event audiences |
| Stape.io | SaaS | Yes | CAPI gateway managed service |

## Templates & scripts
The README documents full curl examples for Custom Audience creation (WCA, customer list, engagement, app activity) and Lookalike creation. See `templates.md` and `examples.md` for funnel-structure templates.

Inline PII hashing snippet (Python):

```python
# meta_hash.py
import hashlib

def normalize_email(e): return e.strip().lower()
def normalize_phone(p, country="us"): 
    digits = "".join(ch for ch in p if ch.isdigit())
    return digits if digits.startswith({"us":"1","gb":"44","de":"49"}.get(country,"")) else \
           {"us":"1","gb":"44","de":"49"}.get(country,"") + digits
def normalize_name(n): return n.strip().lower()
def sha256(v): return hashlib.sha256(v.encode()).hexdigest()

def hash_row(row):
    return {
        "EMAIL":   sha256(normalize_email(row["email"])) if row.get("email") else "",
        "PHONE":   sha256(normalize_phone(row["phone"], row.get("country","us"))) if row.get("phone") else "",
        "FN":      sha256(normalize_name(row["fname"])) if row.get("fname") else "",
        "LN":      sha256(normalize_name(row["lname"])) if row.get("lname") else "",
        "COUNTRY": sha256(row["country"].lower()) if row.get("country") else "",
    }
```

## Best practices
- Build audiences in 4 layers: cold (interest+broad), prospecting (1-3% LAL), warm (engagers, visitors), hot (cart abandoners). Run as separate ad sets, not one mixed targeting blob.
- Always exclude current customers from prospecting — saves 10-20% of budget that would otherwise re-acquire existing accounts.
- Build LALs from PURCHASERS, not just leads — quality of seed dictates quality of lookalike.
- Refresh lookalike source audiences monthly; stale seeds drift away from current ICP.
- Use the broadest viable audience for Advantage+ Shopping/PMax-equivalent campaigns; Meta's ML now outperforms manual layering for most conversion campaigns.
- Test 1%, 3%, 5% LALs with equal budgets; don't pre-pick. The "smaller is better" rule does not always hold post-iOS-14.
- For interest targeting, use 3-5 closely related interests in `flexible_spec` (OR), not nested ANDs.
- Document audience naming convention from day one (`WCA_AllVisitors_30d_50k`) — accounts hit 100+ audiences fast and become unmanageable.
- For EEA users, use the `acquisition_type=USER_PROVIDED_ONLY` and ensure consent records exist; document which list was opted-in vs. partner-acquired.

## AI-agent gotchas
- All PII must be SHA-256 hex (lowercase, no salt); using uppercase or base64 fails silently with 0 matches.
- Phone normalization spec is country-specific — agents must require `country` field, not assume US.
- Audience creation is async — `id` returned immediately, but `delivery_status` takes 1-24h. Agents must poll, not assume readiness.
- Lookalike `ratio` is a fraction (0.01 = 1%), NOT a percentage. Wrong scaling submits ratio=1.0 which means "no lookalike, just source clone" and fails validation.
- Multi-country lookalike `lookalike_spec` is an array of objects (one per country), not a single object with array fields. Easy schema bug.
- Custom Audiences from website pixel (`subtype: WEBSITE`) require an active pixel; without traffic, audience never populates and stays at 0.
- Meta API rate limits: 200 calls/hour/user for ad management; bulk audience uploads count against this.
- Audience overlap: when same user is in multiple targeted audiences, Meta charges only once but reports impressions in all. Agents counting impression sums double-count.
- Engagement audience retention is from event-fire date — agents creating audiences after a campaign ends find them empty.
- Special Ad Categories cannot be removed once a campaign is created; agents wrongly applying must delete and recreate.
- Customer File audience minimum is 100 matched users; uploads with <100 matches stay at 0 reach forever.
- Privacy: `event_sources` field requires the pixel/page/app to be in the same Business Manager; cross-BM audiences fail with vague "permissions" errors.
- Audience size estimates ARE estimates — actual delivery audience can be 30-50% smaller after Meta's relevance filters.

## References
- Meta Marketing API — Audiences: https://developers.facebook.com/docs/marketing-api/audiences/
- Custom Audience reference: https://developers.facebook.com/docs/marketing-api/audiences/reference/custom-audience/
- Customer file hashing spec: https://developers.facebook.com/docs/marketing-api/audiences/guides/customer-file-custom-audiences#hash
- Lookalike Audiences: https://www.facebook.com/business/help/164749007013531
- Special Ad Categories: https://www.facebook.com/business/help/298000447747885
- Targeting reference: https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting/
