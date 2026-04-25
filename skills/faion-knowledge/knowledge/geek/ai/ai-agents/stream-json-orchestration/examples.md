# Examples — Stream-JSON Orchestration

## Example 1: Live UI for a CLI agent

A Discord bot wraps Claude Code:
- User: `/agent fix the login bug`
- Bot spawns `claude -p ... --output-format stream-json`
- Each `assistant` event becomes a Discord message edit (live updates)
- `result` event closes with the final cost

Without stream-json, the user would wait silently for 2 minutes.

## Example 2: Cost cap kills agent at $0.50

Production agent service caps each task at $0.50. Stream-json events include rolling cost estimates; orchestrator kills the subprocess the moment cumulative spend exceeds $0.50, even mid-tool-call.

Saved revenue: 12% of total spend was tasks that would have run unbounded due to bad prompts.

## Example 3: Safety veto on file delete

Orchestrator inspects every `tool_use` event:
```python
if event.type == "assistant" and is_tool_call(event):
    tool_name = extract_tool_name(event)
    if tool_name == "delete_file" and not user_approved_delete:
        kill(proc)
```

The veto fires BEFORE the deletion executes (the model's tool_use event arrives before the tool actually runs).

## Example 4: Conditional chaining (faion-cli pattern)

Stage 1 (planner Claude Code): emits a plan as final assistant message.
Orchestrator parses the plan, spawns N parallel Stage 2 agents (one per task in plan).
Each Stage 2 emits its own stream; orchestrator gathers results.
Stage 3 (reviewer) reads aggregate result, emits approval/changes.

All connected via stream-json + Python orchestrator. No SDK, no in-process complexity.

## Example 5: Telemetry to Langfuse

Each event maps to an OpenTelemetry span:
- `system/init` → root span
- `assistant` → child span "assistant_message"
- `tool_use` → child span "tool_call"
- `result` → close root span with cost/duration

Langfuse / Phoenix consumes the OTLP feed; each agent run becomes a queryable trace.

## Example 6: Anti-example — buffered output

```python
result = subprocess.run([...], capture_output=True)
events = json.loads(result.stdout)  # WRONG: stream-json is LINE-DELIMITED, not one JSON
```

Symptom: parse errors. Fix: read line-by-line as in templates.

## Example 7: opencode terminal agent

opencode (140k+ stars by April 2026) follows the same pattern. Spawn it headless, parse its stream-json, layer your own orchestration. Some teams report dropping to opencode for simpler tasks because Claude Code's tool surface is overkill.

## Example 8: Pause + resume

Stream events are inherently durable. Save them to a file. Later, resume with:
```python
session_id = events[0]["session_id"]
proc = subprocess.Popen(["claude", "--resume", session_id, ...])
```

Replay events to UI, then continue from where it left off.
