# Vendor Exit Cost Estimator

## Summary

**One-sentence:** Estimator for vendor/library exit cost (rewrite + data-migration + retraining + cutover) used as a dimension in vendor-eval / library-eval gates.

**One-paragraph:** Estimator for vendor/library exit cost (rewrite + data-migration + retraining + cutover) used as a dimension in vendor-eval / library-eval gates. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-vendor-exit-cost-estimator.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Architect runs vendor/library evaluation gate з multi-year horizon.
- Exit-cost is non-trivial (proprietary API, locked-in data shape, custom auth).
- Decision-maker reads cost-based artefact (a не gut-feel ranking).
- Procurement / enterprise context де lock-in risk значущий.

## Applies If (ALL must hold)

- Vendor / library evaluation gate where exit cost is non-trivial
- Multi-year horizon (≥2 years of lock-in commitment)
- Proprietary API or data-shape lock-in present
- Decision-maker treats cost-based artefacts as inputs

## Skip If (ANY kills it)

- Open-source library with multiple competing implementations — exit cheap
- Short-horizon use (≤6 months) — exit cost amortised away
- Decision-maker ignores cost-based artefacts (gut-feel buyer)
- No proprietary lock-in (clean API boundary, portable data) — estimator returns ~0

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | medium | One worked example end-to-end (filled artefact) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-vendor-exit-cost-estimator` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-exit-cost-estimator.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[vendor-eval-pilot-template]]
- [[technology-evaluation-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
