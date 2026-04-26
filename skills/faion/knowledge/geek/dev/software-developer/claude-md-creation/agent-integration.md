# Agent Integration — CLAUDE.md Creation (Software Developer Perspective)

## When to use
- Starting a new project where Claude Code will be the primary AI assistant; no CLAUDE.md exists.
- Inheriting a codebase and needing to orient Claude Code to existing conventions before making changes.
- After a major dependency upgrade or framework migration that invalidates existing instructions.
- Setting up per-module CLAUDE.md files in a monorepo where different modules have different stacks and commands.

## When NOT to use
- Throwaway scripts, one-off data migrations, or single-file utilities with no ongoing AI-assisted development.
- Projects where team policy prohibits AI coding tools entirely — writing CLAUDE.md wastes effort.
- When an accurate CLAUDE.md already exists for the project — update specific sections rather than recreating from scratch.

## Where it fails / limitations
- CLAUDE.md is a static snapshot; it goes stale as projects evolve. A 6-month-old CLAUDE.md with wrong commands misleads more than it helps.
- Claude Code reads CLAUDE.md at session start; a 300+ line file consumes context budget that could be used for code.
- Per-directory CLAUDE.md files (faion convention: `@AGENTS.md`) require each directory to maintain its own file — maintenance burden scales with repo size.
- There is no automated test that verifies CLAUDE.md commands are valid; stale commands fail silently for agents.

## Agentic workflow
An agent can auto-generate an initial CLAUDE.md by reading `package.json`, `Makefile`, `pyproject.toml`, `.env.example`, and directory structure, then filling in the standard skeleton. A follow-up agent validates the output by dry-running each command listed (in a safe environment) and flagging any that error. For monorepos following the faion convention, the agent generates root CLAUDE.md (`@AGENTS.md`) plus per-module AGENTS.md files with 20-80 line summaries.

### Recommended subagents
- `faion-sdd-executor-agent` — includes a CLAUDE.md generation/validation step as part of project initialization tasks.

### Prompt pattern
```
Read package.json, Makefile (if present), and the top-level directory structure. Generate a CLAUDE.md for this project using the standard skeleton: Overview (1 paragraph), Tech Stack (table), Commands (bash blocks for dev/test/lint/build), Structure (directory tree, 2 levels), Conventions (naming, imports, types), Key Files (table). Keep total length under 150 lines.
```

```
Review CLAUDE.md. For each command listed under Commands, verify it exists in package.json scripts or Makefile. For any command that cannot be verified, mark it [UNVERIFIED]. For any directory listed under Structure that doesn't exist, mark it [MISSING].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Consumes CLAUDE.md at session start; test with `claude --print "what commands does this project have?"` | https://docs.anthropic.com/en/docs/claude-code |
| `tree -L 2` | Generate directory tree for Structure section | system package |
| `jq '.scripts' package.json` | Extract npm scripts for Commands section | https://jqlang.github.io/jq/ |
| `make -qp` | List all Makefile targets | system package |
| `python -m poetry show` | List Python project dependencies for Tech Stack section | https://python-poetry.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | OSS CLI | Yes — native | Direct consumer; use `claude --print` to test context loading |
| GitHub Copilot Workspace | SaaS (preview) | Partial | Has its own context system; CLAUDE.md not directly consumed |
| Cursor | SaaS/Electron | No | Uses `.cursorrules`; CLAUDE.md not natively consumed |

## Templates & scripts
See templates.md for full CLAUDE.md skeleton variants (minimal, standard, monorepo).

Inline helper to dump project commands into CLAUDE.md-ready format:

```bash
#!/usr/bin/env bash
# extract-commands.sh
# Outputs Commands section for CLAUDE.md

echo "## Commands"
echo ""

if [ -f package.json ]; then
  echo "### npm / Node"
  echo '```bash'
  jq -r '.scripts | to_entries[] | "\(.key)  # \(.value)"' package.json 2>/dev/null \
    | head -20
  echo '```'
fi

if [ -f Makefile ]; then
  echo ""
  echo "### Make"
  echo '```bash'
  grep -E "^[a-zA-Z_-]+:" Makefile \
    | sed 's/:.*//' \
    | head -20 \
    | while read t; do echo "make $t"; done
  echo '```'
fi

if [ -f pyproject.toml ]; then
  echo ""
  echo "### Python"
  echo '```bash'
  grep -A1 '^\[tool.poetry.scripts\]' pyproject.toml | tail -n +2 | head -10
  echo '```'
fi
```

## Best practices
- Write CLAUDE.md for Claude, not for humans: avoid narrative prose, use scannable tables and code blocks instead.
- Lead with Commands — it is the most frequently referenced section during AI-assisted development.
- Keep the Structure section to 2 levels deep; deeper nesting is noise for an agent that will glob and grep anyway.
- Add a "Gotchas" section listing things that have surprised developers (or agents) before: migration order requirements, required but undocumented env vars, test isolation quirks.
- Review CLAUDE.md on every major PR that changes directory layout, build commands, or lint configuration.
- For Python projects: explicitly name active ruff rule groups in CLAUDE.md — agents need to know T20 = no print() to avoid triggering pre-commit hooks.
- For monorepos: root CLAUDE.md delegates to per-module files; never copy module-specific instructions to root.

## AI-agent gotchas
- An agent that generates CLAUDE.md and then immediately commits it bypasses human validation of commands. The generated file should be reviewed before first commit.
- If CLAUDE.md references environment variables with example values (`SECRET_KEY=abc123`), agents may use those literal values in code. Use `SECRET_KEY=<required>` notation instead.
- CLAUDE.md with `@AGENTS.md` delegation (faion convention) requires Claude Code to support the `@` include syntax. Verify version compatibility before deploying this pattern to a new team.
- Agents working on a feature branch may have a branch-local CLAUDE.md that differs from main; ensure the file is kept in sync or explicitly scope which branch the instructions apply to.
- An outdated CLAUDE.md that references a removed directory causes agents to waste tool calls searching for files that no longer exist.

## References
- https://docs.anthropic.com/en/docs/claude-code/memory — Claude Code memory and CLAUDE.md documentation
- https://docs.anthropic.com/en/docs/claude-code/project-setup — Project setup guide
- https://docs.anthropic.com/en/docs/claude-code — Main Claude Code documentation
