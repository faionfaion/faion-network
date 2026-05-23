# IaC Module Design Patterns

## Summary

**One-sentence:** Module shape spec (config): minimal-surface inputs, typed outputs, README + examples, versioning rules, deprecation policy, validation block discipline.

**One-paragraph:** Module shape spec (config): minimal-surface inputs, typed outputs, README + examples, versioning rules, deprecation policy, validation block discipline. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Creating a new Terraform / Pulumi shared module.
- Refactoring an existing module to publish it to a registry.
- Tightening a module input surface after observation of misuse.
- Releasing a major version of a shared module.

## Skip If (ANY kills it)

- Inline single-use module that will never be reused.
- Composition of existing modules (use iac-patterns-composition instead).

**Ефективно для:**

- Shared modules що використовуються >= 3 root configs.
- Public або private module registry.
- Multi-team consumers з різними SLA.
- Modules що потребують deprecation cycles.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC tool (Terraform / Pulumi) | binary | platform team |
| Registry account / module repo | registry | platform team |
| Naming + tagging convention | doc | team |
| Required-examples directory plan | doc | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/iac-basics` | Tool + state choices. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-patterns-module-design.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[iac-patterns-composition]]
- [[iac-patterns-testing]]
- [[iac-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
