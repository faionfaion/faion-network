---
slug: definition-of-done-multi-role
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a per-role Definition-of-Done checklist (PM, BA, Dev, QA, DevOps, PdM) bound to the feature lifecycle.
content_id: "48982e7049c266a5"
complexity: medium
produces: checklist
est_tokens: 3400
tags: ["sdd", "dod", "checklist", "multi-role", "feature-lifecycle"]
---
# Definition of Done — Multi-Role

## Summary

**One-sentence:** Produces a per-role Definition-of-Done checklist (PM, BA, Dev, QA, DevOps, PdM) bound to the feature lifecycle.

**One-paragraph:** Definition of Done — Multi-Role produces a checklist that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Команди з ≥3 ролями: уникнути 'я думав ти це робиш'.
- Pre-merge gate: жодний PR не йде далі без галочок DoD per-role.
- Onboarding нового члена: чітко видно, що від нього чекають у потоці.
- Retro evidence: на retrospective показуємо, на якому пункті DoD застрягали.
- Audit/compliance: DoD як evidence для regulator.

## Applies If (ALL must hold)

- Feature is delivered by ≥2 distinct roles (PM, BA, Dev, QA, DevOps, PdM).
- Team has a merge gate that can block on checklist completion.
- Stakeholders disagree on what 'done' means across roles.

## Skip If (ANY kills it)

- Single-developer project — DoD is the developer's own checklist.
- Team already runs a working multi-role DoD with stable cadence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Role roster | Markdown / YAML | PM / tech lead |
| Feature lifecycle map | Markdown | PM |
| Existing handoff pain log | Markdown | team retro |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sdd-promotion-gate-checklist]] | DoD multi-role complements promotion gates |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-definition-of-done-multi-role` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dod-multi-role.md` | Markdown checklist with per-role rows + evidence column |
| `templates/dod.schema.json` | JSON Schema validating DoD shape |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-done-multi-role.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[sdd-promotion-gate-checklist]]
- [[release-train-coordination]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
