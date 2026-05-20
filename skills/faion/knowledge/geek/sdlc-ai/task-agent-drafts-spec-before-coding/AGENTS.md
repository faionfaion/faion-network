---
slug: task-agent-drafts-spec-before-coding
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When an AI coding agent is assigned a tracker ticket (Linear, Jira, GitHub, GitLab), its first action MUST be a "current state / desired state / proposed plan" comment posted back on the issue, not a code edit.
content_id: "4d559cb3fec82cbe"
tags: [task-lifecycle, spec, agent-workflow, approval-gate, tracker]
---
# Agent Drafts Spec Before Coding

## Summary

**One-sentence:** When an AI coding agent is assigned a tracker ticket (Linear, Jira, GitHub, GitLab), its first action MUST be a "current state / desired state / proposed plan" comment posted back on the issue, not a code edit.

**One-paragraph:** When an AI coding agent is assigned a tracker ticket (Linear, Jira, GitHub, GitLab), its first action MUST be a "current state / desired state / proposed plan" comment posted back on the issue, not a code edit. The agent gathers the issue body plus linked context (Notion spec, Slack thread, prior similar issues, code-intel search) and emits a structured spec draft. Implementation only begins after a specialist signals approval — Linear thumbs-up emoji on the agent's comment, Jira /agent approve slash command, or an explicit agent:approved label transition. First-try-pass on coding (no spec gate) means the agent skipped the discovery step and is fabricating intent.

## Applies If (ALL must hold)

- Ticket is assigned to an AI coding agent on Linear, Jira, GitHub, or GitLab as the primary owner of the work.
- Issue has any non-trivial scope: feature work, multi-file bug fix, refactor, migration.
- Team has at least one human reviewer who can react with a thumbs-up or run an approval slash command.
- Workflow auto-closes the issue on PR merge (Fixes #N, Closes !N) — the spec comment becomes the linkable record of intent.

## Skip If (ANY kills it)

- Trivial tickets pre-flagged agent:auto-approve (typo fixes, dependency bumps, log-message tweaks) — gate cost exceeds risk.
- Spike or research tickets where the desired state is itself the deliverable; the agent's job is to discover, not to commit code.
- Hot-path incident response where a postmortem ticket is filed after the fact; spec drafting belongs to the retro, not the fix.
- Single-author solo projects with no second human in the loop — the gate has no approver and the agent stalls.

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
