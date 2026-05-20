---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.1.0
applies_to: any
content_id: 23442bb5cf3079c6
success_criteria:
  - Phase 0 runs on every invocation and appends PAT/ERR/DEC entries to `.aidocs/memory/`.
  - Any phase that writes (Phase 4 apply, Phase 6 commit) blocks until the Phase 3.5 user-approval gate passes.
  - CRITICAL findings still pass through Phase 3.5 — severity never overrides consent.
  - Phase 7 only fires when the captured experience is reusable as a skill.
---

# Improver Workflow

## Summary

Session-first continuous improvement. Phase 0 (session review) runs on every invocation and appends `PAT-NNN` / `ERR-NNN` / `DEC-NNN` entries to `.aidocs/memory/{patterns,mistakes,decisions}.md`. Phases 1-7 are optional extensions for full audit-brainstorm-apply-log-commit-skill cycles. The orchestrator decides phase, parallel subagents do the work, and the user gates ALL writes through a mandatory Phase 3.5 approval — even CRITICAL findings cannot bypass the gate.

## Why

Without explicit capture, hard-won session learnings evaporate at compaction. Phase 0 turns conversation context into append-only memory entries — costs nothing, compounds over time. The remaining phases stay opt-in so the workflow does not over-run the user's intent: a "log what we did" ask must not silently extend into "audit, fix, commit, push." The Phase 3.5 gate exists because CRITICAL describes impact, not consent; auto-applying CRITICAL findings has caused unintended downtime in past runs.

## When To Use

- End of a productive session — capture before context is lost.
- After a significant feature, fix, or surprising finding.
- "що ми зробили?" / "what did we learn?" / "audit my server" / "find issues".
- Experience worth turning into a reusable skill — Phase 7.

## When NOT To Use

- Mid-session, before anything is actually done — nothing to extract yet.
- Single-line fix with no broader pattern.
- User just wants to commit changes — use direct git, not this workflow.
- Any flow where the user has not authorized writes — this workflow's Phase 4 mutates files and Phase 6 commits.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle, role split, persistent output, language convention. |
| `content/02-phases.xml` | All 8 phases (0 Session Review, 1 Investigate, 2 Classify, 3 Brainstorm, 3.5 User Approval, 4 Apply, 4b SDD Tasks, 5 Log, 6 Commit, 7 Skill Creation). |
| `content/03-decision-tree.xml` | User intent to phase mapping (no-args, audit, brainstorm, fix, log, commit, skill, full cycle). |
| `content/04-memory-files.xml` | The 4 memory files — purpose, format, append-vs-overwrite, identifier rules. |
| `content/05-anti-patterns.xml` | Apply without approval, single option, edit without read, restart without confirm, giant commit, skill from one-off task. |
| `decisions.xml` | Why Phase 0 always first, why mandatory user approval, why System/Project split, why append-only memory, why Phase 7 reusable-knowledge bar. |

## Related

- `../brainstorm/` — multi-agent ideation (Phase 3 delegation target).
- `../../knowledge/solo/sdd/sdd-planning/` — Phase 4b SDD planning route.
- `../../knowledge/solo/infra/server-craft/` — server config and tuning reference.
- `.aidocs/conventions/workflows/workflow-spec.md` — workflow authoring spec.
- `.aidocs/memory/` — append-only PAT / ERR / DEC files written by Phase 0.
