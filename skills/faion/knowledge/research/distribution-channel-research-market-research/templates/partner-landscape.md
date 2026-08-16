<!-- purpose: Partner/marketplace landscape -- reach, exclusivity, take-rate per candidate partner, with confidence summary. -->
<!-- consumes: marketplace/reseller public docs + partner-portal or job-posting inferences -->
<!-- produces: Markdown partner landscape table -->
<!-- depends-on: content/01-core-rules.xml (benchmark-carries-source-year-acv-band-motion-region) -->
<!-- token-budget-impact: ~300-450 tokens when loaded as context -->

## Partner Landscape: <market_category>

**Market boundary:** <geo> + <segment> + <buyer> + <category>
**Source date:** YYYY-MM-DD

| Partner | Type | Reach | Exclusivity | Take-rate | Source | Capture date |
|---------|------|-------|-------------|-----------|--------|--------------|
| AWS Marketplace | Marketplace | L | N | 3% | AWS docs (https://...) | YYYY-MM-DD |
| Shopify App Store | Marketplace | L | N | 15-30% | Shopify docs | YYYY-MM-DD |
| Reseller X | Reseller | M | Y (region) | ~25% [INFERRED] | job post (https://...) | YYYY-MM-DD |
| SI Partner Y | SI | M | N | ~20% [INFERRED] | partner portal screenshot | YYYY-MM-DD |

**Reach:** S = <10K reach, M = 10K-100K, L = >100K
**Exclusivity:** Y = exclusive agreement known, N = non-exclusive
**Take-rate:** cite public docs for marketplace fees; mark [INFERRED] with inference path for private margins

### Confidence Summary

| Confidence | Rows |
|-----------|------|
| HIGH (public source) | X |
| [INFERRED] (job post/RFP/partner-portal) | X |
| UNKNOWN (no data yet) | X |
