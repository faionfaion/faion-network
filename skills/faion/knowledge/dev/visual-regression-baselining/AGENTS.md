# Visual Regression Baselining

## Summary

**One-sentence:** Visual-regression baselining playbook: capture canonical screenshots per state, diff on PR, mark intentional changes, unflake the suite by isolating variability sources.

**One-paragraph:** Visual-regression baselining playbook: capture canonical screenshots per state, diff on PR, mark intentional changes, unflake the suite by isolating variability sources. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-visual-regression-baselining.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- QA engineer unflakes / parallelizes slow E2E suite де visual diff = noise.
- Frontend з Storybook stories або Playwright/Cypress traces.
- CI infrastructure здатна store baselines (S3, GitHub Artifacts, Chromatic).
- Team має discipline mark intentional UI change vs unintended regression.

## Applies If (ALL must hold)

- E2E or Storybook suite generates screenshots per test
- CI artifact storage available (S3 / Chromatic / Percy)
- Team can review pixel diffs on PR within CI signal time
- Variability sources identifiable (fonts, animations, dates)

## Skip If (ANY kills it)

- No screenshot generation in current suite — add it first
- Team lacks discipline to mark intentional diffs — baseline churns weekly
- Pixel-perfect not a quality dimension (CLI / API product) — overhead unjustified
- Variability sources opaque (third-party iframe content) — diffs are noise

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
| `draft-visual-regression-baselining` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-visual-regression-baselining.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[storybook-as-source-of-truth]]
- [[test-pyramid-rebalance-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
