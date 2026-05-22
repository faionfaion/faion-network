---
slug: mob-programming
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a mob-programming session plan (driver rotation, strong-style enforcement, agent role + human cap) for high-stakes work.
content_id: "e910f6c825d84b76"
complexity: medium
produces: playbook-step
est_tokens: 3400
tags: [mob, collaboration, agent-assisted, rotation]
---
# Mob Programming

## Summary

**One-sentence:** Plans a mob-programming session capped at 4 humans + 1 agent, with explicit driver rotation, strong-style rule, and facilitator role.

**One-paragraph:** Mob programming concentrates the team's attention on one problem; without structure it devolves into the loudest voice driving. This methodology emits a session plan: rotation interval (5-15 min), driver / navigator / researcher assignments, agent role (transcription, snippet retrieval — never primary navigator), strong-style enforcement (no key without spoken intent), and a human-facilitator. Output is the plan a session lead executes; metrics (decisions per hour, defects-per-mob-hour) feed a post-session report. Cap at 4 humans + 1 agent.

**Ефективно для:**

- High-stakes refactor: вся команда в темі за одну сесію замість 5-ти PR.
- Onboarding senior: новачок як driver, mob як 'live tutorial'.
- Architectural decision: рішення приймає mob — наявні всі stakeholders.
- AI-augmented session: agent в ролі researcher / snippet-retriever, never primary driver.

## Applies If (ALL must hold)

- ≥3 humans available for the session.
- Topic is non-trivial (not boilerplate / mechanical refactor).
- Decision authority for the topic is present in the mob.

## Skip If (ANY kills it)

- Mechanical / boilerplate task — pair or solo.
- Async-only team (timezone gap &gt; 4h).
- Hot incident — mob slows triage; use pair + standby.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Topic + scope | Markdown | session brief |
| Attendee list | list | calendar invite |
| Agent permission set | JSON | session policy |
| Recording / transcript tool | string | Otter / agent transcript |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-human-cap, rotation-required, strong-style, agent-not-primary, facilitator-named | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for session plan + report | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: loudest-voice, agent-takeover, no-rotation | 600 |
| `content/04-procedure.xml` | essential | 5-step session procedure | 700 |
| `content/06-decision-tree.xml` | essential | Topic + team-shape tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan_session` | sonnet | Session-shape decisions. |
| `agent_during_session` | haiku | Snippet retrieval / transcription only. |
| `post_report` | sonnet | Synthesises decisions + metrics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-driver-prompt.txt` | Prompt scoping the agent to driver-only typing role |
| `templates/agent-navigator-prompt.txt` | Prompt scoping the agent to navigator-suggestion role |
| `templates/rotation-log.sh` | Shell that logs rotation timestamps |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mob-programming.py` | Validate session plan + report against schema | Before session start; after session end |

## Related

- - [[pair-programming]] — same family; 2-person variant.
- - [[code-review-process]] — mob-derived decisions land via this review path.

## Decision tree

See `content/06-decision-tree.xml`. Branches: topic complexity (high vs mechanical), team size (3-4 vs 5-8), agent role (researcher / transcript / none). Each leaf points at the rule that governs the chosen shape.
