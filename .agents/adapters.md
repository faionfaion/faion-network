# Runtime Adapters

This repo is packaged for two runtimes. Shared project rules live in the root `AGENTS.md`; runtime-specific Faion behavior lives in the adapter files below.

| Runtime | Skill adapter | Workflow adapter | Plugin manifest |
|---------|---------------|------------------|-----------------|
| Claude Code | `skills/faion/adapters/claude-code.md` | `skills/faion/workflows/adapters/claude-code.md` | `.claude-plugin/plugin.json` |
| Codex | `skills/faion/adapters/codex.md` | `skills/faion/workflows/adapters/codex.md` | `.codex-plugin/plugin.json` |

Claude Code-specific metadata (`CLAUDE.md`, `allowed-tools`, hooks) is kept for Claude compatibility. Codex should ignore it unless the Codex adapter says otherwise.

`GEMINI.md` at the repo root is a third, standalone copy of the shared project rules for Gemini-based runtimes; it is not driven by an adapter file.

## Hooks (Claude Code only)

`hooks/hooks.json` registers three `UserPromptSubmit` commands, all resolved against `${CLAUDE_PLUGIN_ROOT}`:

| Hook | Purpose |
|------|---------|
| `hooks/context-compact-gate.py` | Gate on context size before a prompt proceeds |
| `hooks/stop-improver-check.py` | Stop signal for the improver workflow |
| `hooks/quota-guard.py` | Rate-limit headroom guard |

`hooks/track-wakeup.sh` is invoked separately, not from `hooks.json`.

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
