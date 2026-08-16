# Strangler-Fig Migration Playbook (Vendor Delivery)

## Summary

**One-sentence:** End-to-end strangler-fig migration playbook framed for vendor delivery — slice picking, traffic shifting, fallback semantics, exit criteria.

**One-paragraph:** End-to-end strangler-fig migration playbook framed for vendor delivery — slice picking, traffic shifting, fallback semantics, exit criteria. This methodology pins the testable rules, output contract, and procedure that turn the abstract pattern into a reviewable artefact. Apply when the preconditions hold; otherwise the decision tree routes to `skip-this-methodology`. Output is the artefact described in `content/02-output-contract.xml`, validated by the bundled script.

**Ефективно для:**

- Team that needs a reusable, reviewable take on strangler-fig migration playbook (vendor delivery) for production code or operations.
- Cross-team alignment on the contract this methodology produces (no hand-rolled variants).
- Onboarding new contributors to the software-architect domain via a worked example + decision tree.
- Audit: traceable rule IDs in every conclusion of the decision tree.
- Pre-flight check before scoping a larger initiative that depends on this pattern.

## Applies If (ALL must hold)

- Task signal matches the scope of this methodology (see decision tree).
- The produced artefact has a named downstream consumer who will review it.
- Required inputs (data, repo state, infra access) are reachable when the work starts.
- The team can absorb the procedure without violating the failure-mode detectors.

## Skip If (ANY kills it)

- Task is clearly outside this methodology's scope — see `06-decision-tree.xml` for the skip branch.
- A more specific methodology already covers the exact use case better.
- The required preconditions for the failure-mode repairs cannot be met.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal | Markdown / JSON | requester |
| Parent skill context | Markdown | `pro/dev/software-architect/AGENTS.md` |
| Existing artefact (if updating) | per output-contract | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + `skip-this-methodology` rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | ~700 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-strangler-fig-playbook-vendor` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.json` | JSON skeleton for the spec artefact |
| `templates/spec.md.j2` | Markdown skeleton for the spec artefact |
| `templates/spec.md` | Markdown skeleton for the spec artefact Generated from `templates/spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strangler-fig-playbook-vendor.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/software-architect/AGENTS.md`
- Sibling methodologies: see `pro/dev/software-architect/` index

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/spec.json`

```json
{
  "monolith_inventory": [
    {
      "route_or_job_name": "GET /api/products/recs",
      "traffic_rps": 120,
      "error_rate_baseline": 0.002,
      "p99_latency_ms_baseline": 180
    }
  ],
  "slice_scoring_table": [
    {
      "slice_id": "S1",
      "coupling_depth": 2,
      "traffic_risk": 2,
      "business_priority": 4,
      "selection_order": 1
    }
  ],
  "cutover_runbook_per_slice": [
    {
      "slice_id": "S1",
      "steps": [
        {
          "command_or_action": "shift weight 10%",
          "rollback_command": "shift weight 0%"
        }
      ],
      "kill_switch_test_passed_at": "2026-05-15T10:00:00Z"
    }
  ],
  "parity_burn_in_record": {
    "window_start": "2026-05-16T00:00:00Z",
    "window_end": "2026-05-23T00:00:00Z",
    "duration_hours": 168,
    "error_rate_delta_percent": 1.2,
    "p99_latency_delta_percent": 3.5
  },
  "exit_criteria_signoff": {
    "legacy_5xx_for_7_days": true,
    "parity_within_threshold": true,
    "runbook_handed_off": true,
    "client_architect_signature_date": "2026-05-23"
  }
}
```
