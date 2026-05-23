# Bench Management Tiering

## Summary

**One-sentence:** Bench Management Tiering: codified delivery-management practice that turns the recurring 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' decision into a repeatable, auditable artefact.

**One-paragraph:** Bench Management Tiering addresses the gap identified by the p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies playbook: ops-contractor-management treats all contractors as one pool with one cadence. Real micro-agencies operate a tiered bench (rapid-call / regular / occasional / blacklist) with different rates and SLAs. There is no methodology for designing or running the tier system. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

**Ефективно для:**

- Micro-agency з тiered subcontractor bench.
- Rapid-call / regular / occasional / blacklist tiers + rates + SLAs.
- Headroom floor ≥20% spare capacity на кожному tier.
- Не стає 'agency-of-agencies' — підтримує operator-led delivery.

## Applies If (ALL must hold)

- task is an instance of p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/bench-management-tiering.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/bench-management-tiering.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bench-management-tiering.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

