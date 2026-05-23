# Architecture Repo Scaffolding Template

## Summary

**One-sentence:** Generates a versioned architecture repo skeleton (ADRs + diagrams + fitness functions + runbooks) ready for monthly architect review.

**One-paragraph:** Architecture Repo Scaffolding Template produces a config that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Старт нового продукту: одразу мати канонічну архітектурну директорію.
- Monthly architecture review: фіксована структура для evidence-based ревʼю.
- Onboarding інженера-архітектора: чітка карта 'що де лежить'.
- Audit prep: ADR + fitness functions discoverable за стандартним шляхом.
- Cross-team alignment: однаковий скаффолд у всіх репозиторіях організації.

## Applies If (ALL must hold)

- Team owns architecture decisions and wants them version-controlled.
- Monthly or quarterly architecture review cadence exists.
- Multiple services share architectural patterns and need a uniform repo layout.

## Skip If (ANY kills it)

- Single-developer prototype where no review cadence exists.
- Architecture is already captured in a wiki and there is no plan to migrate it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tech stack inventory | Markdown | architect |
| Review cadence policy | Markdown | architect |
| Fitness-function targets | JSON / Markdown | architect + dev lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[adr-consequence-evidence-binding]] | scaffold contains ADRs with evidence-binding shape |

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
| `draft-architecture-repo-scaffolding-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/repo-skeleton.tree` | Tree-format skeleton showing canonical dirs + sentinel files |
| `templates/cadence.yml` | Review cadence YAML with owner + next-review + evidence sources |
| `templates/ADR-0000-template.md` | MADR-style ADR template with consequence-evidence section |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-repo-scaffolding-template.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[release-train-coordination]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
