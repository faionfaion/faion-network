# purpose: reference Python orchestrator for `claude -p --output-format stream-json` with budget cap, allowlist, replay log
# consumes: task prompt, allowed_tools list, max_turns, budget_cap_usd, log_dir
# produces: StreamJsonRunReport (see ../content/02-output-contract.xml) + JSONL replay log
# depends-on: stdlib (json, subprocess, pathlib, datetime, signal); no third-party deps
# token-budget-impact: ~700 tokens to render in agent context; 0 tokens at runtime (subprocess only)

from __future__ import annotations

import json
import signal
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


class BudgetExceeded(RuntimeError):
    pass


class SafetyVeto(RuntimeError):
    pass


@dataclass
class StreamHandler:
    task_prompt: str
    allowed_tools: list[str]
    max_turns: int
    budget_cap_usd: float
    log_dir: Path
    safety_predicate: Callable[[dict], bool] | None = None
    cli_path: str = "claude"

    _events_count: int = field(default=0, init=False)
    _total_cost_usd: float = field(default=0.0, init=False)
    _session_id: str = field(default="", init=False)
    _kill_reason: str | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        if not self.allowed_tools:
            raise ValueError("allowed_tools cannot be empty (defence in depth)")
        if self.max_turns < 1:
            raise ValueError("max_turns must be >= 1")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> dict:
        argv = [
            self.cli_path,
            "-p",
            self.task_prompt,
            "--output-format",
            "stream-json",
            "--include-partial-messages",
            "--allowedTools",
            ",".join(self.allowed_tools),
            "--max-turns",
            str(self.max_turns),
        ]
        started_at = datetime.now(timezone.utc).isoformat()
        tmp_log = self.log_dir / "pending.jsonl"
        result_subtype = "error_during_execution"
        with subprocess.Popen(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        ) as proc, tmp_log.open("w", encoding="utf-8") as log_file:
            assert proc.stdout is not None
            for raw_line in proc.stdout:
                line = raw_line.strip()
                if not line:
                    continue
                log_file.write(line + "\n")
                self._events_count += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "system" and event.get("subtype") == "init":
                    self._session_id = event.get("session_id", "")
                cost = event.get("total_cost_usd")
                if isinstance(cost, (int, float)):
                    self._total_cost_usd = float(cost)
                if self._total_cost_usd > self.budget_cap_usd:
                    self._kill_reason = "budget_cap"
                    self._send_kill(proc)
                    break
                if self.safety_predicate and not self.safety_predicate(event):
                    self._kill_reason = "safety_veto"
                    self._send_kill(proc)
                    break
                if event.get("type") == "result":
                    result_subtype = event.get("subtype", "success")
                    break
        ended_at = datetime.now(timezone.utc).isoformat()
        sid = self._session_id or "unknown"
        replay_path = self.log_dir / f"{sid}.jsonl"
        if tmp_log.exists():
            tmp_log.rename(replay_path)
        report = {
            "session_id": sid,
            "cli": "claude-code",
            "started_at": started_at,
            "ended_at": ended_at,
            "events_count": max(self._events_count, 1),
            "result_subtype": "killed_by_orchestrator" if self._kill_reason else result_subtype,
            "total_cost_usd": round(self._total_cost_usd, 6),
            "kill_reason": self._kill_reason,
            "replay_path": str(replay_path.relative_to(self.log_dir.parent)) if replay_path.exists() else f"runs/{sid}.jsonl",
            "allowed_tools": list(self.allowed_tools),
            "max_turns": self.max_turns,
        }
        return report

    @staticmethod
    def _send_kill(proc: subprocess.Popen[str]) -> None:
        try:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def _smoke_test() -> None:
    handler = StreamHandler(
        task_prompt="echo hi",
        allowed_tools=["Read"],
        max_turns=5,
        budget_cap_usd=0.10,
        log_dir=Path("/tmp/stream_handler_smoke"),
        cli_path="/bin/false",
    )
    report = handler.run()
    assert report["session_id"] == "unknown"
    assert report["kill_reason"] is None
    assert report["max_turns"] == 5


if __name__ == "__main__":
    _smoke_test()
