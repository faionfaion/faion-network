# SDD Promotion Gate Checklist

## Summary

**One-sentence:** Produces binary-pass checklists that gate TWO SDD lifecycle transitions: `backlog → todo` (this methodology directly) and `in-progress → done` (delegated to the `readiness-checklist` methodology with extra quality-gate items).

**One-paragraph:** Same shape, two gates. The `backlog → todo` gate verifies canonical artefacts (spec.md always; plan.md unless trivial), evidence-linked yeses, named reviewer, blocker list. The `in-progress → done` gate delegates to readiness-checklist (10 items including conditional API tests, Playwright pos+neg, surface coupling, deploy). The decision tree routes you to the right sub-gate based on the feature's current state.

**Ефективно для:**

- Gate backlog→todo: тільки після binary-pass checklist.
- Reviewer onboarding: чіткий критерій, не gut-feel.
- Async approvals: reviewer заповнює галочки без зустрічі.
- Audit/compliance: evidence коли і чому фіча промотована.
- Velocity hygiene: блокувати недопромочені фічі від todo/.

## Applies If (ALL must hold)

- Team uses SDD lifecycle with backlog/todo/in-progress/done dirs.
- Promotion decisions are currently made informally.
- Reviewer role exists with authority to block.

## Skip If (ANY kills it)

- Team does not use SDD lifecycle.
- Project has < 10 features in backlog — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature directory | .aidocs/backlog/<feature>/ | feature author |
| Reviewer roster | YAML | PM |
| Promotion policy | Markdown | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[definition-of-done-multi-role]] | promotion gate enforces per-role DoD readiness |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |
| `content/07-done-gate.xml` | essential | in-progress → done gate delegated to readiness-checklist; conditional quality gates (API tests, Playwright pos+neg, surface coupling) | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-sdd-promotion-gate-checklist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/promotion-gate-checklist.md` | Markdown checklist with binary criteria + evidence column |
| `templates/promotion-gate.schema.json` | JSON Schema for the gate artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sdd-promotion-gate-checklist.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[definition-of-done-multi-role]]
- [[ai-assisted-specification-writing]]
- [[readiness-checklist]] — methodology consumed by the in-progress → done gate.
- [[plan-md-structure]] — defines which artefacts the backlog → todo gate checks.
- [[cr-bug-tracking]] — CR / BUG side-streams have their own lighter close-out (NOT this gate).

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
