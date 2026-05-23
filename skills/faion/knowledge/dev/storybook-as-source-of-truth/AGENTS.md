# Storybook as Source of Truth

## Summary

**One-sentence:** Converts Storybook into the design-system Source of Truth: story-per-state, a11y CI gate, tokens-only styling, Figma generated from Storybook.

**One-paragraph:** Converts Storybook into the design-system Source of Truth: story-per-state, a11y CI gate, tokens-only styling, Figma generated from Storybook. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-storybook-as-source-of-truth.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Shared design system на ≥2 product surfaces (web + native, або marketing + app).
- Frontend stack з Storybook 8+ та CI здатна гонити storybook build + a11y addon.
- Design tokens (Style Dictionary, design-tokens JSON, CSS custom props) визначені та консумуються компонентами.
- PR governance вже існує — Storybook lint може блокувати merge на новій a11y violation.

## Applies If (ALL must hold)

- Design system shared across ≥2 product surfaces (or planned within 1 quarter)
- Frontend with Storybook 8+ support
- Design tokens exist OR can be defined as first migration step
- CI capable of running headless story builds + a11y addon

## Skip If (ANY kills it)

- Single-app project with no plan for reuse — Storybook becomes debt without payoff
- Team owns no design tokens and cannot get them defined
- Design lead refuses to treat Storybook as SoT (Figma remains canonical)
- Compliance forbids open-source dependencies large enough to host Storybook

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
| `draft-storybook-as-source-of-truth` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | JSON instance matching the output contract |
| `templates/config.yaml` | YAML config skeleton matching the output contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-storybook-as-source-of-truth.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[wcag-severity-rubric]]
- [[visual-regression-baselining]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
