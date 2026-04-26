# Headless CLI — Four Guards Against Mystery Hangs

## Summary

Every non-interactive run of an agent CLI (Claude Code `claude -p`, OpenAI `codex exec`, Aider `--yes`, opencode headless) MUST set four guards: (1) print/headless flag to disable the TUI, (2) explicit `--allowedTools` allowlist (NEVER `--dangerously-skip-permissions` in prod), (3) `--max-turns` cap, (4) closed stdin via `< /dev/null` so the agent cannot block waiting on user input. Missing any one of the four turns into a mystery hang or runaway-loop incident in production.

## Why

Production CIs, cron jobs, and queue workers do not have a TTY, do not have a human to approve a prompt, and do not have a sane upper bound on how many turns the agent will take. Each missing guard maps to a known failure mode: TUI mode → process hangs waiting for terminal control codes; missing allowlist → hangs on the first permission prompt OR runs unbounded tools; no max-turns → infinite agent loop drains budget; open stdin → agent reads garbage from a parent pipe and behaves erratically. The four-guards rule is the minimum viable contract for any headless agent invocation.

## When To Use

- ANY cron/CI/GitHub Actions/queue/scheduled-agent invocation of `claude`, `codex`, `aider`, or `opencode`.
- Multi-agent pipelines where one agent shells out to another.
- Background pool subagents (e.g. `/faion-poll-agents`, `claude --print` workers).
- Self-healing scripts that run unattended on a server.

## When NOT To Use

- Interactive developer sessions — the TUI and prompt-on-demand UX are the whole point; no guards required.
- One-shot smoke tests where the operator is watching the terminal and will Ctrl-C on a hang.
- Local prototyping where you actively want the model to stop and ask.

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-guards.xml` | The four guards with rationale and per-CLI flag mapping. |
| `content/02-failure-modes.xml` | What goes wrong when each guard is missing, with concrete repro shapes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/headless-guards.sh` | Reusable guarded invocation wrapper for Claude Code, Codex, Aider, opencode. |
