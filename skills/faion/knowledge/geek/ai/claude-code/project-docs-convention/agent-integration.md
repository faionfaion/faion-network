# Agent Integration — Project Documentation Convention

## When to use
- Setting up a new repo or directory that will be worked on by both Claude Code and standalone agents (Agent SDK, autoheal, scheduled workers)
- Auditing an existing repo to ensure all directories have discoverable context for multi-agent pipelines
- Onboarding a new project into the faion-network knowledge layer (CLAUDE.md + AGENTS.md pair required)
- Migrating a project from "all context in CLAUDE.md" to the two-file pattern for agent compatibility

## When NOT to use
- Trivial directories with < 3 files and no logic (e.g., empty `__init__.py` stubs) — skip creating the pair
- External vendored code — do not add CLAUDE.md/AGENTS.md to third-party directories
- Temporary scratch directories created during a build or test run — no documentation needed

## Where it fails / limitations
- If CLAUDE.md contains anything other than `@AGENTS.md`, Claude Code will load mixed content — the @-ref pattern is strict: one line only
- AGENTS.md with @-refs to other files is an anti-pattern — standalone agents follow @-refs; AGENTS.md must be self-contained
- INDEX.md tables work only if agents know to look for them — always mention `.agents/INDEX.md` path in AGENTS.md so agents know where to look on demand
- Convention enforcement is manual — there is no automated linter that blocks non-compliant commits (audit script exists but is not a hook)
- The `.product/` vs `.aidocs/` distinction (per-project vs workspace-level SDD) is easy to confuse — document the mapping explicitly per project

## Agentic workflow
A documentation audit agent (Read, Glob, Grep) scans all directories with source files, checks for CLAUDE.md/AGENTS.md pairs, reports missing pairs and content violations. A documentation writer agent (Write, Edit) creates missing files from templates. The audit → write cycle is sequential: no file is created without first checking if it already exists. Human review is recommended before committing the initial pair to a repo.

### Recommended subagents
- Documentation audit agent (Read, Glob) — checks all dirs for compliance, reports missing files
- General-purpose implementer (Write, Edit) — creates CLAUDE.md/AGENTS.md pairs from templates
- `faion-spec-reviewer-agent` — validates AGENTS.md quality (20-80 lines, file table, key types present)

### Prompt pattern
Creating the pair for a new directory:
```
Create CLAUDE.md and AGENTS.md for directory: {path}
CLAUDE.md: exactly one line: @AGENTS.md
AGENTS.md (20-80 lines) must include:
- What this directory IS (one sentence)
- Build/test/deploy commands if applicable
- File table (| File | Description |)
- Key types/modules
- Path to .agents/INDEX.md if .agents/ exists
Do NOT include @-refs in AGENTS.md.
```

Audit prompt:
```
Glob all directories under {root} that contain source files.
For each directory, check if CLAUDE.md and AGENTS.md exist.
For CLAUDE.md: verify it contains only "@AGENTS.md".
Report: missing pairs, CLAUDE.md with extra content, AGENTS.md over 80 lines.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bash audit-claude-md.sh` | Check all CLAUDE.md files are @-ref only | `~/workspace/scripts/audit-claude-md.sh` |
| `grep -r "@AGENTS.md" .` | Quick check for @-ref pattern | System grep |
| `find . -name "AGENTS.md"` | List all AGENTS.md files | System find |
| `wc -l` | Check AGENTS.md line count (target: 20-80) | System |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | OSS/SaaS | Native | Auto-loads CLAUDE.md via @-ref chain |
| Anthropic Agent SDK | OSS | Yes | Reads AGENTS.md directly; no @-ref support |
| GitHub Actions | SaaS | Indirect | CI job can run audit script and fail on violations |
| Pre-commit | OSS | Yes | Hook can enforce CLAUDE.md = @AGENTS.md |

## Templates & scripts
Audit script (≤30 lines):
```bash
#!/usr/bin/env bash
# Check every directory with source files has CLAUDE.md + AGENTS.md
set -euo pipefail
ROOT=${1:-.}
FAIL=0

find "$ROOT" -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" \) \
  | xargs -I {} dirname {} | sort -u \
  | while read -r dir; do
    [[ "$dir" == */.git/* ]] && continue
    [[ "$dir" == */node_modules/* ]] && continue
    [[ "$dir" == */__pycache__/* ]] && continue

    if [[ ! -f "$dir/CLAUDE.md" ]]; then
      echo "MISSING CLAUDE.md: $dir"; FAIL=1
    elif ! grep -q "^@AGENTS.md$" "$dir/CLAUDE.md"; then
      echo "BAD CLAUDE.md (not @-ref only): $dir"; FAIL=1
    fi

    if [[ ! -f "$dir/AGENTS.md" ]]; then
      echo "MISSING AGENTS.md: $dir"; FAIL=1
    fi
  done

[[ $FAIL -eq 0 ]] && echo "All directories compliant." || exit 1
```

## Best practices
- Create the CLAUDE.md/AGENTS.md pair at the same time as the first source file in a new directory — retrofitting is harder
- AGENTS.md file table format: `| File | Description |` with one row per file/subdir — skip auto-generated files
- `.agents/INDEX.md` table format: `| File/Dir | Description |` — one line per entry, no prose
- Don't put implementation details in AGENTS.md (architecture deep dives, full API reference) — those belong in `.agents/`
- When a directory evolves, update AGENTS.md first — it's the single source of truth for agents entering the directory cold
- The convention doesn't replace code comments — it's for cross-agent discoverability, not inline documentation

## AI-agent gotchas
- An agent that reads CLAUDE.md and sees only `@AGENTS.md` will follow the @-ref — but only if the agent's runtime supports @-ref chaining; standalone Agent SDK does not auto-follow @-refs
- Standalone agents (not Claude Code) must be explicitly instructed to read AGENTS.md directly — they do not auto-load any files
- AGENTS.md must be self-contained: if an agent reads AGENTS.md and finds @-refs or cross-file references without context, it will fail to understand the directory
- The `.product/` directory (per-project SDD) vs `.aidocs/` (workspace-level) confusion can cause agents to look in the wrong place — document the mapping in the root AGENTS.md
- Agents creating new directories will skip creating the CLAUDE.md/AGENTS.md pair unless explicitly instructed — always include the pair creation in agent task prompts
- INDEX.md files only help if agents know to ask for them — add "see .agents/INDEX.md for details" to AGENTS.md so agents know on-demand reference exists

## References
- Convention source: `skills/faion-claude-code/project-docs-convention/README.md`
- Audit script: `~/workspace/scripts/audit-claude-md.sh`
- Agent prompt for audit: `~/workspace/scripts/agent-docs-audit.md`
- https://docs.anthropic.com/en/docs/claude-code
