# Test Suite Audit Rubric

## Summary

**One-sentence:** Rubric for auditing an existing test suite on coverage / flakiness / pyramid shape / signal-time / value-per-test, producing a per-axis score and action list.

**One-paragraph:** Rubric for auditing an existing test suite on coverage / flakiness / pyramid shape / signal-time / value-per-test, producing a per-axis score and action list. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-test-suite-audit-rubric.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Onboarding на legacy product — нова QA engineer оцінює inherited suite за 1 day.
- Sprint retro де slow CI / flaky tests / coverage gaps конкурують за fix time.
- Pre-rebalance audit (input для test-pyramid-rebalance-playbook).
- Quarterly health-check суіти, де trend більш важливий ніж single snapshot.

## Applies If (ALL must hold)

- Existing test suite ≥100 tests
- CI history available (flakiness data, run-time per test)
- Coverage tooling exists (line / branch / mutation)
- Audit will drive a follow-up action list

## Skip If (ANY kills it)

- Test suite <50 tests — eyeball audit is faster
- No CI history — flakiness axis collapses to 'unknown'
- Audit will not drive action (theatrical) — skip
- Coverage tooling absent and can't be added — rubric becomes incomplete

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
| `draft-test-suite-audit-rubric` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON instance with axis scores |
| `templates/rubric.md` | Rubric skeleton with weighted axes |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-suite-audit-rubric.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[test-pyramid-rebalance-playbook]]
- [[visual-regression-baselining]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
