---
slug: active-listening
tier: solo
group: comms
domain: communicator
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured listening practice (RASA: Receive, Appreciate, Summarize, Ask) that ensures the speaker feels understood before the listener responds.
content_id: "f164ee2ae0f5bedf"
tags: [listening, rasa, empathy, requirements-gathering, communication]
---
# Active Listening

## Summary

**One-sentence:** A structured listening practice (RASA: Receive, Appreciate, Summarize, Ask) that ensures the speaker feels understood before the listener responds.

**One-paragraph:** A structured listening practice (RASA: Receive, Appreciate, Summarize, Ask) that ensures the speaker feels understood before the listener responds. Combines paraphrasing, mirroring, open questions, and empathic reflection to reach Level 5 empathic listening — understanding both content and emotion.

## Applies If (ALL must hold)

- Requirements gathering sessions with stakeholders or clients
- 1-on-1 meetings where trust or engagement is at risk
- Customer discovery interviews (especially with skeptical interviewees)
- Conflict situations where one party feels misunderstood
- Performance discussions or coaching conversations

## Skip If (ANY kills it)

- Real-time agent conversations — agents cannot perform empathic listening live; they can scaffold it but not execute it
- High-stakes interpersonal conflicts — a script-driven approach risks feeling mechanical and backfiring
- Situations where a direct answer is needed and the other party is not emotionally engaged
- Asynchronous text threads where silence and pace cues are absent

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

- parent skill: `solo/comms/communicator/`
