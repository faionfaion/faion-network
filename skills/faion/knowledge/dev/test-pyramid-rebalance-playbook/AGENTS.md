# Test Pyramid Rebalance Playbook

## Summary

**One-sentence:** Test-shape measurement + rebalance plan: classify current shape (pyramid / ice-cream-cone / hourglass), target shape per architecture, what to delete / push down.

**One-paragraph:** Test-shape measurement + rebalance plan: classify current shape (pyramid / ice-cream-cone / hourglass), target shape per architecture, what to delete / push down. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-test-pyramid-rebalance-playbook.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- QA engineer modernизує 2018-era suite — ice-cream cone heavy E2E, anaemic unit.
- AI-augmented test ops migration (LLM-generated unit tests, mutation testing).
- Architecture shift (monolith → microservices) — pyramid shape must shift теж.
- Slow CI signal (>15 min) caused by E2E heaviness; rebalance unlocks dev velocity.

## Applies If (ALL must hold)

- Existing test suite ≥500 tests across ≥2 layers
- CI run-time observable per layer (unit vs integration vs E2E)
- Team has authority to delete redundant tests
- Target architecture is known (monolith, microservices, LLM-augmented)

## Skip If (ANY kills it)

- Greenfield project — write the right pyramid the first time
- Test suite <100 tests — rebalance overhead unjustified
- Team won't delete tests (test-coverage politics) — rebalance stalls
- Architecture in flux — rebalance to a moving target wastes effort

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
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-test-pyramid-rebalance-playbook` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-pyramid-rebalance-playbook.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[test-suite-audit-rubric]]
- [[visual-regression-baselining]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
