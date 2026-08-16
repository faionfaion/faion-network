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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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
| `templates/few-shot-cot.md.j2` | Prompt skeleton with 2 worked examples. |
| `templates/few-shot-cot.md` | Prompt skeleton with 2 worked examples. Generated from `templates/few-shot-cot.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/lift-report.md.j2` | A/B lift report template. |
| `templates/lift-report.md` | A/B lift report template. Generated from `templates/lift-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum valid cot-config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-cot-techniques.py` | Validates cot-config.json against schema; asserts pattern + voting rule (if self-consistency) + cost guard set. | Pre-commit on config. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[cot-basics]]`
- `[[judge-calibration-protocol]]` — calibrates the verifier when self-consistency uses LLM judge

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects the pattern: low baseline-failure → skip; high failure + branching paths → ToT; high failure + sequential subproblems → least-to-most; high failure + math/logic + budget OK → self-consistency.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cot-config.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/cot-config",
  "_purpose": "Schema for the per-call-site advanced-CoT configuration.",
  "_consumes": "operator-authored cot-config.json",
  "_produces": "validator verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "pattern",
    "cost_guard"
  ],
  "properties": {
    "pattern": {
      "enum": [
        "few-shot-cot",
        "self-consistency",
        "least-to-most",
        "tree-of-thoughts"
      ]
    },
    "few_shot_examples": {
      "type": "array"
    },
    "self_consistency": {
      "type": "object",
      "properties": {
        "n_samples": {
          "type": "integer",
          "minimum": 3,
          "maximum": 11
        },
        "voting_rule": {
          "enum": [
            "majority",
            "median",
            "llm-judge"
          ]
        }
      }
    },
    "tot": {
      "type": "object",
      "properties": {
        "branches_per_node": {
          "type": "integer",
          "minimum": 1,
          "maximum": 4
        },
        "max_depth": {
          "type": "integer",
          "minimum": 1,
          "maximum": 4
        },
        "value_fn": {
          "type": "string"
        }
      }
    },
    "cost_guard": {
      "type": "object",
      "required": [
        "max_usd_per_call"
      ],
      "properties": {
        "max_usd_per_call": {
          "type": "number",
          "exclusiveMinimum": 0
        }
      }
    }
  }
}
```

### `templates/self-consistency-runner.py`

```python
"""
from __future__ import annotations

import concurrent.futures as cf
from collections import Counter
from typing import Callable


def vote(answers: list[str], rule: str = "majority") -> str:
    if rule == "majority":
        return Counter(answers).most_common(1)[0][0]
    if rule == "median":
        nums = sorted(float(a) for a in answers)
        return str(nums[len(nums) // 2])
    raise ValueError(f"unsupported voting rule: {rule}")


def self_consistency(prompt: str, n: int, llm_call: Callable[[str], str], parse_answer: Callable[[str], str], voting_rule: str = "majority") -> dict:
    with cf.ThreadPoolExecutor(max_workers=min(n, 8)) as ex:
        samples = list(ex.map(lambda _: llm_call(prompt), range(n)))
    answers = [parse_answer(s) for s in samples]
    final = vote(answers, voting_rule)
    return {"final_answer": final, "votes": dict(Counter(answers)), "samples": samples}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum valid cot-config for self-consistency pattern.",
  "_consumes": "validate-cot-techniques.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/cot-config.schema.json",
  "_token_budget_impact": "docs-only",
  "pattern": "self-consistency",
  "self_consistency": {
    "n_samples": 5,
    "voting_rule": "majority"
  },
  "cost_guard": {
    "max_usd_per_call": 0.05
  }
}
```
