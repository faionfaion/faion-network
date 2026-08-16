# Stream-JSON Orchestration

## Summary

**One-sentence:** Wrap the agent CLI as a subprocess and react to its `stream-json` events line by line — budget, safety, hand-off — instead of waiting for the final answer.

**One-paragraph:** Produces a Python (or Node) orchestrator that spawns `claude -p --output-format stream-json --allowedTools ... --max-turns N` (or the equivalent Codex / opencode flags), reads stdout line-by-line, parses each JSON event (`system/init`, `assistant`, `user/tool_result`, `result`), and applies budget caps, safety vetoes, conditional chaining, and telemetry export — all mid-run. Defence-in-depth includes `--max-turns`, `--allowedTools`, closed stdin, and an event-log file for replay.

**Ефективно для:** довгих агентських тасків (≥30 сек) у production-orchestrator, де треба телеметрію, budget cap або safety veto в реальному часі — а не post-mortem після того, як CLI вже допрацював.

## Applies If (ALL must hold)

- Orchestrator spawns a coding-agent CLI (`claude`, `codex`, `aider`, `opencode`) as a subprocess.
- Task is expected to run ≥30 seconds or cost ≥$0.10 — long enough for mid-run reaction to matter.
- The orchestrator process can read stdout incrementally (Python `bufsize=1`, Node `readline`).
- The agent CLI supports a stream-json output mode (Claude Code does; opencode/codex have equivalents).
- Budget cap, safety veto, or conditional hand-off is a real requirement, not a nice-to-have.

## Skip If (ANY kills it)

- One-shot tasks under 5 seconds — parsing overhead exceeds value.
- The SDK is available and exposes the same hooks (in-process is cleaner; see Anthropic Agent SDK).
- Output is piped directly to a human in a terminal — pretty-print mode is more readable.
- The CLI does not have a stream-json mode (some forks omit it).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent CLI binary | executable on `$PATH` | `which claude` |
| Allowed tools list | comma-separated | risk-assessment per task |
| Per-task budget cap | float USD | product policy |
| Persistent log dir | filesystem path | infra (`runs/`) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/headless-cli-four-guards` | Defines the four mandatory CLI flags this methodology consumes. |
| `geek/ai/ai-agents/subagent-as-context-firewall` | Stream-per-subagent pattern uses this orchestrator. |
| `geek/ai/ai-agents/trajectory-eval-otel` | Stream events feed OTel spans per the GenAI conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: stream-json mandate, line-buffered read, allowedTools+max-turns, JSON-decode guard, result-event mandatory, replay log, stderr separate | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the run report: session_id, events_count, total_cost_usd, kill_reason, replay_path | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: buffered output, regex-on-plain-text, missing backpressure, no max-turns, ignoring result event | ~700 |
| `content/04-procedure.xml` | medium | Step-by-step: spawn → consume → dispatch → budget → safety veto → replay → finalize | ~900 |
| `content/05-examples.xml` | medium | 5 worked cases: Discord live UI, $0.50 cost cap, file-delete veto, conditional hand-off, OTel telemetry | ~600 |
| `content/06-decision-tree.xml` | essential | Picks the orchestrator shape from task length, budget cap, safety requirements | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate the spawn-and-parse skeleton | sonnet | Boilerplate code, deterministic. |
| Map events → OTel spans | sonnet | Mechanical translation. |
| Design the safety-veto rule set | opus | Risk judgement; opus weighs which tool calls to block. |
| Diagnose a hung stream | sonnet | Pattern-matching against known failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stream_handler.py` | Reference Python class consuming `claude -p --output-format stream-json` with budget cap, allowlist, and replay log. |
| `templates/stream-handler.node.mjs` | Same pattern in Node.js using `child_process.spawn` + `readline`. |
| `templates/jq-filter.sh` | Bash one-liner extracting only assistant messages from a stream-json file for grepping. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stream-json-orchestration.py` | Validates a run report against `02-output-contract.xml` schema. | After each orchestrator run; called by the post-run hook before persisting the report. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[headless-cli-four-guards]] — the four flags (-p, --allowedTools, --max-turns, stream-json) this methodology operationalises.
- [[subagent-as-context-firewall]] — each subagent gets its own stream; this methodology is the pipe.
- [[trajectory-eval-otel]] — stream events → OTel spans.
- [[semantic-field-naming]] — orchestrator code sees field names from the agent's tool calls; renaming pays off here too.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the orchestrator shape from three observables: task length, hard budget cap, and safety-veto requirement. Tasks ≥30s with a budget cap need the full Python class + cost tracker; tasks ≥30s without a budget but with safety vetoes need the event-dispatcher pattern; sub-5-second tasks bypass this methodology entirely and use direct SDK calls.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/stream_handler.py`

