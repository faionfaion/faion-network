# Procurement Management

## Summary

**One-sentence:** Structured vendor engagement: make-or-buy decision, Statement of Work authoring, contract type selection, vendor evaluation scoring, ongoing performance monitoring.

**One-paragraph:** Structured vendor engagement: make-or-buy decision, Statement of Work authoring, contract type selection, vendor evaluation scoring, ongoing performance monitoring. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-procurement-management.py` enforces the output contract.

**Ефективно для:**

- Selecting between in-house and external delivery on a capital program.
- Authoring SOW for a new vendor engagement.
- Multi-vendor competitive bid with weighted scoring rubric.
- Periodic vendor performance review and renewal decisions.

## Applies If (ALL must hold)

- Make-or-buy decision is open (not pre-committed by exec).
- Procurement policy + legal review path available.
- Vendor evaluation criteria can be weighted before bids open.

## Skip If (ANY kills it)

- Pre-committed vendor (no decision authority).
- Below procurement threshold (typically <$10k).
- Internal-only deliverable — use resource-management.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Make-or-buy decision criteria | Markdown | Sponsor |
| Procurement policy | PDF/Markdown | PMO / Legal |
| Evaluation weights | criterion × weight | PM + Sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[change-control]] | vendor scope changes flow through CCB |
| [[communications-management]] | vendor comms cadence |

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
| `make-or-buy` | sonnet | Judgement: cost + capability + risk. |
| `draft-sow` | sonnet | Judgement on scope + acceptance clauses. |
| `score-bids` | haiku | Mechanical weighted scoring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sow.md` | Statement of Work template with scope, deliverables, acceptance, payment schedule |
| `templates/vendor-scoring.py` | Vendor scoring script: criterion × weight × bid → normalised score |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-procurement-management.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[change-control]]
- [[cost-estimation]]
- [[resource-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

