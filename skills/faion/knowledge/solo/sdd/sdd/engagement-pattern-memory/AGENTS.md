---
slug: engagement-pattern-memory
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A per-client / per-engagement memory layer that captures repo conventions, reviewer preferences, deploy quirks, and recurring patterns so freelancers juggling multiple clients don't re-learn each one every sprint.
content_id: "b13e1f9b319b7901"
tags: [sdd, memory, freelance, client-engagement, pattern-memory, repo-conventions]
---

# Engagement Pattern Memory

## Summary

**One-sentence:** A per-engagement memory file (one per active client / repo) that records repo conventions, reviewer preferences, deploy quirks, recurring traps, and resolved questions, replacing the daily re-learn that drains freelancer / contractor time.

**One-paragraph:** Existing `pattern-memory` and `mistake-memory` methodologies are scoped to a single product / brain. Freelancers and contractors with 2-3 concurrent clients need memory layers SCOPED PER ENGAGEMENT so the wrong client's conventions don't leak. Mechanism: a per-engagement file (e.g., `~/engagements/client-X/memory.md`) updated after each session with structured sections (repo conventions, reviewer preferences per person, deploy quirks, recurring traps, glossary terms, resolved-questions log). Files are versioned, indexed, and surfaced to the LLM agent on session start. Primary output: a memory file per engagement + a session-start hook that loads the relevant memory + a session-end discipline of writing back any new patterns observed.

## Applies If (ALL must hold)

- contractor / freelancer working on >= 2 active engagements
- each engagement has distinct repo conventions, reviewer preferences, or deploy paths
- contractor uses an LLM agent (Claude Code, Cursor, etc.) where pre-session context matters
- memory write discipline is realistic (10-15 min at session end)

## Skip If (ANY kills it)

- single-client / employee with one codebase — single pattern-memory file is sufficient
- engagement is &lt;= 1-2 sessions total — overhead exceeds value
- contractor doesn't use an LLM agent — written memory still valuable but the wiring is different
- engagement has no reviewer / convention drift across sessions (rare)

## Prerequisites

- defined location for engagement files (e.g., `~/engagements/<client>/memory.md`)
- session-start practice: agent loads the engagement's memory before any code work
- session-end practice: contractor reviews session for new patterns, writes back
- glossary discipline (terms specific to this engagement, distinct from other engagements)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/pattern-memory` | Generic pattern memory; this methodology scopes patterns per-engagement |
| `solo/sdd/sdd/mistake-memory` | Same; per-engagement mistakes are tracked here, not in a shared mistake file |
| `pro/ba/business-analyst/glossary-management-living-doc` | Per-engagement glossary uses lifecycle rules from this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-engagement-scope, session-end-write-discipline, glossary-isolated-per-engagement, decay-cleanup-quarterly, no-cross-engagement-leak | ~1000 |
| `content/02-output-contract.xml` | essential | Memory file shape + session-update contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (memory bleed, write-skip, stale-entries, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `session_start_summary` | haiku | Load engagement memory + recent commits, produce 1-page brief |
| `pattern_extraction_from_session` | sonnet | At session-end, scan transcript for new repo patterns / reviewer comments / glossary additions |
| `cross_engagement_consistency_audit` | sonnet | Monthly: detect patterns that show up across multiple engagements (signal of cross-leak) |
| `memory_cleanup_quarterly` | sonnet | Prune stale entries; merge near-duplicates |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-memory.md` | Per-engagement file skeleton (sections: conventions, reviewers, deploy, traps, glossary, resolved-q-log) |
| `templates/session-end-checklist.md` | Quick checklist for writing back patterns at session end |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/load-engagement-memory.sh` | Shell hook: load the relevant memory file at session start | Session start (cd into engagement workspace) |
| `scripts/audit-memory-leak.py` | Compares engagement memory files for unintended overlap | Monthly |
| `scripts/decay-cleanup.py` | Flags entries older than 90 days with no reference for cleanup | Quarterly |

## Related

- parent skill: `solo/sdd/sdd/`
- peer methodologies: `pattern-memory`, `mistake-memory`, `session-state`
- external: [GTD Contexts (Allen)](https://gettingthingsdone.com/) · [Memory pattern in workflows (Anthropic Memory tool docs)](https://docs.anthropic.com/) · [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law)
