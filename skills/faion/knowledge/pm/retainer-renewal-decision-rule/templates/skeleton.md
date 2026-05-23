<!-- purpose: RetainerDecision skeleton -->
<!-- consumes: per-client finance + utilisation + NPS data -->
<!-- produces: scaffold consumed by apply-thresholds -->
<!-- depends-on: content/01-core-rules.xml#r1-named-inputs -->
<!-- token-budget-impact: ~120 tokens -->

# Retainer Decision — [client_id]

**Quarter:** YYYY-Qn
**Owner:** [role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Inputs

| signal | value | source |
|--------|-------|--------|
| realised_margin_pct | 0 | finance |
| utilisation_pct | 0 | tracker |
| nps | 0 | survey |
| strategic_fit | 1 | founder-rated 1-5 |

## Thresholds (per current policy)

| threshold | value |
|-----------|-------|
| margin_min | 25 |
| utilisation_max | 90 |
| nps_min | 30 |
| strategic_fit_min | 3 |

## Decision

- **decision:** keep | upsell | renegotiate | kill
- **evidence:** [transcript URL, P&L line, NPS survey row]
- **signed_at:** YYYY-MM-DD
