#!/usr/bin/env python3
# purpose: subprocess dispatcher wrapping `faion` CLI with budget + cache + PII strip + log.
# consumes: tool-defs.json schema; CLI on PATH; per-turn budget config.
# produces: structured tool-call result dict for the agent loop.
# depends-on: python 3.10 stdlib only (no extra pip).
# token-budget-impact: 0 — host code, not in the LLM context.
"""Faion CLI dispatcher for custom agents."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from dataclasses import dataclass, field

EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def strip_pii(s: str) -> str:
    s = EMAIL.sub("[email]", s)
    s = PHONE.sub("[phone]", s)
    s = CARD.sub("[card]", s)
    return s


@dataclass
class Budget:
    max_calls: int = 3
    max_content_tokens: int = 2000
    calls: int = 0
    content_tokens: int = 0


@dataclass
class Dispatcher:
    cli: str = "faion"
    cache: dict = field(default_factory=dict)
    log_sink: callable = None  # noqa: RUF013

    def log(self, **rec) -> None:
        if self.log_sink:
            self.log_sink(rec)

    def call(self, tool: str, args: dict, budget: Budget) -> dict:
        t0 = time.monotonic()
        if budget.calls >= budget.max_calls:
            return {"error": "budget_exceeded", "calls_so_far": budget.calls}
        if tool == "faion_search":
            args["query"] = strip_pii(args.get("query", ""))
        cache_key = hashlib.sha256(f"{tool}:{json.dumps(args, sort_keys=True)}".encode()).hexdigest()
        if tool == "faion_get_content" and cache_key in self.cache:
            res = self.cache[cache_key]
            self._log_call(tool, args, t0, "ok", cached=True)
            budget.calls += 1
            return res
        argv = [self.cli, tool.replace("faion_", "")]
        if tool == "faion_search":
            argv += ["--query", args["query"], "--max", str(args.get("max_results", 5))]
        elif tool == "faion_get_content":
            argv += ["--slug", args["slug"], "--file", args.get("file", "AGENTS.md")]
        try:
            p = subprocess.run(argv, capture_output=True, text=True, timeout=15, check=False)
        except subprocess.TimeoutExpired:
            self._log_call(tool, args, t0, "timeout")
            budget.calls += 1
            return {"error": "timeout"}
        if p.returncode == 0:
            res = json.loads(p.stdout)
        elif "403" in p.stderr or "tier_required" in p.stderr:
            res = {"preview": p.stdout.strip()[:200], "upgrade_to": "next-tier"}
        else:
            res = {"error": "cli_error", "detail": p.stderr.strip()[:300]}
        if tool == "faion_get_content" and "error" not in res:
            self.cache[cache_key] = res
            budget.content_tokens += min(2000, len(json.dumps(res)) // 4)
        self._log_call(tool, args, t0, "ok" if "error" not in res else "error")
        budget.calls += 1
        return res

    def _log_call(self, tool: str, args: dict, t0: float, status: str, cached: bool = False) -> None:
        self.log(
            tool_name=tool,
            args_redacted=strip_pii(json.dumps(args)),
            latency_ms=int((time.monotonic() - t0) * 1000),
            status=status,
            cached=cached,
        )
