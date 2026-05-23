# Requirements Prioritization

## Summary

**One-sentence:** Produces a ranked requirements table using MoSCoW / RICE / WSJF with explicit per-requirement scores, weights, and rationale.

**One-paragraph:** Produces a ranked requirements table using MoSCoW / RICE / WSJF with explicit per-requirement scores, weights, and rationale. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Backlog > capacity на найближчий cycle — потрібен ranked drop-set.
- Stakeholder disagreement — empirical scoring як arbiter.
- Multi-cycle release planning, де dependencies між requirement'ами важать.
- Compliance audit — треба показати rationale за пріоритетами.

## Applies If (ALL must hold)

- Backlog exceeds team capacity for the upcoming cycle.
- Stakeholders disagree on priority — empirical scoring is needed to arbitrate.
- Multi-cycle release planning where sequencing affects dependencies.
- Compliance audit requires documented prioritisation rationale.

## Skip If (ANY kills it)

- Backlog fits in one sprint — prioritisation overhead exceeds value.
- Stakeholders have already converged informally.
- Roadmap is fixed by external constraint (contract, regulation).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements list | Output of requirements-documentation | BA |
| Effort estimates per requirement | T-shirt / story points | engineering |
| Value drivers (business value, risk reduction) | Markdown | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[requirements-documentation]] | input requirements |
| [[requirements-lifecycle]] | priority feeds the workflow state |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-requirements` | haiku | Mechanical computation of RICE / WSJF. |
| `rank-and-bucket` | sonnet | Apply MoSCoW partition on top of scores. |
| `write-rationale` | sonnet | Light judgement on phrasing per bucket. |

## Templates

| File | Purpose |
|------|---------|
| `templates/moscow-template.md` | MoSCoW prioritisation table with criteria. |
| `templates/rice-template.md` | RICE scoring matrix. |
| `templates/prio_method_and_wsjf.py` | Stdlib calculator for RICE + WSJF + MoSCoW. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-prioritization.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[requirements-documentation]]
- [[requirements-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
