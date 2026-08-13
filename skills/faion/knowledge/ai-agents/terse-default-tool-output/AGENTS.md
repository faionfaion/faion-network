# Terse Default Tool Output, Verbosity Opt-In

## Summary

**One-sentence:** Tools default to compact summary output (one-line per hit + id + truncated flag) and accept a `format=full` opt-in with mandatory `reason`, validated by a CI envelope schema.

**One-paragraph:** Verbose-by-default tool outputs are the most common cause of context blowup in long agent loops — they bury the signal the model uses for the next step. SkillReducer (arXiv:2603.29919) reported a 2.8% absolute task-quality LIFT after compressing tool bodies ~40%. This methodology forces every list/search/query tool whose p95 output exceeds 500 tokens to default to a compact Markdown table including the primary key, expose a `format: Literal["summary","full"]` knob, always return `truncated` + `total_hits`, and require a `reason` argument when `format="full"` so raw-mode usage stays auditable.

**Ефективно для:**

- Довгі агент-loop'и: search_logs / list_files / query_db, де summary economiт по 3-5K токенів на виклик.
- MCP-агрегатори з 20+ tool'ів — без summary mode кожен виклик заливає контекст і модель плутає інструменти.
- Команди, які бачуть, що Claude/GPT агенти passують `format="full"` за замовчуванням — `reason`-аргумент зупиняє creep.
- CI-кріплення tool-контрактів: будь-який response без `truncated`+`total_hits` падає на валідаторі ще до deploy.

## Applies If (ALL must hold)

- Tool's measured p95 response token-count exceeds ~500 tokens at intended usage.
- Tool is invoked inside a multi-step agent loop where context budget is finite.
- Tool's output is used by the model to plan a next action (only IDs + a hint matter at that step).

## Skip If (ANY kills it)

- Tool's every field is load-bearing for the agent (e.g. `get_payment_invoice` for an audit task).
- Tool returns small, fixed-shape responses (`get_user(id)` returning 5 fields).
- Final-result tool at the end of the loop where the user wants the full answer rendered.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool source code | Python / TypeScript / Go | repo path |
| Sample queries | list of 20 representative inputs | recorded agent traces or query logs |
| Backend client w/ count API | function returning total-hits estimate | tool's data source (ES, DB, FS) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This is a foundational tool-design rule; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: terse-default-required, primary-key-in-summary, explicit-truncation-flag, tokens-budget-doc, full-mode-justification | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for tool-response envelope + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: summary-without-id, silent-truncation, format-full-default-creep | 700 |
| `content/04-procedure.xml` | essential | 4-step retrofit procedure measure → design → implement → wire-eval | 700 |
| `content/06-decision-tree.xml` | essential | Branches on p95-tokens + tool-role + primary-key-availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `measure_worst_case` | haiku | Token-counting + percentile math; deterministic. |
| `design_summary_shape` | sonnet | Choosing minimum useful columns needs light judgment. |
| `implement_format_knob` | haiku | Filling a known template against the schema. |
| `wire_eval_gate` | sonnet | Picking thresholds + tying to existing dashboards. |

## Templates

| File | Purpose |
|------|---------|
| `templates/search_tool.py` | Reference Python tool with `format: Literal["summary","full"]`, primary-key in summary, `reason` requirement on full, `truncated` + `total_hits` always returned. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terse-default-tool-output.py` | Validate a tool response JSON against the envelope schema | CI on each tool deploy + on captured agent traces |

## Related

- [[tool-description-as-prompt]] — tool description must declare the format modes and their token bands.
- [[verb-object-tool-naming]] — naming + namespace pair with this methodology's output shape.

## Decision tree

See `content/06-decision-tree.xml`. The tree first asks whether the tool's measured p95 response exceeds 500 tokens (skip if not), then whether the tool is a final-result or intermediate planning tool (final-result keeps full-by-default), then whether each row has a stable primary key (introduce one before applying summary mode if not). Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/search_tool.py`

```python
"""Reference search tool with terse-default output and verbosity opt-in.

Contract:
- `format="summary"` returns one Markdown row per hit (id, ts, level, headline).
- `format="full"`    returns the raw record list AND requires a `reason` argument.
- Always returns `truncated` + `total_hits` so the agent knows when to paginate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class LogRow:
    id: str
    ts: str
    level: str
    msg: str

    def headline(self) -> str:
        return self.msg[:80]


def search_logs(
    query: str,
    limit: int = 20,
    format: Literal["summary", "full"] = "summary",
    reason: str | None = None,
    *,
    backend,
) -> dict:
    rows: list[LogRow] = backend.search(query, size=limit + 1)
    truncated = len(rows) > limit
    rows = rows[:limit]
    total_hits = backend.count(query) if hasattr(backend, "count") else len(rows)

    if format == "summary":
        body = "\n".join(
            f"| {r.id} | {r.ts} | {r.level} | {r.headline()} |" for r in rows
        )
        header = "| id | ts | level | msg |\n|----|----|-------|-----|"
        return {
            "format": "summary",
            "total_hits": total_hits,
            "truncated": truncated,
            "table": f"{header}\n{body}" if rows else "(no hits)",
        }

    if not reason or len(reason) < 4:
        raise ValueError("format='full' requires non-empty `reason` argument (e.g. 'audit', 'debug', 'exact-match')")

    return {
        "format": "full",
        "total_hits": total_hits,
        "truncated": truncated,
        "rows": [{"id": r.id, "ts": r.ts, "level": r.level, "msg": r.msg} for r in rows],
        "reason": reason,
    }
```
