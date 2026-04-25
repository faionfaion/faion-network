# Stream-JSON Orchestration

**Category:** `cli-` (CLI vs SDK trade-offs)

## The Rule

When wrapping an agent CLI (Claude Code, Codex, Aider, opencode) as a subprocess inside a larger orchestrator, use the **stream-json output format** so the orchestrator can react MID-RUN — apply budget caps, hand off to another agent, chain conditional steps, kill on safety violations — instead of waiting for final output.

For Claude Code: `claude -p "task" --output-format stream-json --include-partial-messages`.

## Why It Works

A line-delimited JSON stream is the load-bearing format for CLI-as-subprocess orchestration. Each event (model_message, tool_use, tool_result, status) arrives as a JSON object on stdout the moment it happens. The orchestrator parses each line as-it-lands.

That gives you:
- **Budget caps**: track token spend per event; kill on threshold
- **Hand-off triggers**: detect a tool call or message pattern; route to another agent
- **Live UI**: pipe events to a dashboard
- **Conditional chaining**: "if first agent returns X, spawn second"
- **Safety stops**: detect dangerous tool call before it executes (with `--permission-mode plan` or `bash-deny-list` patterns)

Without stream-json, you wait for the agent to finish, then post-mortem.

## When To Use

- Orchestrator spawns Claude Code or Codex CLI as a subprocess (most common 2026 pattern)
- Long-running agent tasks (> 30 sec) where you want feedback
- Multi-step pipelines where step N+1 depends on signals from step N's progress
- Production agents where you want telemetry per event
- Safety/policy enforcement that must intervene mid-run

## When NOT To Use

- One-shot, short tasks (< 5 sec) — overhead of parsing isn't worth it
- When the SDK is available and gives you the same hooks more cleanly (use SDK directly)
- When you're piping stdout to a human user — pretty-print mode is more readable for direct interaction

## Event Shapes (Claude Code stream-json)

Common event types you'll see:

```jsonl
{"type":"system","subtype":"init","session_id":"...","model":"...","tools":[...]}
{"type":"assistant","message":{"role":"assistant","content":[...]}}
{"type":"user","message":{"role":"user","content":[{"type":"tool_result",...}]}}
{"type":"result","subtype":"success","total_cost_usd":0.0042,...}
```

Parse line-by-line; ignore unknown types; never assume order beyond "init" → many → "result".

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Reading agent output as one big JSON blob at end | Switch to stream-json; parse per line |
| Using regex on plain-text output to detect tool calls | Use the structured stream — robust across model versions |
| Buffering events without back-pressure | Use line-buffered reads + a queue; backpressure when downstream slow |
| Killing the agent without `--max-turns` and `--allowedTools` | Defense in depth: hard cap + allowlist + monitor stream events |
| Ignoring `result` event | Always handle the final event — that's your "done, with summary" |

## Composition

- + **subagent-as-context-firewall**: orchestrator spawns multiple Claude Code instances; each emits its own stream
- + **eval-trajectory-as-spans**: each event becomes an OTel span; trajectory is recoverable
- + **headless safety pattern**: stream-json + `-p` + `--allowedTools` + `--max-turns` + closed stdin = the canonical "safe headless agent"

## Reference Headless Pattern (the four pillars)

For headless agent runs, ALL of these matter:

1. `-p "task"` — non-interactive mode, exits when done
2. `--allowedTools "Read,Bash(npm test)"` — explicit allowlist; nothing else can run
3. `--max-turns N` — hard cap on iteration count
4. `--output-format stream-json` — observable + interruptible
5. (close stdin) — no chance of injection from a TTY

## References

- [Claude Code Headless mode docs](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
- [opencode terminal-first agent (140k stars)](https://github.com/opencode-ai/opencode)
- [Codex CLI Responses-API mode](https://github.com/openai/codex)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
