---
slug: async-cross-timezone-delivery-cadence-p4-outsource
tier: solo
group: role-project-manager
persona: PM on a P4 outsource engagement with <2h overlap between dev team and client
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Sustainable ceremony rhythm when PM, dev, and client overlap <2h/day: standups, planning, demos, retros, status all running async-first."
content_id: 24345646819600cf
methodology_refs:
  - ai-in-project-management
  - ai-powered-pm-tools
  - kanban-scaled-agile-ceremonies
  - scrum-ceremonies
  - communications-management
  - agile-ceremonies-setup
---

# Async cross-timezone delivery cadence (P4 outsource)

## Context

PM is running a P4 outsource engagement where the dev team and client share <2h overlap. This playbook sets up the recurring cadence: async standups, async sprint planning, recorded demos, async retros, and an AI-assisted client status digest. Sync events are scheduled only when a decision is blocked. Done when one full sprint has completed without a missed deliverable and the client opted into the async cadence.

## Outcome

Sync-first ceremony chaos -> async-first rhythm with sync events only when blocking. Sustainable ceremony rhythm when PM, dev, and client overlap <2h/day: standups, planning, demos, retros, status all running async-first.

## Steps

1. Know exactly when sync is even possible. Plot working hours per person across all timezones; Identify the realistic overlap window; Mark non-overlap blocks as async-only territory
2. Daily standup as written thread, not a meeting. Stand up a daily async-standup thread in Slack/Teams; Template: yesterday / today / blockers; Require posts before each contributor's local 11:00
3. Sprint planning and retro across timezones without a 2h meeting. Pre-fill sprint plan template; team comments + votes async over 24h; Run async retro with structured prompts collected over 48h; Reserve 30 min sync only for unresolved planning conflicts
4. Client sees progress on their own time. Record 5-10 min Loom-style demo at end of sprint; Post in client channel with embedded next-step questions; Schedule sync demo only if client requests decisions
5. Weekly client status assembled by AI from artifacts. Configure AI pipeline to pull standup threads + Jira deltas; Auto-draft weekly status; PM reviews + signs; Deliver to client on a fixed day/time
6. Get explicit client opt-in so the cadence sticks. Document the async cadence in the engagement charter; Get written client acceptance; Schedule a 30-day check-in to recalibrate

## Decision points

- **Map overlap** -> Advance only after the team agrees on the overlap window.
- **Convert standups** -> Advance when 5 consecutive days have full participation.
- **Convert planning + retros** -> Advance only when first cycle of async planning + retro completes inside SLA.
- **Recorded demos** -> Advance when client responds to demo without requesting a sync call.
- **AI status digest** -> Advance when client accepts the digest as the primary status channel.
- **Lock cadence** -> Done when charter is signed and 30-day check-in is on the calendar.

## References

- `faion/knowledge/geek/pm/pm-agile/ai-in-project-management`
- `faion/knowledge/geek/pm/pm-agile/ai-powered-pm-tools`
- `faion/knowledge/pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `faion/knowledge/pro/pm/pm-agile/scrum-ceremonies`
- `faion/knowledge/pro/pm/pm-traditional/communications-management`
- `faion/knowledge/pro/pm/project-manager/agile-ceremonies-setup`
- Related: `run-an-escalation-conversation-with-a-stakeholder`, `ai-assisted-sprint-planning-with-capacity-reality-check`
