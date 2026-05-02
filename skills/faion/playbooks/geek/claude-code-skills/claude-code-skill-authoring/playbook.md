---
name: claude-code-skill-authoring
description: Author a production-ready Claude Code skill from folder scaffold to validated SKILL.md — frontmatter keys, trigger keyword placement, multi-file split, allowed-tools scoping, and script colocation.
tier: geek
group: claude-code-skills
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a fully working Claude Code skill: a correctly shaped `SKILL.md` with all required frontmatter, trigger keywords placed for reliable auto-invocation, tool permissions scoped to minimum necessary, and — if the skill is complex — a `reference.md` for on-demand detail and a `scripts/` folder for colocated helpers. The skill will auto-appear in the `/` menu (or stay hidden for orchestration use), and will invoke correctly via the `Skill` tool from agent pipelines.

## Prerequisites

- Claude Code installed and running (version ≥1.0; `claude --version` shows a semver).
- `faion-network` repo cloned and symlinked at `~/.claude` (`ls ~/.claude/skills/` returns skill dirs).
- Decision made: **global** (committed to `faion-network`, available everywhere) or **project-specific** (gitignored, scoped to one project).
- One sentence describing exactly what the skill does and who calls it (human or agent pipeline).
- For global skills: write access to `faion-network` and a clean working branch.

## Steps

### 1. Decide skill type and location

Identify whether the skill is global or project-specific:

| Type | Location | Committed? |
|------|----------|------------|
| Global (shared) | `~/.claude/skills/faion-<name>/` | Yes, to `faion-network` |
| Project-specific | `<project-root>/.claude/skills/<project>-<name>/` | No, gitignored |

For a global skill that wraps a deploy script, the path is:

```
~/.claude/skills/faion-my-deploy/
├── SKILL.md
└── scripts/
    └── deploy.sh
```

For a project-specific skill named `mediamanager-db-migrate`:

```
~/workspace/projects/mediamanager-faion-net/.claude/skills/mediamanager-db-migrate/
└── SKILL.md
```

Add to `~/.gitignore`:

```
.claude/skills/mediamanager-*/
```

### 2. Scaffold the directory

```bash
# Global skill (replace my-deploy with your skill name)
SKILL_DIR="$HOME/.claude/skills/faion-my-deploy"
mkdir -p "$SKILL_DIR/scripts"
touch "$SKILL_DIR/SKILL.md"

# Project-specific skill
SKILL_DIR="$HOME/workspace/projects/mediamanager-faion-net/.claude/skills/mediamanager-db-migrate"
mkdir -p "$SKILL_DIR"
touch "$SKILL_DIR/SKILL.md"
```

### 3. Write the SKILL.md frontmatter

Open `SKILL.md` and write the YAML block. Required fields: `name` and `description`. All others are optional but recommended for production skills:

```yaml
---
name: faion-my-deploy                   # lowercase, hyphens, max 64 chars
description: Deploys the active project to the target environment by running deploy.sh. Use when the user asks to deploy, ship, push to production, or release.
user-invocable: true                    # true = appears in / menu
allowed-tools: Bash(bash:*), Read      # scope to minimum needed
---
```

Frontmatter rules:

- `name` must equal the folder name exactly.
- `description` must be third-person. Never "I can deploy…" — write "Deploys…".
- Front-load trigger keywords in the first 20 words. Claude Code's skill-selection algorithm scans the beginning; "Use when the user asks to deploy, ship, push to production, or release" after the functional description catches all common phrasings.
- `user-invocable: false` hides the skill from the `/` menu but allows programmatic invocation via the `Skill` tool. Use this for orchestration sub-skills that users should never call directly.
- `context: fork` runs the skill in an isolated context with no prior conversation history. Required when the skill must not be influenced by what was said before. Pass all needed context explicitly through the skill prompt.
- `allowed-tools` follows prefix matching: `Bash(git:*)` matches any git command; `Bash(bash:*)` matches `bash <path>`. Without `:*`, the pattern requires an exact match.

