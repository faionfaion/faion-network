# Agent Integration — Creating or Updating Claude Code Skills

## When to use
- A Claude subagent needs to encapsulate a repeatable workflow that Claude Code should automatically discover and invoke
- A task is too large for a single prompt and needs multi-file knowledge broken across SKILL.md + reference.md
- You need to scope tool permissions for a workflow (e.g., only `Read, Grep, Glob` for read-only research agents)
- You want a project-specific skill that must be gitignored and kept out of faion-network
- A user explicitly says "create skill", "edit skill", or references SKILL.md

## When NOT to use
- The workflow is a one-time task — use a plain prompt instead
- You only need a slash command with arguments — create a command, not a skill
- The skill already exists in faion-network and only needs minor wording changes — edit the existing file
- The workflow is project-specific business logic that should not be shared across projects

## Where it fails / limitations
- Skills with vague `description` fields fail to auto-trigger; Claude can't select them from the menu
- `allowed-tools` with Bash patterns missing `:*` require exact string match, breaking shell calls
- Skills with deeply nested references (A → B → C) may only be partially loaded, losing context
- `context: fork` isolates the skill's history — the parent conversation state is not visible inside the fork
- `disable-model-invocation: true` is permanent for that skill; the Skill tool cannot call it programmatically

## Agentic workflow
A Claude subagent can scaffold a new skill end-to-end: read existing skills for style, ask the user for purpose/triggers/tool scope, write SKILL.md and an optional reference.md, and verify placement. For updates, the subagent reads the existing SKILL.md, identifies the change scope, and edits in-place. The subagent should use the Skill tool to self-invoke the skill afterward to confirm trigger behavior, though this requires the skill to not have `disable-model-invocation: true`.

### Recommended subagents
- `faion-sdd-executor-agent` — for skills that are part of a larger feature SDD task
- `password-scrubber-agent` — review skill files before committing to ensure no secrets leak into SKILL.md

### Prompt pattern
```
Create a Claude Code skill named `{name}` that triggers when the user asks about {topic}.
The skill should: {purpose}. Allowed tools: {tool-list}. Scope: {local|global}.
Output: SKILL.md at .claude/skills/{name}/SKILL.md
```

```
Update skill `{name}`: change the description to include trigger keyword "{keyword}".
Do not change any other sections. Read the existing file first.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` | Run Claude Code, invoke skills via `/` menu or Skill tool | `npm i -g @anthropic-ai/claude-code` |
| `git` | Track skill files in faion-network repo | system |
| `pre-commit` | Enforce CHANGELOG.md update on every commit | `pip install pre-commit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code (Anthropic) | SaaS | Yes | Primary runtime; reads `~/.claude/skills/` on start |
| GitHub (faion-network) | SaaS | Yes | Skills committed here are distributed to all projects via symlink |
| 1Password CLI | SaaS | Yes | Use `op` to inject secrets into SKILL.md `allowed-tools` env vars without hardcoding |

## Templates & scripts
See `templates.md` for SKILL.md skeleton with frontmatter, Workflow, Degrees of Freedom, Failed Attempts, and Agent Selection sections.

Inline helper — verify a skill's trigger coverage:
```bash
# Check description length and keyword density
python3 -c "
import sys, re
text = open('.claude/skills/$1/SKILL.md').read()
match = re.search(r'description: (.+)', text)
desc = match.group(1) if match else ''
print(f'Length: {len(desc)} chars (max 1024)')
print(f'Triggers: {desc}')
"
```

## Best practices
- Keep `description` under 1024 chars; front-load the most distinctive trigger keywords in the first 20 words
- Use `user-invocable: false` for internal/orchestration skills that users should never invoke directly from the `/` menu
- Split large knowledge into SKILL.md + reference.md; never go three levels deep (A→B→C breaks partial reads)
- For Bash patterns in `allowed-tools`, always append `:*` (e.g., `Bash(git:*)`, `Bash(python -m pytest:*)`)
- Document failed approaches in "Failed Attempts" — Anthropic's own guidance is that failure paths save more time than success paths
- Local/project skills must be gitignored at the parent `.gitignore`, not inside `.claude/`; otherwise the skill leaks into faion-network

## AI-agent gotchas
- Skills do not inherit the parent conversation's tool permissions; `allowed-tools` must be explicitly declared or the skill defaults to inheriting — test this before deploying
- When `context: fork` is set, the skill runs with no prior history; pass all required context through the skill prompt, not by relying on earlier messages
- The `Skill` tool requires user permission the first time per session; automated pipelines must pre-approve or the pipeline halts for human input
- If a skill calls another skill (nested invocation) without `context: fork`, the inner skill can read the outer conversation, which may cause unintended behavior or context pollution
- Model field in frontmatter is advisory — Claude Code may downgrade or override the model depending on the active plan; do not rely on `model: claude-opus-4` being honored in all environments

## References
- [Claude Code Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Slash Commands docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Subagents docs](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- faion-network: `skills/faion-claude-code/project-docs-convention/README.md`
