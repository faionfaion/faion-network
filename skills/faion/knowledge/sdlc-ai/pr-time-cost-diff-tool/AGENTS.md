# PR Time + Cost Diff Tool

## Summary

**One-sentence:** CI checker that estimates the latency-delta and $/req-delta a PR introduces when it touches prompts, models, context assembly, or token-budget surfaces — posted as a PR comment before review.

**One-paragraph:** AI-pipeline PRs change cost and latency invisibly: a "tiny prompt tweak" doubles tokens, a context-assembly refactor adds a 200ms RAG call, a model swap halves cost but spikes p99 latency. This methodology produces a CI checker that diff-replays the pipeline on a fixed eval set, estimates the median + p95 latency delta and the $/req delta vs main, and posts a structured report comment on the PR. Reviewers see the cost impact before they approve, not at the next monthly bill.

**Ефективно для:**

- Repo з LLM pipeline (prompts / agents / RAG) де PR можуть тихо подвоїти вартість.
- Команда з production inference cost sweep що хоче shift-left.
- Repo де PR описи не згадують cost impact — checker змушує factual diff.
- Eval-set + cost-table maintainers, які хочуть автоматизувати regression-watch.

## Applies If (ALL must hold)

- Repo runs an LLM pipeline (prompts, agents, RAG, or batch inference) in production.
- Eval set exists (≥20 representative requests) and can be replayed in CI.
- Cost table (per-model + per-token rates) is maintained and accessible to CI.
- PRs change at least one of: prompts, model id, context-assembly, token budget.

## Skip If (ANY kills it)

- No LLM pipeline — methodology has no surface.
- No eval set; rebuilding one is its own project.
- Eval-set replay cost &gt; the saving the checker enables — skip until eval cheapens.
- Pipeline is non-deterministic without a seed — replay produces noise, not signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Eval set | jsonl with `input` + `expected` | ml-engineer |
| Cost table | yaml (model → $/1k in + $/1k out + p50 latency) | platform |
| Pipeline replay script | python / shell entrypoint | ml-engineer |
| CI integration | GitHub Actions workflow | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[regression-eval-before-fix-rule]] | Eval discipline this checker reuses. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/05-examples.xml` | essential | Worked report example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pr_surface_detect` | haiku | Grep PR diff for prompt/model/context files. |
| `eval_replay_summarise` | sonnet | Summarise eval replay deltas with judgement. |
| `report_render` | haiku | Mechanical markdown render of structured report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-report.md` | PR-comment report skeleton (latency delta, $/req delta, eval pass-rate delta). |
| `templates/cost-table.yaml` | Per-model cost table format with input/output rates. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pr-time-cost-diff-tool.py` | Validate produced cost-report artefact against schema. | Pre-PR-comment posting |

## Related

- [[regression-eval-before-fix-rule]]
- [[postmortem-action-item-slo-tracking]]
- [[mr-error-tracker-draft-pr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (PR touches LLM surface? eval set exists? cost table present?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether the checker should fire on a given PR — the tree terminates either on the active rule or on `skip-this-methodology`.
