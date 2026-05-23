# Dep Bump Batching Strategy

## Summary

**One-sentence:** Splits patch/minor/major dependency bumps into batched PRs with documented blast-radius, test gates, and rollback hooks; produces a batching plan artefact with one row per bump and a named owner.

**One-paragraph:** Splits patch/minor/major dependency bumps into batched PRs with documented blast-radius, test gates, and rollback hooks; produces a batching plan artefact with one row per bump and a named owner. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Weekly maintenance windows where 5–30 deps need bumping at once.
- Pre-release stabilisation when bump fatigue otherwise stalls the train.
- Audit-driven CVE response when patches arrive in clusters.
- Solo founders who must batch review-able PRs without a co-reviewer.

## Applies If (ALL must hold)

- Project has ≥10 third-party dependencies and a weekly or bi-weekly bump cadence.
- CI is green on `main` before the bump session starts (no carry-over regressions).
- A single named owner can take the resulting batched PRs through review.
- The dependency manifest is the source of truth (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.).

## Skip If (ANY kills it)

- One-off project with no upcoming releases — overhead does not pay back.
- No automated test suite covering the dependency surface — bumps cannot be gated.
- Mandatory same-day security CVE patch — use an emergency single-bump flow instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[blast-radius-scoring-rubric]] | upstream context this methodology builds on |
| [[changelog-automation-conventional-commits]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-dep-bump-batching-strategy-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-dep-bump-batching-strategy.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dep-bump-batching-strategy.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[blast-radius-scoring-rubric]]
- [[changelog-automation-conventional-commits]]
- [[library-evaluation-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