```python
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
```

### `templates/stream-handler.node.mjs`

```javascript
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { mkdir, rename, writeFile, open } from "node:fs/promises";

/**
 * @param {{
 *   taskPrompt: string,
 *   allowedTools: string[],
 *   maxTurns: number,
 *   budgetCapUsd: number,
 *   logDir: string,
 *   cliPath?: string,
 *   safetyPredicate?: (event: any) => boolean,
 * }} opts
 */
export async function runStreamHandler(opts) {
  if (!opts.allowedTools?.length) throw new Error("allowedTools cannot be empty");
  if (!opts.maxTurns || opts.maxTurns < 1) throw new Error("maxTurns must be >= 1");
  await mkdir(opts.logDir, { recursive: true });
  const startedAt = new Date().toISOString();
  const cliPath = opts.cliPath ?? "claude";
  const proc = spawn(cliPath, [
    "-p", opts.taskPrompt,
    "--output-format", "stream-json",
    "--include-partial-messages",
    "--allowedTools", opts.allowedTools.join(","),
    "--max-turns", String(opts.maxTurns),
  ], { stdio: ["ignore", "pipe", "pipe"] });

  const tmpLog = `${opts.logDir}/pending.jsonl`;
  const logHandle = await open(tmpLog, "w");
  const rl = createInterface({ input: proc.stdout });

  let eventsCount = 0;
  let totalCostUsd = 0;
  let sessionId = "";
  let killReason = null;
  let resultSubtype = "error_during_execution";

  for await (const rawLine of rl) {
    const line = rawLine.trim();
    if (!line) continue;
    await logHandle.write(line + "\n");
    eventsCount += 1;
    let event;
    try { event = JSON.parse(line); } catch { continue; }
    if (event.type === "system" && event.subtype === "init") sessionId = event.session_id ?? "";
    if (typeof event.total_cost_usd === "number") totalCostUsd = event.total_cost_usd;
    if (totalCostUsd > opts.budgetCapUsd) { killReason = "budget_cap"; proc.kill("SIGTERM"); break; }
    if (opts.safetyPredicate && !opts.safetyPredicate(event)) { killReason = "safety_veto"; proc.kill("SIGTERM"); break; }
    if (event.type === "result") { resultSubtype = event.subtype ?? "success"; break; }
  }
  await logHandle.close();
  const sid = sessionId || "unknown";
  const replayPath = `${opts.logDir}/${sid}.jsonl`;
  try { await rename(tmpLog, replayPath); } catch {}
  const endedAt = new Date().toISOString();
  return {
    session_id: sid,
    cli: "claude-code",
    started_at: startedAt,
    ended_at: endedAt,
    events_count: Math.max(eventsCount, 1),
    result_subtype: killReason ? "killed_by_orchestrator" : resultSubtype,
    total_cost_usd: Number(totalCostUsd.toFixed(6)),
    kill_reason: killReason,
    replay_path: `runs/${sid}.jsonl`,
    allowed_tools: [...opts.allowedTools],
    max_turns: opts.maxTurns,
  };
}

async function _smokeTest() {
  const report = await runStreamHandler({
    taskPrompt: "echo hi",
    allowedTools: ["Read"],
    maxTurns: 5,
    budgetCapUsd: 0.1,
    logDir: "/tmp/stream_handler_smoke_node",
    cliPath: "/bin/false",
  });
  if (report.max_turns !== 5) throw new Error("smoke test failed");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  _smokeTest().catch((e) => { console.error(e); process.exit(1); });
}
```

### `templates/jq-filter.sh`

```bash
set -euo pipefail

FILE="${1:-}"
MODE="${2:-assistant}"

if [ -z "${FILE}" ] || [ "${FILE}" = "--help" ]; then
  cat <<EOF
Usage: $0 <replay.jsonl> [assistant|tools|cost|errors|all]
  assistant   only assistant message text (default)
  tools       all tool_use events with name + input
  cost        running total_cost_usd per event
  errors      result events with non-success subtype
  all         pretty-print every event
EOF
  exit 0
fi

case "${MODE}" in
  assistant)
    jq -c 'select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text' "${FILE}"
    ;;
  tools)
    jq -c 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | {name, input}' "${FILE}"
    ;;
  cost)
    jq -c 'select(.total_cost_usd != null) | {t: .type, cost: .total_cost_usd}' "${FILE}"
    ;;
  errors)
    jq -c 'select(.type == "result" and .subtype != "success")' "${FILE}"
    ;;
  all)
    jq '.' "${FILE}"
    ;;
  *)
    echo "unknown mode: ${MODE}" >&2
    exit 2
    ;;
esac
```
