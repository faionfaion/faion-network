# Requirements Prioritization

## Summary

**One-sentence:** Method-locked prioritization pipeline (MoSCoW / RICE / Kano / WSJF) with stakeholder weights, cost-coupled scoring, and decision-record output blocking method-shopping and HiPPO bias.

**One-paragraph:** BABOK-aligned methodology for BA-as-facilitator of multi-stakeholder prioritization. Lock the method (MoSCoW, RICE, Kano, WSJF) before scoring; couple business value with effort estimate; reject flat-priority distributions; produce a decision record with traced rationale. Output: prioritized requirement list with per-item rationale + method-version stamp.

**Ефективно для:**

- Multi-stakeholder backlog з обмеженою capacity.
- Steerco з auditable rationale.
- Cross-functional програма (FR + NFR + compliance).
- Portfolio prioritization з шаблоном матриці на N ініціатив.

## Applies If (ALL must hold)

- Multi-stakeholder backlog with limited capacity.
- Steerco needs auditable prioritization rationale.
- Cross-functional programme balancing FR + NFR + compliance.
- Portfolio prioritization with reused matrix template.
- Post-elicitation phase converging on a baseline set.

## Skip If (ANY kills it)

- Solo dev backlog where conversation suffices.
- Compliance-only programme where mandate ordering applies.
- Pure financial decisions (use NPV).
- Pre-elicitation phase — too early.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Requirements pack | Markdown / YAML | requirements-documentation |
| Stakeholder weight inputs | JSON | stakeholder-analysis |
| Effort estimates | story-points / hours | engineering |
| Method policy | Markdown | this methodology |
| Decision record template | Markdown | templates/ |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-documentation` | Pack to prioritize. |
| `pro/ba/business-analyst/decision-analysis` | Cross-method tie-breaks. |
| `pro/ba/business-analyst/data-driven-requirements` | Provides baselines for RICE scoring. |

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
| `method-lock` | haiku | Pick + lock the prioritization method. |
| `stakeholder-weight-elicitation` | sonnet | Per-stakeholder weight vectors. |
| `rice-or-moscow-scoring` | sonnet | Apply method scoring. |
| `tie-break` | opus | Cross-method tie-break with sensitivity. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prioritization-record.md` | Decision record with method + scores + rationale. |
| `templates/moscow-matrix.md` | MoSCoW matrix skeleton. |
| `templates/rice-sheet.md` | RICE scoring sheet. |
| `templates/_smoke-test.md` | Minimum filled-in record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-prioritization.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-documentation]]
- [[decision-analysis]]
- [[data-driven-requirements]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
