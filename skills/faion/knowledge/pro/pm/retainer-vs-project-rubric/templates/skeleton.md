<!-- purpose: EngagementRubric skeleton with default dimensions -->
<!-- consumes: opportunity brief + history -->
<!-- produces: scaffold consumed by score-dimension -->
<!-- depends-on: content/01-core-rules.xml#r1-named-dimensions -->
<!-- token-budget-impact: ~140 tokens -->

# Engagement Rubric — [opportunity_id]

**Owner:** [role] / [person]
**Version:** [semver]
**Last reviewed:** YYYY-MM-DD
**Reviewers:** founder, partner

## Dimensions (4-7; anchored 1-5)

| dimension_id | name | score (1-5) | anchor_text matched | evidence |
|--------------|------|-------------|---------------------|----------|
| predictability | Predictability of work | 4 | Recurring monthly cadence | brief#cadence |
| churn_risk | Churn risk | 3 | Stakeholder change every 12mo | brief#stakeholders |
| scope_creep_risk | Scope creep risk | 2 | Out-of-SOW history | transcript |
| margin_profile | Margin profile | 4 | 28% margin | p_and_l |
| founder_fatigue | Founder fatigue impact | 5 | No personal-time overlap | calendar |

## Aggregate

- aggregate_score: SUM
- recommendation: retainer | hybrid | project | decline (per band thresholds)
