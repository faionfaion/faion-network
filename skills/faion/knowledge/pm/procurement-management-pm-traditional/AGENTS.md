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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[change-control]]
- [[cost-estimation]]
- [[resource-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/vendor-scoring.py`

```python
"""vendor_scoring.py — weighted vendor evaluation with sensitivity check.

Usage:
  criteria = [{"name": "Price", "weight": 0.30},
              {"name": "Experience", "weight": 0.25},
              {"name": "Technical", "weight": 0.25},
              {"name": "Timeline", "weight": 0.10},
              {"name": "References", "weight": 0.10}]
  vendors = {"Agency A": {"Price": 85, "Experience": 90, "Technical": 85,
                           "Timeline": 80, "References": 90},
             "Agency B": {"Price": 90, "Experience": 80, "Technical": 85,
                           "Timeline": 90, "References": 75}}
  print(score(criteria, vendors))
"""


def score(criteria: list[dict], vendors: dict) -> dict:
    """Score vendors; check if top-2 margin is robust to ±5% weight shifts."""
    if abs(sum(c["weight"] for c in criteria) - 1.0) > 0.01:
        raise ValueError("Weights must sum to 1.0")

    scores = {}
    for vendor, ratings in vendors.items():
        scores[vendor] = round(
            sum(c["weight"] * ratings[c["name"]] for c in criteria), 3
        )

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    margin = ranked[0][1] - ranked[1][1] if len(ranked) > 1 else 1.0

    # Sensitivity: shift each criterion weight by ±5%, see if winner flips
    flips = []
    for i, crit in enumerate(criteria):
        for delta in (+0.05, -0.05):
            adj = [
                dict(c, weight=c["weight"] + (delta if j == i else 0))
                for j, c in enumerate(criteria)
            ]
            total = sum(c["weight"] for c in adj)
            adj = [dict(c, weight=c["weight"] / total) for c in adj]
            adj_scores = {
                v: sum(c["weight"] * r[c["name"]] for c in adj)
                for v, r in vendors.items()
            }
            adj_winner = max(adj_scores, key=adj_scores.__getitem__)
            if adj_winner != ranked[0][0]:
                flips.append(f"{crit['name']} {delta:+.0%}")

    return {
        "scores": scores,
        "winner": ranked[0][0],
        "margin": round(margin, 3),
        "robust": len(flips) == 0,
        "sensitivity_flips": flips,
    }
```
