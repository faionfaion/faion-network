# FinOps — Rightsizing + Graviton Migration

## Summary

**One-sentence:** Generates a rightsizing decision-record (CPU/Memory percentile baseline → recommended size + Graviton migration) targeting 20-40% compute spend reduction with no SLO impact.

**One-paragraph:** FinOps — Rightsizing + Graviton Migration — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a decision-record that the downstream agent can verify with the included validator.

**Ефективно для:**

- EC2 / GCE / Azure VM workloads running > 4 weeks with utilization metrics available.
- Compute spend exceeds $5k/mo on the candidate workload.
- Workload is x86_64 and could run on Arm (Graviton) without source-incompatible binaries.

## Applies If (ALL must hold)

- EC2 / GCE / Azure VM workloads running > 4 weeks with utilization metrics available.
- Compute spend exceeds $5k/mo on the candidate workload.
- Workload is x86_64 and could run on Arm (Graviton) without source-incompatible binaries.

## Skip If (ANY kills it)

- Workload tightly bound to x86-only commercial software with no Arm port.
- Workload utilization data < 4 weeks — produce a longer baseline first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[fco-commitment-pricing]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (4-week-baseline-required, p95-headroom, graviton-eligibility-check, no-downsize-on-burst, a-b-rollout, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the decision-record + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fco-rightsizing` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rightsize-decision.md` | Decision record: workload + baseline + recommended size + Graviton evaluation + rollout plan |
| `templates/backup-config.example.json` | Filled decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fco-rightsizing.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[fco-commitment-pricing]]
- [[fco-cost-allocation]]
- [[fco-spot-instances]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
