---
name: make-skills
description: Creates, edits, updates, or modifies Claude Code skills. Use when user asks to create skill, edit skill, update skill, change skill, modify skill, fix skill, improve skill, add to skill. Triggers on "skill", "SKILL.md", "agent skill".
user-invocable: true
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(rm:*), Bash(ls:*), Glob
---

# Creating or Updating Skills

**Communication with user: User's language. Skill content: English.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create a new skill
- Edit/update/change/modify existing skill
- Fix or improve a skill
- Add functionality to a skill

**Trigger phrases:** "create skill", "edit skill", "change skill", "update skill", "modify skill", "fix skill", "skill", "SKILL.md"

---

## Token Economy Rules (CRITICAL)

Skills consume context window. Every token must earn its place.

**DO:**
- Use bullet lists instead of tables
- Use simple markdown without ASCII art borders
- Write in English (smaller tokens than Ukrainian)
- Keep SKILL.md under 300 lines (ideal), max 500
- Challenge each line: "Does Claude need this?"

**DON'T:**
- ASCII borders like `+----+----+` or `|    |    |`
- Verbose explanations Claude already knows
- Tables where lists work
- Emojis unless user requests

## Skills vs Commands

**Skill** - automatic discovery, complex workflows, multiple files
**Command** - manual `/invoke`, accepts arguments, single file

---

## Skill Structure

```
skill-name/
├── SKILL.md         # Required
├── reference.md     # Optional - details
└── scripts/         # Optional - utilities
```

---

## SKILL.md Frontmatter

```yaml
---
name: skill-name              # lowercase, hyphens, max 64 chars
description: Third-person description with trigger keywords. Max 1024 chars.
user-invocable: true          # Show in / menu (default: true)
disable-model-invocation: false  # Block programmatic Skill tool calls
context: fork                 # Isolated context (optional)
agent: general-purpose        # Agent type for forked context
allowed-tools: Read, Grep, Glob, Bash(cmd:*)  # Optional
model: claude-sonnet-4-20250514               # Optional
hooks:                        # Optional lifecycle hooks
  PreToolUse:
    command: "echo 'Before tool'"
  PostToolUse:
    command: "echo 'After tool'"
  Stop:
    command: "echo 'Skill finished'"
---
```

**Required:** name, description
**Optional:** user-invocable, disable-model-invocation, context, agent, allowed-tools, model, hooks

**New fields (Jan 2026):**
- `user-invocable: false` - hide from / menu, Claude can still invoke via Skill tool
- `disable-model-invocation: true` - completely block programmatic invocation
- `context: fork` - run in isolated context with own history
- `agent` - specify agent type: Explore, Plan, general-purpose
- `hooks` - lifecycle hooks: PreToolUse, PostToolUse, Stop

---

## Built-in Tools

**File tools (no permission):**
- Read - read file contents
- Glob - find files by pattern
- Grep - search with regex

**File tools (permission required):**
- Write - create/overwrite files
- Edit - targeted edits
- NotebookEdit - Jupyter cells

**Execution:**
- Bash - shell commands (permission)
- Task - sub-agent (no permission)
- Skill - another skill (permission)

**Web:**
- WebFetch - fetch URL (permission)
- WebSearch - search (permission)

**Other:**
- LSP - language server (permission)
- AskUserQuestion - multiple choice (no permission)
- TodoWrite - task lists (no permission)

---

## allowed-tools Syntax

Basic: `allowed-tools: Read, Grep, Glob`

Bash prefix matching:
- `Bash(git:*)` - all git commands
- `Bash(python -m pytest:*)` - pytest with args

WebFetch domain: `WebFetch(domain:github.com)`

Combined: `allowed-tools: Read, Bash(git:*), WebFetch(domain:github.com)`

**Note:** Pattern is PREFIX match, not regex. Without `:*` requires exact match.

---

## Description Rules

