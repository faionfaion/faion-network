# Methodologies Summary (Product Manager)

## Summary

**One-sentence:** Routing rubric matching observable PM-task signals (artifact, time horizon, decision shape) to the right methodology under pro/product/product-manager/.

**One-paragraph:** A deterministic triage rubric for cold-start PM tasks: given (artifact requested, time horizon, decision shape) the rubric selects exactly one methodology. Fallback is named (this methodology) so silent guessing never occurs. Output: rubric-decision JSON pointing at one slug plus rationale.

**Ефективно для:**

- Cold-start agent invocation із PM-task без pre-selected методології.
- Triage між RICE/MoSCoW, MVP/MLP, roadmap/OKR, lifecycle/feedback.
- Onboarding new PM/agent у скіл — перша орієнтаційна точка.
- Ambiguous task language: stakeholder сказав 'prioritize' без named framework.

## Applies If (ALL must hold)

- Cold start: agent has a PM task and no methodology is pre-selected.
- Task triage: deciding between RICE vs MoSCoW, MVP vs MLP, roadmap vs OKR, lifecycle vs feedback management.
- Onboarding a new PM or agent to the skill — first read to orient.
- Ambiguous task language: stakeholder said 'prioritize' or 'plan' without naming a framework.
- Multiple PM activities bundled in one request — split using the rubric before execution.

## Skip If (ANY kills it)

- Task already explicitly tagged with a methodology slug — go directly there.
- Agent inside another methodology's procedure — do not re-route mid-flow.
- Single-methodology skill where routing is trivial.
- Tasks outside the PM domain (use the appropriate domain's summary).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task description | free-form text | user / system |
| Available methodology slugs | list | this directory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Routing rubric is the entrypoint; consumes no upstream methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: deterministic routing, artifact-first, horizon-second, decision-shape-third, named fallback | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for routing-decision artefact | 750 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: silent guessing, recursive routing, horizon mismatch | 600 |
| `content/06-decision-tree.xml` | essential | Three-dimension triage: artifact -> horizon -> decision-shape | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage` | haiku | Pattern-match observable signals to candidate methodologies. |
| `fallback-explain` | sonnet | When fallback fires, explain why and propose next step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/routing-rubric.md` | Human-readable routing rubric printable card. |
| `templates/rubric-decision.json` | JSON skeleton for the routing-decision artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodologies-summary.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[continuous-discovery-habits]]
- [[experimentation-at-scale]]
- [[portfolio-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
