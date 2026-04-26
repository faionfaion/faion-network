---
name: faion-improver
description: "Session-based continuous improvement: investigate system, find gaps, brainstorm, apply fixes, log improvements, commit, create skills from experience. 5 methodologies."
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, TaskCreate, TaskUpdate, TaskList, AskUserQuestion, Skill
---

# Session Improver

Turns the current session's experience into persistent knowledge. **First priority: analyze what happened THIS session** — what was built, what broke, what patterns emerged. Then optionally investigate broader system state.

**Entry point:** `/faion-improver` (invoked directly)

---

## How It Works

```
Session Review → Investigate (optional) → Classify → Apply → Log → Commit → Skill
```

Each session produces:
1. **Patterns** — what worked well, extracted for reuse (→ `.aidocs/memory/patterns.md`)
2. **Mistakes** — what broke and why, with prevention steps (→ `.aidocs/memory/mistakes.md`)
3. **Improvements** — applied to system (configs, code, docs)
4. **Skills** — new or updated skills from domain knowledge gained

---

## Workflow Phases

### Phase 0: Session Review (ALWAYS DO FIRST)

Before any investigation, analyze the **current conversation context**:

1. **What was built/changed this session?** List features, fixes, configs touched
2. **What broke?** Bugs found, deploy failures, silent errors, wrong assumptions
3. **What patterns emerged?** Recurring approaches that worked (or didn't)
4. **What was surprising?** Non-obvious findings, undocumented behavior
5. **What should future sessions know?** Context that would save time next time

**Output:** Structured list of patterns (PAT-NNN) and mistakes (ERR-NNN)

Write immediately to:
- `.aidocs/memory/patterns.md` — append new PAT entries
- `.aidocs/memory/mistakes.md` — append new ERR entries

**This phase is the core value.** Phases 1-7 are optional extensions.

### Phase 1: Investigate (optional — when user asks for system audit)

Audit the current state of the target system. Use parallel agents for speed.

```
Agent 1: Read all configs (shell, SSH, nginx, systemd, Docker, cron)
Agent 2: Check security posture (firewall, fail2ban, SSL, exposed ports)
Agent 3: Check performance (kernel tuning, swap, resource limits)
Agent 4: Check developer experience (tools, aliases, tmux, git config)
```

**Output:** Detailed findings list with priority (CRITICAL/HIGH/MEDIUM/LOW)

### Phase 2: Classify & Prioritize

Group findings by priority:
- **Critical**: Security vulnerabilities, data loss risks
- **High**: Missing resource limits, performance gaps
- **Medium**: DX improvements, missing documentation
- **Low**: Nice-to-haves, cosmetic issues

Group findings by scope:
- **System** — server configs, kernel tuning, firewall, packages → apply directly (Phase 4)
- **Project** — code changes, API improvements, new features, refactoring → create SDD tasks using `faion/knowledge/solo/sdd/sdd-planning/` (Phase 4b)

This distinction is important: system improvements are applied in the current session, project improvements go through SDD workflow with proper specs, design, and implementation plans.

### Phase 3: Brainstorm

Run `Skill(faion-brainstorm)` with:
- Session context (what was done, what was learned)
- Investigation findings
- Questions about reusability, patterns, new skills

**Output:** Brainstorm document with insights, ideas, action items

### Phase 3.5: User Approval

**MANDATORY before any changes.** Use `AskUserQuestion` to present findings and get explicit approval.

For each improvement:
1. Describe the problem found
2. Explain the risk if left unfixed
3. Propose 2-3 implementation options with trade-offs
4. Ask which option to apply (or skip)

Example:
```
Found: RabbitMQ AMQP (5672) and Management UI (15672) exposed to internet.

Options:
A) Bind both ports to 127.0.0.1 — keeps services, blocks external access
B) Remove Management UI entirely, bind AMQP to localhost — smaller attack surface
C) Keep as-is but add fail2ban jail for RabbitMQ — detect brute force

Recommended: B

Which option? (A/B/C/skip)
```

For security changes — always explain:
- What's currently exposed/vulnerable
- What each option changes
- Whether services need restart (and downtime impact)

Group related changes together (e.g., all Docker port changes as one approval) but separate unrelated categories (security vs DX vs performance).

**Never apply changes without user approval, even if CRITICAL.**

### Phase 4: Apply Fixes

Apply only user-approved improvements using parallel agents:
- Agent for config fixes (systemd, Docker, nginx)
- Agent for documentation updates (CLAUDE.md, .aidocs)
- Agent for new files (.bash_aliases, sysctl configs)

**Rules:**
- Only apply changes explicitly approved in Phase 3.5
- Never restart production services without user approval
- Always backup before modifying system configs
- Read before edit — never blind-write

### Phase 4b: SDD Tasks for Project Improvements

For findings that require code changes, new features, or architectural work — don't apply directly. Instead, create SDD artifacts:

1. Classify as feature or improvement
2. Create `.aidocs/improvements/AI-NNN-*.md` or `.aidocs/backlog/feature-NNN-*/`
3. If user approves full planning → read `faion/knowledge/solo/sdd/sdd-planning/` for spec + design + implementation plan guidance
4. If user wants quick tracking → create task files in `.aidocs/todo/`

Examples of project-scope findings:
- "Health endpoint should return service dependency status" → feature task
- "Celery concurrency=20 is too high for 16 cores" → improvement with benchmarking needed
- "Missing Redis auth" → security task with migration plan
- "PostgreSQL not tuned for write-heavy workload" → performance task with spec

The key difference: system changes are config edits (immediate), project changes are code (need planning, testing, deploy).

### Phase 5: Log

Create/update improvement log at project-specific path:
- `{project}/operations/improvement-log.md` for project improvements
- `~/.claude/projects/{project}/memory/` for cross-session memory

Log format:
```markdown
## YYYY-MM-DD — Session Title

### Changes
- [CRITICAL] Fixed exposed RabbitMQ ports → bound to 127.0.0.1
- [HIGH] Added MemoryMax to systemd services
- [MEDIUM] Created .bash_aliases with 30+ shortcuts

### Patterns Learned
- Workspace/runtime separation for deploy safety
- Claude Code hooks for environment persistence

### Skills Created
- faion-server-craft (27 methodologies)
```

### Phase 6: Commit

If changes touch git repos:
1. `git diff` to review changes
2. Stage only relevant files
3. Commit with descriptive message
4. Push if user approves

### Phase 7: Skill Creation

If the session produced enough domain knowledge:
1. Create skill directory in `~/.claude/skills/faion-{name}/`
2. Write SKILL.md with frontmatter, decision tree, methodology list
3. Write CLAUDE.md with overview
4. Create methodology folders with 5-file structure
5. Register in faion routing
6. Commit to faion-network repo

---

## Decision Tree

| User Intent | Phase |
|-------------|-------|
| `/faion-improver` (no args) | Phase 0 (Session Review) — analyze current session |
| "What did we learn?" / "що ми зробили?" | Phase 0 (Session Review) |
| "Audit this server" / "find issues" | Phase 0 + 1 (Session Review + Investigate) |
| "What can be improved?" | Phase 0 + 1 + 2 (Session + Investigate + Classify) |
| "Brainstorm improvements" | Phase 0 + 3 (Session + Brainstorm) |
| "Fix the issues you found" | Phase 4 (Apply) |
| "Log what we did" | Phase 0 + 5 (Session Review + Log) |
| "Commit improvements" | Phase 6 (Commit) |
| "Create a skill from this" | Phase 7 (Skill Creation) |
| "Full improvement cycle" | All phases |

**Rule: Phase 0 (Session Review) runs FIRST in every invocation.** It costs nothing (just reads conversation context) and produces the highest-value output (patterns + mistakes for future sessions).

---

## Methodologies (5)

| Methodology | Focus |
|-------------|-------|
| `system-audit/` | How to investigate a system thoroughly |
| `gap-analysis/` | Classifying and prioritizing findings |
| `improvement-application/` | Safely applying fixes |
| `knowledge-capture/` | Logging, memory, .aidocs patterns |
| `skill-extraction/` | Creating skills from experience |

---

## Integration Points

- **faion-brainstorm**: Multi-agent brainstorming for improvement ideas
- **faion/knowledge/solo/infra/server-craft/**: Server-specific configurations and tuning
- **faion/knowledge/pro/infra/devops-engineer/**: Infrastructure and CI/CD improvements
- **faion/knowledge/solo/sdd/sdd/**: SDD workflow improvements
- **.aidocs/memory/**: Project-specific pattern/mistake/decision capture

---

## Anti-patterns

- Don't apply ANY fix without explicit user approval via AskUserQuestion
- Don't present a single option — always offer 2-3 alternatives with trade-offs
- Don't apply fixes without reading current state first
- Don't restart services without user confirmation
- Don't commit everything at once — commit logically grouped changes
- Don't create skills for one-off tasks — only for reusable knowledge
- Don't log ephemeral state — log patterns and decisions
- Don't assume CRITICAL = auto-apply. Even critical fixes need user sign-off
