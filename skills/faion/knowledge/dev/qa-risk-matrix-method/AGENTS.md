# QA Risk Matrix Method

## Summary

**One-sentence:** Maintain a 2-dimensional risk matrix (impact × likelihood) per product area, score it before every release cycle, and use the scores to allocate test-investment across unit / integration / e2e / exploratory — replacing "test everything equally" with explicit priorities.

**One-paragraph:** Risk-based testing is the meta-decision that drives every other QA choice (where unit-test depth, where to invest in e2e, where to schedule exploratory sessions, what to leave to monitoring). This methodology pins how to build and maintain the matrix itself: enumerate product areas at a useful granularity (typically 8-20 areas — auth, billing, search, onboarding), score each on impact (customer-money-or-trust at stake if it breaks) and likelihood (frequency of change × complexity × novelty), produce a heatmap, then map the four quadrants to four test-investment patterns (heavy automation + exploratory, automation only, light, monitor-only). Update the matrix before every release cycle. Primary output: `risk-matrix.yaml` per project plus a quarterly heatmap + investment plan posted to the team channel.

**Ефективно для:**

- Teams with bounded QA capacity who need to defend why they invest unevenly across the product.
- Quarterly test-strategy reviews where past assumptions need to be re-anchored to current incident data.
- Products with mixed risk profiles (billing critical, search tolerant) where uniform thresholds underspend or overspend.
- Driving the per-file threshold overrides in [[qa-changed-lines-coverage-dashboard]].
- Picking which areas get exploratory sessions per [[qa-exploratory-charter-template]].

## Applies If (ALL must hold)

- Product has ≥ 5 distinct user-facing or business-critical areas.
- Team has bounded testing capacity (always; the matrix is for allocation).
- There is a release cycle where investment decisions can be reconsidered.
- Team can articulate the worst customer-impact for at least 3 product areas without prompts.

## Skip If (ANY kills it)

- Single-feature product with one user flow — risk is uniform, matrix overhead exceeds benefit.
- Pre-MVP — risk landscape is unknown, build the matrix after the first 90 days of real usage.
- Compliance environment where every area is "high risk" by mandate — risk-tier the inside of compliance buckets but defer to the regulator on the outside.
- Team has no test-investment to allocate (everything is exploratory) — adopt automation first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product-area list | YAML / markdown enumeration | engineering |
| Recent incident data (≥6 months) | postmortem log / Jira / Linear | engineering |
| Commit-churn data per area | git history | engineering |
| Impact-tier rubric | one-pager linking each score to a customer/business effect | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-changed-lines-coverage-dashboard]] | Per-file coverage overrides reflect the matrix quadrants. |
| [[qa-exploratory-charter-template]] | High-risk-high-uncertainty areas get exploratory sessions. |
| [[qa-ac-to-assertion-mapping]] | Mapping discipline is more thorough on HH-quadrant features. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + skip rule: explicit area enumeration, impact-from-customer-effect, likelihood-data-anchored, quadrant-to-investment map, per-release refresh | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for risk-matrix.yaml + investment-plan + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: enumerate areas → score impact → score likelihood → map quadrants → publish investment plan | ~800 |
| `content/05-examples.xml` | essential | Worked example: SaaS billing/search product matrix refresh | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_product_areas_from_codebase` | sonnet | Bounded extraction from module / route map. |
| `propose_impact_score_per_area` | sonnet | Per-area judgement from customer-effect framing. |
| `compute_likelihood_from_data` | haiku | Mechanical computation from incident + commit data. |
| `generate_investment_plan` | opus | Cross-area synthesis: balance capacity vs risk. |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-matrix.yaml` | Per-area scores with impact / likelihood / quadrant / investment. |
| `templates/investment-plan.md` | Quarterly investment plan: what each quadrant gets, with rationale and owner. |
| `templates/_smoke-test.json` | Minimum viable risk-matrix artefact for validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-risk-matrix-method.py` | Validate risk-matrix.yaml + investment-plan against `content/02-output-contract.xml`. | Pre-publish gate before quarterly review. |

## Related

- [[qa-changed-lines-coverage-dashboard]]
- [[qa-exploratory-charter-template]]
- [[qa-ac-to-assertion-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — area count, MVP status, compliance regime, capacity-to-allocate — onto a rule id from `content/01-core-rules.xml`. Walk it before the quarterly refresh: it catches flat-ratings and stale-matrix conditions upstream.
