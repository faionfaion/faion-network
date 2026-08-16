# Cost Estimation

## Summary

**One-sentence:** Bottom-up estimation: decompose WBS into work packages, apply three-point PERT, load labour with fully-loaded multiplier (1.3-1.5x), and stack risk-based contingency.

**One-paragraph:** Bottom-up estimation: decompose WBS into work packages, apply three-point PERT, load labour with fully-loaded multiplier (1.3-1.5x), and stack risk-based contingency. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-cost-estimation.py` enforces the output contract.

**Ефективно для:**

- Fixed-price proposals where margin depends on estimation accuracy.
- Capital projects requiring board-approved budget.
- Multi-vendor programs needing per-package cost transparency.
- Programs where contingency must be justified, not negotiated.

## Applies If (ALL must hold)

- WBS exists with leaf packages ≤80 hours each.
- Three estimators (or estimator + 2 reviewers) available per package.
- Fully-loaded labour rate documented per role.

## Skip If (ANY kills it)

- Top-down estimate sufficient for the decision (early concept / option screen).
- WBS not decomposed yet — decompose first.
- No risk register — contingency cannot be defended.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| WBS | indented list / dict-of-dicts | PM + tech lead |
| Labour rates by role | Currency/hour, fully-loaded | Finance / PMO |
| Risk register | YAML/CSV with probability × impact | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-integration]] | WBS is the integrator's artefact |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decompose-wbs` | sonnet | Judgement: package size + estimator fit. |
| `compute-pert` | haiku | Mechanical: (O + 4M + P) / 6 per package. |
| `size-contingency` | sonnet | Judgement: which risks ride into contingency vs accepted. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-worksheet.md.j2` | Bottom-up cost worksheet with three-point PERT per package + contingency stack |
| `templates/cost-worksheet.md` | Bottom-up cost worksheet with three-point PERT per package + contingency stack Generated from `templates/cost-worksheet.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/risk-contingency.py` | Risk register → contingency reserve via expected monetary value |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[earned-value-management]]
- [[procurement-management]]
- [[resource-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/risk-contingency.py`

```python
if __name__ == "__main__":
    pass
```
