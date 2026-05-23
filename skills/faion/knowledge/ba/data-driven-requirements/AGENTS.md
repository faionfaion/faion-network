# Data-Driven Requirements Engineering

## Summary

**One-sentence:** Evidence-based requirements pipeline: every requirement anchored to a business question, quantified baseline metric, measurable success target, and instrumentation plan that closes the loop after launch.

**One-paragraph:** Replaces opinion-driven prioritization with usage/performance/business/customer metrics. Each requirement carries a business question, baseline metric, success target, instrumentation plan, and a post-launch measurement window. Prioritization uses RICE/ICE/WSJF anchored to these numbers, not stakeholder seniority. Output is a requirement record with a built-in measurement contract.

**Ефективно для:**

- Backlog prioritization з реальними usage / conversion / error rate baselines.
- Feature validation перед інвестицією — гіпотеза + success target до коду.
- Post-MVP ітерації, де треба перевірити, які flows users насправді ходять.
- AI/ML scoping з measurable business impact до тренування моделі.

## Applies If (ALL must hold)

- Prioritizing a backlog where features compete for limited capacity and ROI data is available.
- Feature validation before investment when analytics can answer the business question.
- Post-MVP iteration where product analytics reveal real flows.
- A/B test design where the requirement specifies hypothesis + outcome that declares success.
- AI/ML feature scoping where business impact (cycle time, CSAT, error rate) must be defined before model training.

## Skip If (ANY kills it)

- Greenfield products with no users and no baseline — use hypothesis-driven (Lean Startup) instead.
- Compliance/legal mandates — the mandate, not ROI, is the reason to build.
- One-off internal tooling where instrumentation cost > value.
- No analytics tooling and instrumentation out of scope — gather qualitative evidence instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Analytics tooling | GA4 / Amplitude / Mixpanel / Posthog | product analytics |
| Business question | Markdown | stakeholder |
| Baseline metric | JSON snapshot | analytics warehouse |
| Hypothesis statement | Markdown | PM / BA |
| Instrumentation budget | scope estimate | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/data-analysis` | Source the baseline metric quality. |
| `pro/ba/business-analyst/requirements-prioritization` | Consumes the quantified target → RICE/WSJF input. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `baseline-extraction` | haiku | Mechanical SQL pull from analytics warehouse. |
| `success-target-drafting` | sonnet | Light judgement on measurable target band. |
| `instrumentation-plan` | sonnet | Plan events + properties + dashboards. |
| `prioritization-scoring` | sonnet | Score against RICE/WSJF using baseline + target. |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-driven-req.md` | BR/SR record with business question + baseline + target + instrumentation + post-launch window. |
| `templates/instrumentation-plan.md` | Event + property + dashboard plan tied to the success target. |
| `templates/_smoke-test.md` | Minimum viable filled-in record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-data-driven-requirements.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[data-analysis]]
- [[requirements-prioritization]]
- [[requirements-documentation]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
