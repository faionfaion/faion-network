# Claude Code Hooks

## Summary

Claude Code hooks are user-defined shell scripts that execute synchronously at specific lifecycle events (PreToolUse, PostToolUse, UserPromptSubmit, SubagentStart, Stop, SessionStart, PreCompact, PostCompact). The core rule: always read stdin fully with `INPUT=$(cat)` as the first command and always return valid JSON on stdout — hooks that ignore stdin or emit invalid JSON break the Claude Code session.

## Why

Without hooks, Claude edits files without auto-formatting, can execute destructive git commands without safeguards, and loses session context during long runs. Hooks enforce quality gates locally at the point of execution rather than relying on developer discipline or post-hoc CI checks, and they integrate directly with the tool call lifecycle before CI ever runs.

## When To Use

- Auto-formatting code after Claude edits a file (PostToolUse + Edit/Write matcher)
- Blocking dangerous git commands before execution (PreToolUse + Bash matcher)
- Saving tmux session state during long agent runs (UserPromptSubmit, SubagentStart)
- Auto-running tests after code changes (PostToolUse + Edit matcher)
- Enforcing coding standards on every edit without manual invocation

## When NOT To Use

- Logic that belongs in CI/CD pipelines — hooks run locally and do not replace remote quality gates
- Actions taking more than 10 seconds — blocking hooks make the entire Claude session unresponsive
- Network-dependent validation (external API calls, remote test runners) — latency is unpredictable
- Operations requiring human judgment — hooks are automatic and cannot pause mid-execution
- Environments without `jq` installed — most hook patterns depend on it for JSON parsing

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Hook events, types (command/prompt), matcher syntax, stdin/stdout JSON contracts |
| `content/02-patterns.xml` | Six common hook patterns: auto-format, tmux-save, git-safety, auto-test, git-stage |
| `content/03-antipatterns.xml` | Silent stdin, invalid JSON output, missing reason in block action, settings.json corruption |

## Templates

| File | Purpose |
|------|---------|
| `templates/settings-hooks.json` | Complete settings.json with PostToolUse/PreToolUse/UserPromptSubmit/SubagentStart hooks |
| `templates/post-edit-format.sh` | Auto-format hook: Python (ruff), JS/TS (prettier), Go (gofmt), Rust (rustfmt) |
| `templates/pre-bash-safety.sh` | Safety guard: blocks force-push to main, git clean -f, rm -rf /, shutdown |
| `templates/tmux-save.sh` | Captures tmux pane content on prompt submit and subagent start |
