# purpose: reference Python tool with terse-default + verbosity opt-in
# consumes: backend.search(query, size) → list[LogRow]; runtime agent call
# produces: tool response conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (terse-default-required, primary-key-in-summary, explicit-truncation-flag)
# token-budget-impact: ~30 tok/hit in summary mode; ~300-1200 tok/hit in full mode
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
