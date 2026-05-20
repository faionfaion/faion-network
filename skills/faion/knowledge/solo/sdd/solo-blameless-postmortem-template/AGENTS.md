---
slug: solo-blameless-postmortem-template
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "50d0f1c3712d634f"
summary: A 20-minute postmortem template sized for one human — fills mistakes.md and patterns.md directly, with no retro meeting, no blame language, and no team-scale rituals.
---
# Solo Blameless Postmortem Template

## Summary

**One-sentence:** Single-page postmortem template that a solo founder completes in 20 minutes after a production incident, with structured output that lands directly in `.aidocs/memory/mistakes.md` and `patterns.md`.

**One-paragraph:** Standard blameless-postmortem methodologies assume a team (facilitator, scribe, retro meeting, action-owner). A solo founder has none of those roles available. This methodology defines a small, opinionated template the founder fills alone: timeline (5 lines), trigger, contributing factors (max 3), what worked, action item (exactly 1, with a date or kill it), and a one-line entry written in the canonical form that `sdd/mistake-memory` consumes. The "blameless" language stays — the inner critic does the same damage as a hostile teammate. Anchored to "Solo prod incident response (no team safety net)" for the solo SaaS builder.

## Applies If (ALL must hold)

- A user-visible incident occurred (downtime, data loss, charge error, broken core flow ≥ 5 minutes).
- You are the only person responsible — no on-call rotation, no team retro.
- The SDD memory system (`.aidocs/memory/mistakes.md`, `patterns.md`) is in place or you commit to standing it up.
- You can complete the template within 24 hours of resolution.

## Skip If (ANY kills it)

- Trivial bug fixed before any user noticed and with zero risk of recurrence — log a one-line note in the bug tracker, that is enough.
- Mid-incident, still mitigating — finish the fix first; postmortem is for after stability.
- Multi-person team — use the team-scale blameless postmortem patterns (`geek/sdlc-ai/blameless-postmortem-facilitation`) instead.

## Prerequisites

- Access to incident timeline data (logs, monitoring snapshots, user reports).
- Write access to `.aidocs/memory/mistakes.md` and `patterns.md`.
- A calendar block of 20 minutes within 24h of resolution.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/AGENTS.md` | Parent group context |
| `solo/sdd/sdd/mistake-memory` if present | Defines the canonical mistakes.md entry shape this template emits |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every solo postmortem enforces | ~900 |

## Related

- parent skill: `solo/sdd/`
- triggering activity: `p1-solo-saas-builder/Solo prod incident response (no team safety net)`
- adjacent: `geek/sdlc-ai/blameless-postmortem-facilitation` (team variant)
