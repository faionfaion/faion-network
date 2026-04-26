"""Reference search tool with terse-default output and verbosity opt-in.

Contract:
- `format="summary"` returns one Markdown row per hit (id, ts, headline).
- `format="full"`    returns the raw record list.
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
    *,
    backend,
) -> dict:
    rows: list[LogRow] = backend.search(query, size=limit + 1)
    truncated = len(rows) > limit
    rows = rows[:limit]

    if format == "summary":
        body = "\n".join(
            f"| {r.id} | {r.ts} | {r.level} | {r.headline()} |" for r in rows
        )
        header = "| id | ts | level | msg |\n|----|----|-------|-----|"
        return {
            "format": "summary",
            "total_hits": len(rows),
            "truncated": truncated,
            "table": f"{header}\n{body}" if rows else "(no hits)",
        }

    return {
        "format": "full",
        "total_hits": len(rows),
        "truncated": truncated,
        "rows": [r.__dict__ for r in rows],
    }
