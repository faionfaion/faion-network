# Design Debt Vs Design Bet

## Summary

**One-sentence:** Per-design-task classifier: design-debt (pay-down work, must-fix, known UX bug) vs design-bet (forward-looking, hypothesis-driven, may fail) — output is a decision-record with budget envelope per class.

**One-paragraph:** Designers and solo PMs need a discipline for distinguishing pay-down design-debt work (refactors, accessibility fixes, friction-map items) from forward-looking design-bets (new patterns, speculative redesigns). This methodology produces a per-task decision-record naming the class, the success criterion (debt = friction metric improves; bet = hypothesis falsifiable in N weeks), the budget envelope (debt ≤ X% of sprint capacity; bet ≤ Y% and time-boxed). The classifier prevents bet work from masquerading as debt and debt work from masquerading as bets.

**Ефективно для:**

- Solo designer + PM with mixed debt + bet backlog.
- Indie operator deciding when to ship a redesign.
- Founder choosing between accessibility fixes and a marquee feature.
- Tech-lead allocating engineering capacity to UX work.

## Applies If (ALL must hold)

- Design tasks queue up alongside engineering work.
- Sprint capacity is constrained (solo / small team).
- There is a friction-map or UX-audit listing concrete debt items.
- Bet candidates have stated hypotheses.

## Skip If (ANY kills it)

- All design work is greenfield (no debt yet) — bets only.
- Team has a dedicated design lead who already classifies work.
- Design work is contractually fixed (e.g., regulator-driven).
- Sprint capacity has ≥40% slack — methodology adds friction without payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Friction map / UX audit | md / Figma | research repo |
| Sprint capacity estimate | hours | team calendar |
| Open design backlog | list | tracker |
| Hypothesis register | md | discovery doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/friction-to-backlog` | debt items source |
| `solo/product/demo-hypothesis-template` | bet hypothesis source |
| `solo/ux/ui-designer` | parent design operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-design-debt-vs-design-bet` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-debt-vs-design-bet.md` | Markdown skeleton for the decision-record artefact, matching content/02-output-contract.xml |
| `templates/design-debt-vs-design-bet.schema.json` | JSON Schema seed + filled fixture for the decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-debt-vs-design-bet.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[friction-to-backlog]]`
- `[[demo-hypothesis-template]]`
- `[[kano-prioritization]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
