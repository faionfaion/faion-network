# improver

**Session-first** continuous improvement. Analyzes the current session's experience BEFORE doing anything else: what was built, what broke, what patterns emerged. Then optionally extends to system audit.

## When to Use

- **End of productive session** — capture patterns and mistakes before context is lost
- After completing a significant feature or fix
- When the user asks "що ми зробили?", "what did we learn?"
- When the user asks to audit/improve their system
- When experience should become a reusable skill

## Workflow

```
Phase 0: Session Review (ALWAYS FIRST)
  → What was built? What broke? What patterns? What's surprising?
  → Write to .aidocs/memory/patterns.md (PAT-NNN)
  → Write to .aidocs/memory/mistakes.md (ERR-NNN)

Phase 1-7: (optional, when requested)
  Investigate → Classify → Brainstorm → Apply → Log → Commit → Skill
```

**Phase 0 is the core value.** It runs in every invocation, costs nothing (reads conversation context), and produces the highest-ROI output: patterns + mistakes for future sessions.

## Methodologies (5)

- **session-review**: Extract patterns/mistakes from current session context
- **system-audit**: Parallel investigation of configs, security, performance, DX
- **gap-analysis**: Classify findings by priority (CRITICAL → LOW)
- **knowledge-capture**: Logging to .aidocs/memory/, improvement-log.md
- **skill-extraction**: Creating new faion- skills from domain experience

## Memory Files

| File | Content | Format |
|------|---------|--------|
| `.aidocs/memory/patterns.md` | PAT-NNN: what worked, when, evidence | Append-only |
| `.aidocs/memory/mistakes.md` | ERR-NNN: what broke, fix, prevention | Append-only |
| `.aidocs/memory/decisions.md` | Key architectural decisions | Append-only |
| `.aidocs/memory/session.md` | Current session state/notes | Overwrite |

## Related Skills

- `brainstorm` (multi-agent brainstorming)
- `/faion` (knowledge/solo/sdd/sdd/) (quality gates, reflexion learning)
- `faion/knowledge/solo/infra/server-craft/` (server config/tuning)
