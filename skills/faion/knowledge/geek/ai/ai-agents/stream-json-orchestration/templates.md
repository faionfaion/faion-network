# Templates — Stream-JSON Orchestration

## Python: spawn Claude Code, parse stream

```python
import json
import subprocess

proc = subprocess.Popen(
    [
        "claude", "-p", task_prompt,
        "--output-format", "stream-json",
        "--include-partial-messages",
        "--allowedTools", "Read,Grep,Bash(npm test:*)",
        "--max-turns", "20",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.DEVNULL,
    text=True,
    bufsize=1,
)

total_cost = 0.0
for line in proc.stdout:
    line = line.strip()
    if not line:
        continue
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        log_warning(f"non-JSON line: {line!r}")
        continue

    handle_event(event)

    if event.get("type") == "result":
        total_cost = event.get("total_cost_usd", 0)
        break

    if total_cost_so_far(event) > BUDGET_USD:
        proc.kill()
        raise BudgetExceeded(f"killed at ${total_cost_so_far(event)}")
```

## Bash: pipe stream to jq

```bash
claude -p "Refactor src/auth.py" \
    --output-format stream-json \
    --allowedTools "Read,Edit" \
    --max-turns 15 \
  | jq -c 'select(.type == "assistant") | .message.content[0].text // empty'
```

Streams only assistant messages.

## Node.js: SSE-style consumption

```javascript
const { spawn } = require("child_process");
const readline = require("readline");

const proc = spawn("claude", [
    "-p", task,
    "--output-format", "stream-json",
    "--allowedTools", "Read,Grep",
    "--max-turns", "10",
]);

const rl = readline.createInterface({ input: proc.stdout });
rl.on("line", (line) => {
    const event = JSON.parse(line);
    if (event.type === "assistant") emitToUI(event);
    if (event.type === "result")    finalize(event);
});
```

## Python: budget-aware kill

```python
class BudgetWatcher:
    def __init__(self, max_usd: float):
        self.max = max_usd
        self.so_far = 0.0
    def observe(self, event: dict) -> bool:
        # Claude Code sends running totals in some events
        cost = event.get("total_cost_usd")
        if cost is not None:
            self.so_far = cost
        return self.so_far <= self.max
```

## Pattern: fan-out + collect

```python
async def parallel_agents(tasks: list[str]) -> list[dict]:
    procs = [start_claude(t) for t in tasks]
    results = await asyncio.gather(*[
        consume_stream(p) for p in procs
    ])
    return results
```

Each subprocess has its own stream; orchestrator joins their final results.

## Pattern: conditional hand-off

```python
for event in stream:
    if event["type"] == "assistant" and "REQUEST_REVIEW" in extract_text(event):
        kill(proc)
        spawn_review_agent(latest_diff())
        break
```

The first agent signals; orchestrator spawns the next one.

## Pattern: full event log for replay

```python
log = []
for event in stream:
    log.append(event)
    handle_event(event)

# After run, save for replay
with open(f"runs/{session_id}.jsonl", "w") as f:
    for e in log:
        f.write(json.dumps(e) + "\n")
```
