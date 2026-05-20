---
slug: task-agent-fixable-triage-gate
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agents that turn issues into pull requests (Devin, Copilot Coding Agent, Codex, Cursor Background) waste tokens spinning on tickets they cannot solve: no acceptance criteria, no reproducible bug, blocked on product decisions, or duplicates of an existing issue.
content_id: "6dfd70640e4cb475"
tags: [task-lifecycle, triage, agent-fleet, label-gate, coding-agent]
---
# `agent-fixable` Triage Gate (Humans Pick, Agents Work)

## Summary

**One-sentence:** Agents that turn issues into pull requests (Devin, Copilot Coding Agent, Codex, Cursor Background) waste tokens spinning on tickets they cannot solve: no acceptance criteria, no reproducible bug, blocked on product decisions, or duplicates of an existing issue.

**One-paragraph:** Agents that turn issues into pull requests (Devin, Copilot Coding Agent, Codex, Cursor Background) waste tokens spinning on tickets they cannot solve: no acceptance criteria, no reproducible bug, blocked on product decisions, or duplicates of an existing issue. Insert a triage gate as a label — agent-fixable (or copilot, devin-pickup) — applied by a human or by a triage bot AFTER spam/duplicate/scope checks. The coding agent only listens for that label, never for "issue opened". Cognition's published Devin numbers show PR merge rate climbing from 34% to 67% over 2025 once gating was added; the same shape works for any coding agent fleet.

## Applies If (ALL must hold)

- Issue trackers with more than 50 open items where agents would otherwise pick the wrong ones.
- Mixed agent fleets (Devin + Copilot + Codex + Cursor) sharing the same backlog.
- Repos with strict CODEOWNERS where mis-routed agent attempts produce noisy stale PRs.
- Teams adopting their first coding agent — start with a tiny agent-fixable allowlist, expand as merge rate stabilizes.

## Skip If (ANY kills it)

- Tiny backlogs (fewer than 10 open issues) where a human picks each issue manually anyway.
- Tickets needing product discovery, not code — those should carry needs-spec, never agent-fixable.
- One-off prototypes with no merge rate to optimize.
- Teams that have not yet defined what "fixable by an agent" means — write the criteria first, label after.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
