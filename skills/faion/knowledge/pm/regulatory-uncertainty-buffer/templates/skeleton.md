<!-- purpose: RegulatoryBuffer skeleton with default jurisdictions -->
<!-- consumes: project scope + counsel input + jurisdiction list -->
<!-- produces: scaffold consumed by threshold-setter -->
<!-- depends-on: content/01-core-rules.xml#r1-named-inputs -->
<!-- token-budget-impact: ~150 tokens -->

# Regulatory Uncertainty Buffer — [Project]

**Owner:** [role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD

## Rules

| rule_id | jurisdiction | regulation | signal | threshold | default_action | buffer_pct | evidence |
|---------|--------------|------------|--------|-----------|----------------|------------|----------|
| eu-ai-act-annex3 | EU | AI Act 2024 | system classified Annex III high-risk | true | proceed | 30 | counsel-memo-2026-04 |
| gdpr-art22 | EU | GDPR Art 22 | automated decisions affecting individuals | true | pause | 15 | counsel-memo-2026-03 |
| dsa-vlop | EU | DSA | platform meets VLOP threshold | true | escalate_to_legal | 0 | regulator-letter-2025 |
| ccpa-1798 | US-CA | CCPA | personal info of 50000+ CA residents | true | proceed | 10 | counsel-memo-2026-02 |

<!-- Rules:
- threshold MUST be numeric or boolean (no "significant").
- default_action MUST be one of {proceed, pause, escalate_to_legal}.
- evidence MUST cite a recorded call or signed memo.
-->