### 4. Write the SKILL.md body

Below the frontmatter, write the skill body. Minimum required sections:

```markdown
# Faion My Deploy

**Communication with user: User's language. Skill content: English.**

## Purpose

Runs `deploy.sh` in the current project root, then reports the deployed URL and git SHA.

## Workflow

1. Read `deploy.sh` to confirm it exists and is executable.
2. Run `bash scripts/deploy.sh` from the project root.
3. Report the result: deployed URL, exit code, and git SHA of the deployed commit.

## Degrees of Freedom

- Low: always run `deploy.sh` exactly as-is; do not modify it or substitute another script.
- High: decide whether to run `git status` first to warn about uncommitted changes.

## Failed Attempts

- Running `./deploy.sh` directly — fails when cwd is not the project root; use `bash scripts/deploy.sh` with an absolute path instead.
- Calling `npm run deploy` — project uses a custom shell script, not an npm lifecycle hook.

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Routine deploy with known state | claude-haiku-4-5-20251001 | Mechanical execution; no reasoning needed |
| Deploy with pre-flight checks and rollback decision | claude-sonnet-4-6 | Requires judgment about risk signals |
```

Key body rules:

- "Degrees of Freedom" distinguishes where the model has latitude (High) vs. where it must follow instructions exactly (Low). This prevents both over-rigidity and unsafe improvisation.
- "Failed Attempts" is the most valuable section for multi-agent pipelines: it eliminates wasted retries on known dead ends.
- "Agent Selection" maps subtasks to the right Claude model: use `claude-haiku-4-5-20251001` for mechanical tasks, `claude-sonnet-4-6` for judgment calls, `claude-opus-4-7` for complex architectural decisions.

### 5. Colocate helper scripts in scripts/

Place any executable helpers inside `<skill>/scripts/`. Never wrap them in XML or markdown fences — they are called directly via the `Bash` tool:

```bash
# scripts/deploy.sh  (inside the skill directory)
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

echo "Deploying from $(git rev-parse --short HEAD)..."
bash deploy.sh
echo "Done. Deployed commit: $(git rev-parse --short HEAD)"
```

Make the script executable:

```bash
chmod +x ~/.claude/skills/faion-my-deploy/scripts/deploy.sh
```

Reference the script from SKILL.md using its absolute path pattern:

```markdown
Run `bash ~/.claude/skills/faion-my-deploy/scripts/deploy.sh` from the project root.
```

### 6. Split large skills into SKILL.md + reference.md

If `SKILL.md` exceeds 300 lines, extract the deep-reference content into `reference.md`. Keep SKILL.md as the auto-loaded summary; `reference.md` is loaded on demand:

```
faion-my-deploy/
├── SKILL.md        # ≤300 lines: frontmatter + purpose + workflow + key rules
├── reference.md    # extended: API contracts, error codes, advanced examples
└── scripts/
    └── deploy.sh
```

In SKILL.md, link to reference.md explicitly so the model knows to load it when needed:

```markdown
## Extended Reference

Load `reference.md` for: full deploy.sh flag reference, rollback procedure, environment variable list.
```

Never go three levels deep (SKILL.md → reference.md → another file). Partial reads at the third level cause context loss.

### 7. Scope allowed-tools to minimum necessary

Match `allowed-tools` to what the skill actually needs:

| Skill purpose | Suggested allowed-tools |
|---------------|------------------------|
| Read-only research / audit | `Read, Grep, Glob` |
| Code generation + git commit | `Read, Write, Edit, Bash(git:*)` |
| Deploy via shell script | `Bash(bash:*), Read` |
| API calls to GitHub | `WebFetch(domain:api.github.com), Bash(curl:*)` |
| Full infrastructure management | `Bash(*), Read, Write, Edit, WebFetch` |

Always append `:*` to `Bash(...)` patterns: `Bash(git:*)` not `Bash(git)`. Without `:*`, the pattern requires an exact match (no arguments), which breaks for commands like `git commit -m "..."`.

### 8. Test auto-invocation

