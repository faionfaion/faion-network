---
name: faion-improver
description: "Session-based continuous improvement: investigate system, find gaps, brainstorm, apply fixes, log improvements, commit, create skills from experience. 5 methodologies."
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, TaskCreate, TaskUpdate, TaskList, AskUserQuestion, Skill
---

# Session Improver

A structured workflow for turning hands-on experience into persistent improvements. When you solve a problem, configure a system, or discover a pattern, this skill captures that knowledge and feeds it back into the codebase, documentation, skills, and memory.

**Entry point:** `/faion-net` (routes here for improvement/audit/retrospective tasks)

---

## How It Works

```
Experience → Investigate → Find gaps → Brainstorm → Apply → Log → Commit → Skill
```

Each session produces:
1. **Improvements** applied to the system (configs, code, docs)
2. **Knowledge** captured in skills, memory, or .aidocs
3. **Patterns** extracted for future reuse

---

## Workflow Phases

### Phase 1: Investigate

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
- **Project** — code changes, API improvements, new features, refactoring → create SDD tasks via `Skill(faion-sdd-planning)` (Phase 4b)

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
3. If user approves full planning → `Skill(faion-sdd-planning)` for spec + design + implementation plan
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
5. Register in faion-net routing
6. Commit to faion-network repo

---

## Decision Tree

| User Intent | Phase |
|-------------|-------|
| "Audit this server" / "find issues" | Phase 1 (Investigate) |
| "What can be improved?" | Phase 1 + 2 (Investigate + Classify) |
| "Brainstorm improvements" | Phase 3 (Brainstorm) |
| "Fix the issues you found" | Phase 4 (Apply) |
| "Log what we did" | Phase 5 (Log) |
| "Commit improvements" | Phase 6 (Commit) |
| "Create a skill from this" | Phase 7 (Skill Creation) |
| "Full improvement cycle" | All phases |

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
- **faion-server-craft**: Server-specific configurations and tuning
- **faion-devops-engineer**: Infrastructure and CI/CD improvements
- **faion-sdd**: SDD workflow improvements
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
