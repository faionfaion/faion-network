# Graph-Indexed vs Diff-Only AI Reviewers

## Summary

**One-sentence:** Two AI reviewer architectures (graph-indexed vs diff-only) co-exist. Pick by PR size, repo complexity, and impact-analysis need — record the decision and revisit per repo.

**One-paragraph:** Graph-Indexed vs Diff-Only AI Reviewers produces a decision-record artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Picking the right AI reviewer tool for a repo.
- Comparing CodeRabbit / Bito-style diff-only vs Greptile / Sourcegraph-style graph-indexed.
- Large monorepo where diff-only misses cross-file impact.
- Small repo where graph-indexed is over-engineered.

## Applies If (ALL must hold)

- Repo wants AI code review.
- ≥ 2 candidate tools are evaluable (one diff-only, one graph-indexed).
- Repo has the right data: > 5 PRs / week for diff-only, > 100 KLOC for graph-indexed payoff.
- Team can sign off on a decision record per repo.

## Skip If (ANY kills it)

- Repo doesn't want AI review.
- Only one tool available — no comparison needed.
- Repo too small for either to matter — human review suffices.
- Compliance forbids external code analysis tools.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool candidates | ≥ 2 reviewer tools accessible | platform |
| Eval PR set | 5-10 historical PRs to test against | lead |
| Decision-record location | ADR or .aidocs/decisions.md | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-codemod-refactor-agent]] | Reviewer evaluates codemod PRs |
| [[kb-codebase-rag-symbol-chunked]] | Graph reviewer often uses similar index |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eval_runner` | sonnet | Run both tools on eval PR set. |
| `scorecard_compile` | sonnet | Compile precision/recall/coverage. |
| `decision_record_draft` | opus | Write the ADR. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | ADR template. |
| `templates/eval-scorecard.md` | Tool comparison scorecard. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graph-vs-diff-reviewer.py` | Validate the decision-record artefact. | pre-merge of ADR |

## Related

- [[mr-codemod-refactor-agent]]
- [[lint-autofix-vs-flag-decision-rule]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
