---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
---

# Improver Workflow

## Summary

Session-first continuous improvement: extract patterns and mistakes from the current conversation, optionally extend to system audit, propose fixes with explicit approval, apply, log, commit. Phase 0 (session review) runs in every invocation; Phases 1-7 are optional extensions.

## Why

Without explicit capture, hard-won session learnings evaporate at compaction. Phase 0 turns conversation context into append-only `.aidocs/memory/{patterns,mistakes,decisions}.md` entries — costs nothing, compounds over time. The remaining phases (audit/brainstorm/apply/log/commit/skill) are opt-in extensions for full improvement cycles.

## When To Use

- End of productive session — capture before context is lost
- After a significant feature/fix
- "що ми зробили?" / "what did we learn?"
- "audit my server" / "find issues" — extends to Phase 1+
- Experience worth turning into a reusable skill — Phase 7

## When NOT To Use

- Mid-session, before something is actually done — nothing to extract yet
- Single-line fix with no broader pattern
- User just wants to commit changes — use direct git, not this workflow

## Phases

### Phase 0: Session Review (ALWAYS FIRST)

Read conversation context and extract:
1. What was built/changed?
2. What broke? (bugs, deploy failures, wrong assumptions)
3. What patterns emerged? (recurring approaches that worked)
4. What was surprising? (non-obvious findings)
5. What should future sessions know?

**Output:** Append PAT-NNN entries to `.aidocs/memory/patterns.md`, ERR-NNN entries to `.aidocs/memory/mistakes.md`. This phase is the core ROI.

### Phase 1: Investigate (optional — system audit)

Parallel agents: configs, security posture, performance, DX. Output: findings list with priorities (CRITICAL/HIGH/MEDIUM/LOW).

### Phase 2: Classify & Prioritize

Group by priority + scope: System (config edits, applied directly in Phase 4) vs Project (code changes, route through SDD via `knowledge/solo/sdd/sdd-planning/`).

### Phase 3: Brainstorm (optional)

Delegate to `../brainstorm/` workflow with session context + investigation findings. Skip if Phase 0 already produced clear actions.

### Phase 3.5: User Approval (MANDATORY before any change)

For each improvement: describe problem, explain risk, propose 2-3 options with trade-offs, ask which to apply. Group related changes; separate categories. **Never apply without approval, even CRITICAL.** Use `AskUserQuestion`.

### Phase 4: Apply Fixes

Apply only approved improvements. Parallel agents for orthogonal categories (configs / docs / new files). Rules: read before edit, never restart prod services without approval, backup before modifying system configs.

### Phase 4b: SDD Tasks for Project Improvements

Code/architecture findings → don't apply directly. Create `.aidocs/improvements/AI-NNN-*.md` or `.aidocs/backlog/feature-NNN-*/`. Route through SDD planning if user wants full spec.

### Phase 5: Log

`{project}/operations/improvement-log.md` (project) and `~/.claude/projects/{project}/memory/` (cross-session). Format: `## YYYY-MM-DD — Title` + `### Changes` + `### Patterns Learned` + `### Skills Created`.

### Phase 6: Commit

Stage relevant files only, descriptive message, push only on user approval.

### Phase 7: Skill Creation

If session produced reusable domain knowledge: create methodology folder under `../../knowledge/<tier>/<group>/<name>/` with 5-file structure (README, checklist, templates, examples, llm-prompts).

## Decision Tree

| User intent | Phases |
|-------------|--------|
| (no args) / "що ми зробили?" | 0 only |
| "audit X" / "find issues" | 0 + 1 |
| "what can be improved?" | 0 + 1 + 2 |
| "brainstorm improvements" | 0 + 3 |
| "fix the issues" | 4 |
| "log what we did" | 0 + 5 |
| "commit improvements" | 6 |
| "make a skill from this" | 7 |
| "full improvement cycle" | all |

## Anti-Patterns

- Apply ANY fix without `AskUserQuestion` approval
- Single option presented (always 2-3 alternatives)
- Apply without reading current state first
- Restart services without confirmation
- One giant commit (group logically)
- Skill from one-off task (only reusable knowledge)
- Auto-apply CRITICAL — even critical needs approval

## Related

- `../brainstorm/` — multi-agent ideation (Phase 3 delegation)
- `../../knowledge/solo/sdd/sdd-planning/` — Phase 4b SDD planning
- `../../knowledge/solo/infra/server-craft/` — server config / tuning
- `.aidocs/memory/` — append-only PAT/ERR/DEC files
