---
slug: weekly-client-status-report-outsource
tier: pro
group: client-engagement
persona: P4
goal: operate-ritual
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: End-of-week RAG report that the offshore senior owns → client PM forwards upstream without rewriting, pre-empts Monday interrogation.
content_id: f4ffc0f7f27da9c3
methodology_refs:
  - stakeholder-analysis
  - risk-register
  - active-listening
  - communications-management
  - business-storytelling
  - selling-ideas
  - weekly-status-report-outsource-template
  - rag-translation-for-non-tech-stakeholders
---

# Weekly client status report (outsource senior)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** light · **Angle:** atomic

## Why this playbook exists

End-of-week RAG report that the offshore senior owns → client PM forwards upstream without rewriting, pre-empts Monday interrogation.

Atomic weekly ceremony for an offshore senior who owns the report (not the PM). By Friday cutoff: a six-section RAG status with progress vs sprint goal, risks, asks, ready for upstream forwarding without rewriting. Bridges the gap between vendor-side ground truth and client-side stakeholder expectations.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

A weekly status report from an outsource senior is a forwarding decision, not a status update. The client PM either forwards it upstream unchanged or rewrites it. Each rewrite is signal: the report did not survive contact with the upstream reader. Aim for the report to be the upstream artefact, not the input to one.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Collect

**Intent:** Pull facts from the sprint board, not your head.

**Tasks**
- Snapshot sprint progress against goal
- Pull risk register deltas this week
- Identify open asks blocked on client side
- Stakeholder-analysis on who the report needs to land for

**Outputs**
- Fact pack (sprint metrics, risk deltas, asks list)

**Decision gate**

Advance when every claim in the fact pack can be traced to a board, PR, or doc.

Collection is sometimes painful because the sprint board lies about progress in week 3 of a fortnight sprint. Pull the numbers regardless. If the board says one thing and your gut says another, write down the gut version and chase the board to reflect reality before sending.

### Stage 2 — Compose

**Intent:** Six sections, plain language, no padding.

**Tasks**
- Headline RAG with one-line justification
- Progress vs goal (numbers, not adjectives)
- Risks + mitigations + owners
- Asks + decisions needed
- Next-week plan
- Stakeholder narrative (storytelling for the upstream audience)

**Outputs**
- Drafted report

**Decision gate**

Advance only if every RAG colour has data behind it.

Composition is where most outsource seniors stumble. They write for themselves — 'I shipped X, Y, Z' — when the upstream reader wants the answer to 'is anything on fire?' first. Lead with RAG, then progress, then risks, then asks. Numbers wherever possible.

### Stage 3 — Send + follow-up

**Intent:** Ship inside the window and pre-empt the Monday interrogation.

**Tasks**
- Send to client PM in the agreed channel by Friday cutoff
- Confirm receipt; offer 10-min call window
- Pin asks at the top of Monday's first comms
- Archive in engagement journal

**Outputs**
- Sent report
- Journal entry

**Decision gate**

Done only after client PM has acknowledged. Silence = follow-up Monday morning.

Sending is a real step, not a footnote. Friday 17:00 local-to-the-client is the magic window for most US/EU PMs; Friday 23:00 your time is too late for them and too late for you. Confirm receipt; offer a quick call; archive in the engagement journal so retros land.

## Common pitfalls

- Green RAG every week — kills the signal value
- Asks buried at the bottom — the upstream reader never sees them
- Sending Friday 23:55 your time — the client PM cannot use it

## Quality checklist

- Could the client CEO read it cold and know what's hot?
- Did I name every ask + owner + decision date?
- Did I send in the window the client PM can act on?

## Related playbooks

- `cross-timezone-async-daily-standup`
- `client-demo-prep-and-run`

## Closing note

Pair this playbook with the async daily standup playbook to cover the full reporting cadence. Together they pre-empt every Monday-morning fire-drill, and they give the client PM the artefacts they need to defend the engagement upstream when budgets get scrutinised.

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `weekly-status-report-outsource-template` (blocks stage 2)
- `rag-translation-for-non-tech-stakeholders` (blocks stage 2)
