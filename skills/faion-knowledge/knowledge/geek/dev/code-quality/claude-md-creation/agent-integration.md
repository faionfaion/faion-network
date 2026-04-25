# Agent Integration — CLAUDE.md Creation

## When to use
- Bootstrapping a new repo for Claude Code: no CLAUDE.md exists and the codebase has project-specific conventions.
- Onboarding a pre-existing codebase: commands, structure, and lint rules need to be machine-readable in context.
- After significant project restructuring: existing CLAUDE.md is stale (wrong commands, removed paths).
- In multi-agent setups where multiple subagents share the same repo and need a consistent orientation doc.

## When NOT to use
- Single-file scripts or throwaway prototypes with no conventions worth capturing.
- Projects where CLAUDE.md already exists and is accurate — updating one section is not a full creation task.
- Documentation-only repos with no commands to run and no code conventions to enforce.

## Where it fails / limitations
- CLAUDE.md is loaded once at context start; updates during a session do not take effect until the next conversation.
- Context window budget is shared with CLAUDE.md; an over-long file hurts reasoning quality on code tasks.
- Agents cannot validate that commands in CLAUDE.md actually work — stale commands silently mislead future agents.
- The `@AGENTS.md` delegation pattern (faion convention) requires per-directory AGENTS.md; CLAUDE.md alone is insufficient for large monorepos.

## Agentic workflow
A subagent can scan the repo structure (glob, read key files, check package.json / Makefile / pyproject.toml) to auto-draft a CLAUDE.md. A second review pass by a Sonnet-class agent checks for completeness and staleness. For monorepos, the agent should recursively generate per-module AGENTS.md files and a root CLAUDE.md that delegates via `@<path>/AGENTS.md`.

### Recommended subagents
- `faion-sdd-executor-agent` — structured task execution that can include a "generate CLAUDE.md" step with a quality gate verifying commands run.

### Prompt pattern
```
Scan this repository. Identify: build commands, test commands, lint tools, directory structure, naming conventions, environment variables. Generate a CLAUDE.md under 150 lines following the skeleton in the methodology README.
```

```
Review the CLAUDE.md at <path>. Verify each command actually exists in Makefile/package.json/pyproject.toml. Flag stale or missing entries.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code CLI) | Reads CLAUDE.md at session start; `--print` flag to test context loading | https://docs.anthropic.com/en/docs/claude-code |
| `tree` / `find` | Scan directory structure to populate CLAUDE.md | system package |
| `jq` | Parse package.json scripts section into command list | https://jqlang.github.io/jq/ |
| `rg` (ripgrep) | Grep for Makefile targets, script invocations | https://github.com/BurntSushi/ripgrep |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Copilot | SaaS | No (IDE extension) | Reads CLAUDE.md indirectly via editor context |
| Cursor | SaaS/Electron | Partial | Has its own `.cursorrules`; CLAUDE.md ignored |
| Claude Code | OSS CLI | Yes — native | First-class consumer of CLAUDE.md |

## Templates & scripts
See templates.md for full CLAUDE.md skeleton variants (minimal, standard, monorepo).

Inline helper — extract npm scripts into CLAUDE.md commands block:
```bash
#!/usr/bin/env bash
# dump-scripts.sh — pipe into CLAUDE.md Commands section
echo "## Commands"
echo '```bash'
jq -r '.scripts | to_entries[] | "# \(.key)\n\(.value)"' package.json
echo '```'
```

## Best practices
- Keep CLAUDE.md under 200 lines; use `@path/AGENTS.md` references for modules to avoid bloat.
- Always include at least: one command to start dev, one to run tests, one to lint. These three prevent the most common agent mistakes.
- Use tables for environment variable docs; prose descriptions are too long and easy to skip.
- Never duplicate information from README.md verbatim; link to it instead — duplication creates maintenance debt.
- Version the CLAUDE.md with the project: keep it alongside code in git so agents working on branches see branch-appropriate instructions.
- For Python projects: list the ruff rule groups actually active, not just "run ruff check". Agents need to know T20 = no print() to avoid violations.
- Add a "Gotchas" section for anything that has burned a developer (or agent) before — migration order requirements, required env vars with no defaults, etc.

## AI-agent gotchas
- Claude Code loads CLAUDE.md before the first tool call; if the file references a path that doesn't exist, the agent may hallucinate what is there rather than admit the reference is broken.
- An agent generating CLAUDE.md should not commit it without a human reviewing the commands section; wrong commands cause downstream agents to fail silently on retries.
- `@AGENTS.md` delegation (faion convention) is not standard Claude Code behavior in all setups; document which version of Claude Code supports it if using across teams.
- Monorepo CLAUDE.md with dozens of `@subdir/AGENTS.md` references can exceed practical context limits; keep the root file to routing-only.
- If CLAUDE.md contains secrets (API keys accidentally included in example env tables), every agent session leaks them via context. Never include actual secret values, only variable names.

## References
- https://docs.anthropic.com/en/docs/claude-code/memory — Official CLAUDE.md memory documentation
- https://docs.anthropic.com/en/docs/claude-code/project-setup — Project setup best practices
- https://github.com/anthropics/claude-code — Claude Code source and issue tracker
