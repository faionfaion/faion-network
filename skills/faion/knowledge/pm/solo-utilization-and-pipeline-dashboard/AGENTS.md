# Solo Utilization & Pipeline Dashboard

## Summary

**One-sentence:** A lightweight utilization-and-pipeline dashboard that tracks billable %, realised $/hr, and pipeline coverage so a freelancer can make defensible rate-raise and capacity decisions quarterly.

**One-paragraph:** Generic `reporting-dashboards` methodologies are tool-focused (Looker / Tableau / Mode). A freelance practice doesn't need a tool — it needs the right four metrics: weekly utilization %, realised $/hr (billed revenue / total worked hours, INCLUDING admin), pipeline coverage (signed + qualified next-90d revenue / target), and rate trend over time. This methodology fixes those four, the exact formulas, and the quarterly review cadence that turns the numbers into a rate decision.

**Ефективно для:**

- Фрилансер чи solo-консультант приймає квартальні рішення про ставку та capacity.
- Команда відстежує billable %, realised $/hr, pipeline coverage без важкого PSA.
- Власник практики хоче, щоб rate-raise розмови були defensible by data, not feeling.

## Applies If (ALL must hold)

- the operator earns from billable services (T&M, fixed-price, retainer)
- the operator wants rate decisions to be defensible against their own data
- the operator already tracks hours somewhere (Toggl / Harvest / a sheet)
- engagements are long enough that pipeline coverage is meaningful (4+ weeks)

## Skip If (ANY kills it)

- revenue is product-led (SaaS / digital downloads) — utilization doesn't apply
- the operator is fully booked on a single retainer and has no pipeline to track
- a real PSA (Harvest Forecast, Float, Productive) is already in place — use it
- the operator is in a salaried role; utilization is their employer's problem

## Prerequisites

- a time-tracking habit (any tool) covering at least the last 4 weeks
- a written floor rate and target rate
- an opportunity log (signed / qualified / unqualified pipeline rows)
- a clear definition of "weekly capacity hours" (e.g., 30 billable target)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent skill |
| `pro/pm/capacity-planning-realistic` | sibling — feeds the weekly-capacity-hours input |
| `pro/marketing/rate-raise-conversation-script` | downstream — consumer of rate-trend output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-if` | sonnet | Decision tree application against typed inputs. |
| `gather-typed-inputs` | haiku | Mechanical fetch + source-pin. |
| `produce-artefact` | sonnet | Per-instance judgment; bounded inputs. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-utilization-and-pipeline-dashboard.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/solo-utilization-and-pipeline-dashboard.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-solo-utilization-and-pipeline-dashboard.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-utilization-and-pipeline-dashboard.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/project-manager`
- upstream playbook: `p3-technical-freelancer/Quarterly rate adjustment review`
- sibling: `pro/marketing/rate-raise-conversation-script`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
