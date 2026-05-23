# Chain-of-Thought (CoT) Techniques

## Summary

**One-sentence:** Produces a selected advanced-CoT pattern (few-shot CoT, self-consistency, least-to-most, tree-of-thoughts) — config, runner, eval-lift report, cost guard.

**One-paragraph:** Zero-shot CoT solves the majority of multi-step tasks; the rest need a heavier pattern. Few-shot CoT (2-3 worked examples) anchors the model to the right reasoning shape. Self-consistency runs N=3-7 parallel paths and majority-votes the answer — increases accuracy on math/logic at NxCost. Least-to-most decomposes the problem into a strict chain of sub-questions where each answer feeds the next. Tree-of-thoughts explores branching solution paths and prunes with a value heuristic. Pick exactly one technique per call site and measure lift vs zero-shot CoT before keeping it.

**Ефективно для:** advanced math problem-solving, multi-hop logic, plan-decomposition, code-design exploration with multiple candidate paths.

## Applies If (ALL must hold)

- Zero-shot CoT measurable failure rate >10% on the task.
- Latency / cost budget tolerates Nx multiplier (self-consistency) or branching (ToT).
- An eval set exists to compare baseline CoT vs advanced CoT.
- Caller has the engineering capacity to wire branching / parallel runners.

## Skip If (ANY kills it)

- Zero-shot CoT already at target accuracy — overhead not justified.
- Reasoning model in use (Extended Thinking, o-series) — internal reasoning already covers most advanced patterns.
- High-throughput pipeline (>10 req/s per worker) — Nx cost compounds.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Baseline CoT accuracy | number | eval harness |
| Eval set | JSONL | eval harness |
| Cost / latency budget | doc | finops / SLO |
| Sample worked-reasoning examples | text | domain expert |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[cot-basics]]` | Baseline zero-shot CoT must be in place first. |
| `[[latency-vs-quality-decision-grid]]` | Picks the right pattern given the call-site SLO. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: pick-one, baseline-first, eval-lift gate, cost-guard, voting-rule for self-consistency, branch-pruning for ToT | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for cot-config.json + lift-report.json | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: cargo-cult ToT, no voting rule, leaked branches, no cost guard, no baseline | ~600 |
| `content/04-procedure.xml` | medium | 6-step: measure baseline → pick pattern → wire runner → run A/B → decide → log | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "zero-shot CoT failure rate &gt;10% AND budget allows Nx?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pick pattern | opus | Multi-axis tradeoff. |
| Author few-shot examples | opus | Quality-sensitive. |
| Run N-sample voting | runtime | Mechanical. |
| Report lift | haiku | Numerical. |

## Templates

| File | Purpose |
|---|---|
| `templates/cot-config.schema.json` | JSON Schema for cot-config.json. |
| `templates/self-consistency-runner.py` | Reference parallel runner with majority vote. |
| `templates/few-shot-cot.md` | Prompt skeleton with 2 worked examples. |
| `templates/lift-report.md` | A/B lift report template. |
| `templates/_smoke-test.json` | Minimum valid cot-config. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-cot-techniques.py` | Validates cot-config.json against schema; asserts pattern + voting rule (if self-consistency) + cost guard set. | Pre-commit on config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[cot-basics]]`
- `[[judge-calibration-protocol]]` — calibrates the verifier when self-consistency uses LLM judge

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects the pattern: low baseline-failure → skip; high failure + branching paths → ToT; high failure + sequential subproblems → least-to-most; high failure + math/logic + budget OK → self-consistency.
