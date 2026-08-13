# Feature Flag Types and Lifecycle

## Summary

**One-sentence:** Classifies every flag as release / experiment / ops / permission and assigns lifecycle window: release ≤30d, experiment 1-4w, ops indefinite, permission indefinite with audit.

**One-paragraph:** Classifies every flag as release / experiment / ops / permission and assigns lifecycle window: release ≤30d, experiment 1-4w, ops indefinite, permission indefinite with audit. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Onboarding a new flag and need to decide its kind + retirement plan.
- Auditing existing flags to classify and identify cleanup candidates.
- Drafting flag policy for the team.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Onboarding a new flag and need to decide its kind + retirement plan.
- Auditing existing flags to classify and identify cleanup candidates.
- Drafting flag policy for the team.

## Skip If (ANY kills it)

- No flags in use yet — start with feature-flags-core-implementation.
- Trivial single-flag project — taxonomy is overkill.
- Managed service auto-classifies and you trust its labels.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing flag list (if any) | flags.json or service export | team |
| Owner table | user-to-flag ownership | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flags-core-implementation]] | registration + manager upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-flag` | sonnet | Map flag to kind via interview. |
| `draft-retirement-plan` | sonnet | Per-kind window + cleanup criteria. |
| `policy-document` | sonnet | Team-facing policy doc. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flag_classification.json` | Per-flag classification + retirement plan |
| `templates/policy.md` | Team flag policy: per-kind window + retirement criteria |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags-types-lifecycle.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[feature-flags-core-implementation]]
- [[feature-flags-services-testing]]
- [[feature-flags-rollout-targeting]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the flag a temporary rollout, an experiment, an operational switch, or an entitlement?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/flag_classification.json`

```json
{
  "name": "new-checkout-flow",
  "kind": "release",
  "created_at": "2026-05-01",
  "owner": "checkout-team",
  "retire_by": "2026-06-01",
  "cleanup_criteria": "100% rollout for 14 days, no rollback"
}
```
