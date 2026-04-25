# Agent Integration — CLAUDE.md / AGENTS.md Documentation

## When to use
- Creating a new directory in a repo: drop in a CLAUDE.md (entry point) + AGENTS.md (full context) before any other file.
- Onboarding an agent to an unfamiliar module — agent first generates AGENTS.md by reading the directory, then commits it.
- After a significant refactor: agents must regenerate AGENTS.md so future context loads stay accurate.
- Multi-agent workspaces (Claude Code + Cursor + Cline + Aider) where each tool reads a different filename — symlink or `@AGENTS.md` chain ensures one source of truth.
- Repos with many sub-packages where loading the whole tree blows context.

## When NOT to use
- Tiny one-file scripts; the README is sufficient.
- Generated / vendored code (`node_modules/`, `dist/`) — never document these.
- Highly volatile prototypes where the structure changes daily; document after the dust settles.
- Directories that are pure data (assets, fixtures) without logic — a one-line README is enough.

## Where it fails / limitations
- AGENTS.md drift: agents update code but forget the doc. Without a hook, drift compounds.
- Multi-tool conflict: Cursor reads `.cursorrules`, Cline reads `.clinerules`, Claude Code reads CLAUDE.md, Codex CLI reads AGENTS.md. The convention here uses `CLAUDE.md = @AGENTS.md` to bridge two; the others need their own bridge files.
- Token waste from over-documenting — 500-line AGENTS.md negates the load-on-demand premise.
- LLMs hallucinate "common operations" sections (commands that don't exist in the repo).
- Subdirectory CLAUDE.md/AGENTS.md pairs are easy to forget for new dirs; needs a hook or scheduled audit.

## Agentic workflow
A scaffold subagent runs whenever a new directory with code is created: it reads up to ~20 files, summarizes purpose, key types, entry points, common commands, and writes the CLAUDE.md (one-line `@AGENTS.md` import) + AGENTS.md (20–80 lines). A drift-detection subagent runs on a schedule (e.g., weekly) and re-generates AGENTS.md from the current code, then diffs against existing — significant deltas open a maintenance PR. A loader subagent at session start reads only AGENTS.md files along the current working directory chain, never the whole tree.

### Recommended subagents
- `faion-improver` — session-based audit/improve loop already covers doc drift detection.
- `nero-context` — context loader that respects this convention.
- A custom `docs-scaffold` subagent — input: directory path; output: pair of CLAUDE.md/AGENTS.md following the project template.
- A `docs-drift-detector` subagent — pre-commit hook in CI that flags directories whose AGENTS.md hasn't been touched while their source files have.

### Prompt pattern
```
Read all *.py / *.ts / *.go in <dir> (max 20 files). Produce AGENTS.md following template:
- Purpose (1 sentence)
- File table (name → purpose)
- Key types/exports
- Common commands found in package.json/Makefile
- Gotchas inferred from comments or known patterns
Length: 20–80 lines. No ASCII art. No time estimates. English only.
Then write CLAUDE.md with single line: @AGENTS.md
```

```
Audit AGENTS.md vs current source. List:
- Files in source but missing from AGENTS.md table.
- Entries in AGENTS.md pointing to deleted files.
- Commands in AGENTS.md not present in package.json/Makefile.
Block PR if drift > 30%.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pre-commit` | Hook that blocks commits without AGENTS.md update when src changes | https://pre-commit.com |
| `git ls-tree -r HEAD --name-only` | List tracked files for doc generation | git docs |
| `tokei` / `cloc` | Quick LoC stats per directory to size the doc effort | https://github.com/XAMPPRocky/tokei |
| `mkdocs-material` | Render AGENTS.md/READMEs into a browsable site | https://squidfunk.github.io/mkdocs-material/ |
| `mdformat` | Markdown formatter (CI gate) | https://github.com/executablebooks/mdformat |
| `markdownlint-cli2` | Lint headings / link rot | https://github.com/DavidAnson/markdownlint-cli2 |
| `lychee` | Broken-link checker | https://github.com/lycheeverse/lychee |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | yes | Run drift detection + lychee on PR. |
| Read the Docs / Mintlify | SaaS | yes | Some teams publish AGENTS.md alongside human docs; works if you avoid agent-only jargon. |
| Vale | OSS | yes | Style-lint AGENTS.md for tone consistency. |
| GitBook / Notion | SaaS | partial | Mirroring possible but adds drift risk. |
| Continue.dev / Cursor | SaaS | yes | Both honour AGENTS.md when present (or symlink). |

## Templates & scripts
See `templates.md` (this methodology) for the universal template plus backend / frontend / infra / library variants. Inline drift-detector script:

```bash
#!/usr/bin/env bash
# scripts/audit-agents-md.sh
# Exit 1 if any directory has src files newer than its AGENTS.md by > 14 days.
set -e
THRESH=$((14*24*60*60))
NOW=$(date +%s)
fail=0
while IFS= read -r dir; do
  agents="$dir/AGENTS.md"
  [ -f "$agents" ] || continue
  agents_ts=$(stat -c %Y "$agents")
  newest_src=$(find "$dir" -maxdepth 1 -type f \
      \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.go' \) \
      -printf '%T@\n' | sort -n | tail -1 | cut -d. -f1)
  [ -z "$newest_src" ] && continue
  if [ $((newest_src - agents_ts)) -gt $THRESH ]; then
      echo "DRIFT: $agents (src newer by >14d)"
      fail=1
  fi
done < <(find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*')
exit $fail
```

## Best practices
- CLAUDE.md is a one-liner: `@AGENTS.md`. Nothing else. If you find yourself adding content to CLAUDE.md, it belongs in AGENTS.md.
- AGENTS.md target length 20–80 lines; over 80 → split into `.agents/` reference docs and link from AGENTS.md.
- Always include a "Gotchas" section — that's the highest-value content for an LLM (corrects training-data assumptions).
- Use absolute paths from repo root in tables, not paths relative to the doc — agents may load AGENTS.md without knowing where it sits.
- Reference commands exactly as they exist in `package.json`/`Makefile`. Drift here is the most common silent breakage.
- Keep one source of truth: AGENTS.md. Bridge other tools via symlink or one-line includes (`.cursorrules` → "See AGENTS.md").
- For each significant subdir, run the scaffold; per-module coverage scales because each agent loads only the relevant chain.

## AI-agent gotchas
- LLMs invent commands that "look like" what a project of this kind would have (`npm test`, `pytest`) regardless of whether they exist. Always grep the repo before writing the Common Commands section.
- Agents over-link: every paragraph becomes a sea of `[link]` to files that may not exist. Validate links in CI with lychee.
- The `@AGENTS.md` import directive is a Claude Code convention; other tools may treat it as literal text. Document for the broader team.
- Agents skip the "Gotchas" section because there's no obvious source. Prompt explicitly: "from comments containing TODO/FIXME/XXX/HACK and from recent fix commit messages, extract gotchas."
- Update cycles: when you add a hook that auto-regenerates AGENTS.md, agents start writing increasingly verbose docs because they're rewarded by tooling. Cap at 80 lines hard.
- Human-in-loop checkpoint: a human should approve the first AGENTS.md for any project root; subdirs can be agent-owned with diff review.
- Don't put secrets, environment variables, or API keys in AGENTS.md — even references to env files leak via grep.

## References
- https://agents.md — emerging convention spec
- https://docs.anthropic.com/en/docs/claude-code/memory — Claude Code memory model
- https://docs.cursor.com/context/rules-for-ai — Cursor's `.cursorrules`
- https://github.com/openai/codex — OpenAI Codex CLI AGENTS.md handling
- https://github.com/cline/cline — Cline `.clinerules`
- https://www.mintlify.com — docs platform compatible with markdown-first repos
