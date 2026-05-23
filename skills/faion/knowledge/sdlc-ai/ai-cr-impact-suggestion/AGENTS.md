# AI Code-Review Impact Suggestion

## Summary

**One-sentence:** Produces an AI-drafted impact-analysis comment for each PR, listing affected modules, test coverage gaps, and risk hot-spots, gated by a named reviewer.

**One-paragraph:** AI Code-Review Impact Suggestion produces a report that fixes a recurring decision in the sdlc-ai domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Per-PR impact comment, не read-after-the-fact summary.
- Test coverage gap: автоматично видно, що не покрите.
- Risk hot-spots: high-churn files у diff.
- Reviewer prep: дивиться impact перед reading diff.
- Audit: видно why we considered PR risky / safe.

## Applies If (ALL must hold)

- Repo has accessible module + dependency graph.
- PR coverage tooling exists (e.g. coverage.py / istanbul).
- Reviewer workflow accepts AI-drafted comments.

## Skip If (ANY kills it)

- Repo has no module graph or coverage tooling.
- PR is trivial (config typo / docs only) — impact analysis is overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | git diff | VCS |
| Module dependency graph | JSON / DOT | build system |
| Coverage report | JSON / lcov | test suite |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-graph-vs-diff-reviewer]] | impact suggestion uses graph reviewer signal |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-cr-impact-suggestion` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/impact-comment.md` | Markdown comment skeleton with module list + coverage + hot-spot + AI flag |
| `templates/impact.schema.json` | JSON Schema for the impact artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-cr-impact-suggestion.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[adr-ai-drafted-with-review]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
