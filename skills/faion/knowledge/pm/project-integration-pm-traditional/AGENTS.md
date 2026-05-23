# Project Integration Management

## Summary

**One-sentence:** PM as integrator: ensures decisions in scope/schedule/cost/quality/risk/resources/comms/procurement are consistent and mutually reinforcing via charter, baseline, status RAG.

**One-paragraph:** PM as integrator: ensures decisions in scope/schedule/cost/quality/risk/resources/comms/procurement are consistent and mutually reinforcing via charter, baseline, status RAG. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-project-integration.py` enforces the output contract.

**Ефективно для:**

- Programs with ≥4 knowledge areas in scope.
- Multi-vendor programs needing integrator authority.
- Projects where charter is the contract between Sponsor and PM.
- Status reporting that rolls up area-level signal to portfolio.

## Applies If (ALL must hold)

- Project charter is authored or being authored.
- Each knowledge area has a baseline.
- Status cadence is agreed with Sponsor.

## Skip If (ANY kills it)

- Single-area project (e.g., pure dev sprint).
- Pre-charter discovery phase.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter | Markdown | Sponsor + PM |
| Per-area baselines | scope/schedule/cost/quality/risk/resources/comms/procurement | area leads |
| Status cadence | weekly/biweekly | Sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[change-control]] | integration tracks baseline integrity via change control |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-charter` | sonnet | Judgement on charter scope + authority. |
| `integrate-baselines` | sonnet | Cross-area consistency check. |
| `roll-up-rag` | haiku | Mechanical RAG roll-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-rag.py` | Status RAG roll-up script: per-area signal → overall RAG |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-project-integration.py` | Validate the config artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[change-control]]
- [[seven-performance-domains]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