**Third person only:**
- Good: "Processes Excel files and generates reports"
- Bad: "I can help you process Excel files"

**Include trigger keywords:**
- Good: "Extracts text from PDFs, fills forms, merges documents. Use when working with PDF files."
- Bad: "Helps with documents"

---

## Naming Convention

Anthropic recommends gerund form (verb + -ing):
- Best: `processing-pdfs`, `analyzing-spreadsheets`
- Good: `pdf-processing`, `code-review`
- Bad: `CodeReview`, `my_skill`, `helper`, `utils`

---

## SKILL.md Body Template

```markdown
# Skill Title

**Communication with user: User's language. Skill content: English.**

## Purpose
One sentence.

## Workflow
1. Step one
2. Step two
3. Step three

## Degrees of Freedom
- High: decision X
- Low: must follow Y exactly

## Failed Attempts
- Approach A - why it fails
- Approach B - why it fails

## Sources
- Reference 1
- Reference 2
```

---

## Skill Locations

- Personal: `.claude/skills/skill-name/`
- Project: `.claude/skills/skill-name/`

Project overrides personal with same name.

---

## Creation Process

1. Ask requirements: purpose, triggers, tools, scope
2. **Ask: local or shared?**
   - Local = project-specific, not committed to `.claude/` repo
   - Shared = committed to `.claude/` repo, available to all projects using it
3. Create directory: `mkdir -p .claude/skills/skill-name`
4. Write SKILL.md with token-efficient structure
5. Add reference.md if needed (split large content)
6. **If local:** make skill private (see below)

---

## Local/Private Skills

To keep a skill local (not synced to `.claude/` remote repo):

1. **Check parent directory has git repo:**
   ```bash
   cd ..  # parent of .claude/
   git status || git init
   ```

2. **Add skill to parent's .gitignore:**
   ```bash
   echo ".claude/skills/skill-name/" >> .gitignore
   ```

3. **If skill already tracked in .claude repo, remove it:**
   ```bash
   cd .claude
   git rm -r --cached skills/skill-name/
   git commit -m "Remove skill-name from tracking (local skill)"
   git push
   ```

**Why parent .gitignore?**
- `.claude/` is often a separate repo (submodule or standalone)
- Parent project's `.gitignore` prevents `.claude/skills/skill-name/` from being committed to parent
- `.claude/.gitignore` uses whitelist (`!skills/**`), so skills are tracked by default

**Example structure:**
```
project/              # Parent repo
├── .gitignore        # Contains: .claude/skills/my-local-skill/
├── .claude/          # Separate repo (faion-network)
│   ├── .gitignore    # Whitelist approach
│   └── skills/
│       ├── shared-skill/    # Tracked in .claude repo
│       └── my-local-skill/  # NOT tracked (in parent .gitignore)
```

---

## Troubleshooting

- Skill not triggering → more specific description with keywords
- YAML error → use spaces not tabs, check `---` delimiters
- Skill not found → file must be exactly `SKILL.md` (case-sensitive)
- Tools not working → use `:*` suffix for Bash patterns

---

## Advanced Patterns

**Failed Attempts section:**
Document what doesn't work. From Anthropic: "Failure paths save more time than success paths."

**Degrees of Freedom:**
- High freedom: multiple valid approaches
- Medium: preferred pattern exists
- Low: fragile operations, exact steps required

**One level deep references:**
SKILL.md → reference.md (good)
SKILL.md → advanced.md → details.md (bad - may be partially read)

**MCP tools:** Use full names `ServerName:tool_name`

---

## Self-Updating

This skill can update itself. To update:
1. Edit `~/.claude/claudedm/skills/make-skills/SKILL.md`
2. Sync: `cp -r ~/.claude/claudedm/skills/make-skills ~/.claude/skills/`
3. Changes apply immediately (hot-reload in Jan 2026+)

Repository: `~/.claude/claudedm/` (faionfaion/claudedm on GitHub)

---

## Documentation

- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