Open Claude Code and type a phrase that matches your trigger keywords. Verify:

1. The `/` menu shows the skill name when you type `/faion-my-deploy`.
2. Typing "deploy this project" without the slash causes Claude to auto-select and invoke the skill via the `Skill` tool.
3. The skill runs its workflow as described in the `## Workflow` section.

If the skill is not triggering, rewrite the `description` field: move the most specific trigger keywords to the first 10 words and add alternative phrasings in the "Use when" clause.

### 9. Commit global skills to faion-network

For global skills only:

```bash
cd ~/workspace/projects/faion-net/faion-network
git add skills/faion-my-deploy/
# Update CHANGELOG.md under [Unreleased]:
# - feat: add faion-my-deploy skill for project deployment
git add CHANGELOG.md
git commit -m "feat: add faion-my-deploy skill"
```

Project-specific skills stay gitignored and are never committed.

## Verify

Run all three checks after authoring:

```bash
# 1. Confirm SKILL.md parses as valid YAML frontmatter
python3 -c "
import re, sys, yaml
text = open('$HOME/.claude/skills/faion-my-deploy/SKILL.md').read()
m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
if not m: sys.exit('no frontmatter')
d = yaml.safe_load(m.group(1))
required = ['name','description']
missing = [k for k in required if k not in d]
if missing: sys.exit(f'missing keys: {missing}')
print('frontmatter OK:', list(d.keys()))
"

# 2. Confirm skill appears in Claude Code skill list
ls ~/.claude/skills/ | grep faion-my-deploy

# 3. Invoke programmatically (in a Claude Code session, run):
# /faion-my-deploy
# Expected: Claude loads SKILL.md, acknowledges the skill, executes workflow Step 1
```

For faion-network global playbooks, additionally run:

```bash
cd ~/workspace/projects/faion-net/faion-network
python3 scripts/validate-tier-playbook.py skills/faion/playbooks/geek/claude-code-skills/claude-code-skill-authoring/playbook.md
# Expected: exit code 0, no validation errors
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill not shown in `/` menu | `user-invocable: false` or Claude Code not reloaded | Set `user-invocable: true`; restart Claude Code session to reload skill index |
| `YAML parse error` on launch | Tabs in frontmatter or missing `---` delimiters | Replace all tabs with spaces; confirm opening and closing `---` lines are exact |
| `Bash(git:*)` returns permission error | Missing `:*` suffix | Change `Bash(git)` to `Bash(git:*)` in `allowed-tools`; `:*` is required for any command with arguments |
| Script not found when skill runs | Skill references `./scripts/deploy.sh` with relative path | Use absolute path `~/.claude/skills/faion-my-deploy/scripts/deploy.sh`; relative paths break when cwd changes |
| Skill invokes but ignores `context: fork` | `context` key placed outside frontmatter | Confirm `context: fork` is inside the `---` block, not in the body |
| Auto-invocation chooses wrong skill | Trigger keywords too generic (e.g., "runs commands") | Rewrite description to include unique domain terms; test with `claude --debug` to see skill-selection scoring |
| `reference.md` content ignored | Model didn't load it | Add explicit instruction in SKILL.md body: `"Load reference.md for <topic>."`; the model loads files only when prompted |
| Project-specific skill committed to faion-network | Gitignore pattern too narrow | Use `~/.gitignore` (global) not `.claude/.gitignore`; pattern: `.claude/skills/<project>-*/` |

## Next

- `claude-code-agent-design` — design multi-skill agent pipelines with `context: fork` and inter-skill data passing.
- `claude-code-hooks` — add `PreToolUse` and `PostToolUse` lifecycle hooks to validate inputs and audit outputs around skill execution.

## References

- [knowledge/geek/ai/claude-code/skills](../../../../../knowledge/geek/ai/claude-code/skills) — SKILL.md frontmatter rules, `allowed-tools` prefix-matching syntax, `user-invocable`/`context: fork`/`disable-model-invocation` semantics, and the global vs. project-specific naming convention that backs Steps 1–3 and 7.
