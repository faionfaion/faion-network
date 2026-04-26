# Checklist — Stream-JSON Orchestration

## Setup

- [ ] CLI invoked with `--output-format stream-json` (Claude Code) or equivalent
- [ ] Subprocess stdout read line-by-line (line-buffered)
- [ ] Each line parsed as JSON; bad lines logged not crashed
- [ ] Subprocess stderr captured separately for debugging
- [ ] Closed stdin (or piped from a known source) — never an open TTY

## Headless safety pillars

- [ ] `-p "task"` (or equivalent non-interactive flag)
- [ ] `--allowedTools` (or equivalent allowlist) — explicit whitelist
- [ ] `--max-turns N` — hard cap
- [ ] `--permission-mode plan` if pre-approval is wanted
- [ ] Timeout at the orchestrator level (subprocess.run timeout=)

## Event handling

- [ ] `system/init` event captured — record session_id
- [ ] `assistant` events streamed to telemetry / UI
- [ ] `user` (tool_result) events checked against budget / safety rules
- [ ] `result` event always handled — never assume the agent ran forever
- [ ] Unknown event types pass through gracefully

## Mid-run intervention

- [ ] Token-budget tracker accumulates per event; kills on overrun
- [ ] Tool-call inspector can veto specific calls (kill subprocess if unauthorized)
- [ ] Conditional chaining: at known event patterns, spawn next agent / route
- [ ] Backpressure when downstream consumer is slow

## Post-run

- [ ] Final `result` event logged with cost + duration
- [ ] Full event log persisted (replay-debugging)
- [ ] Failures categorized (timeout / budget / safety / agent error)

## Composition

- [ ] Each subagent gets its own stream (firewall pattern)
- [ ] Stream events feed eval-trajectory-as-spans for OTel
- [ ] Stream + caching + cheap-then-strong = full observability cheap loop
