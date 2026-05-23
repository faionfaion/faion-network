# Hybrid Delivery

## Summary

**One-sentence:** ADR for a hybrid delivery model that assigns predictive (stage-gate) or agile method per component by risk profile, with explicit translation boundaries.

**One-paragraph:** Hybrid Delivery defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Programs spanning regulated (compliance) and non-regulated (UI / integrations) components.
- Fixed-price contracts that require agile execution under predictive governance.
- Organisations migrating from pure waterfall and unable to flip the whole portfolio at once.
- Multi-vendor delivery where vendors run different methods.

## Applies If (ALL must hold)

- Program comprises >=2 components with materially different risk profiles.
- Stage-gate funding model is in effect at the program level.
- An execution PMO can enforce translation boundaries between methods.
- Components can be enumerated and tagged with risk profile.

## Skip If (ANY kills it)

- Single-component project — pure agile or pure predictive is the right call.
- Risk profile is uniform across components — hybrid adds overhead without benefit.
- No PMO authority to enforce translation boundaries — hybrid will collapse into mixed-mode chaos.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hybrid-delivery_template_fill` | haiku | Bounded template fill, no judgement. |
| `hybrid-delivery_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `hybrid-delivery_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the hybrid-delivery ADR artefact. |
| `templates/hybrid-alignment.py` | Reference script aligning component method assignment with risk profile. |
| `templates/component-map.md` | Markdown skeleton listing components with method + risk profile + boundary contracts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-delivery.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
