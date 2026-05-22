---
slug: customer-support-inbox-sweep-2x-weekly
tier: solo
group: solo-saas
persona: P1
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Zero unread customer messages: each ticket resolved or scheduled, top 3 themes pushed into product feedback, churn signals flagged, FAQ updated where the same answer was given twice."
content_id: 19d656c6c18bfc1a
methodology_refs:
  - active-listening
  - continuous-discovery
  - mom-test
  - feedback-management
  - stakeholder-communication
  - ops-customer-support
  - backlog-management
---

# Customer support inbox sweep (2x weekly)

## Intent

Zero unread customer messages: each ticket resolved or scheduled, top 3 themes pushed into product feedback, churn signals flagged, FAQ updated where the same answer was given twice.

## Scope

Zero unread customer messages: each ticket resolved or scheduled, top 3 themes pushed into product feedback, churn signals flagged, FAQ updated where the same answer was given twice.

## Stages

### 1. Inbox triage

Zero unread, every ticket categorised.

Tasks:
- Open the support inbox
- Tag each ticket: bug / feature / billing / churn-signal
- Set a target response time per category

Outputs:
- Tagged inbox
- Category counts
- Response-time SLA per category

Decision gate: Advance only when inbox count = 0 unread.

### 2. Resolve or schedule

Every ticket either closed today or has a scheduled reply.

Tasks:
- Resolve quick wins (<=5 minutes each)
- Schedule callbacks for deeper issues
- Escalate billing / churn signals immediately

Outputs:
- Resolved ticket count
- Scheduled callbacks
- Escalation log

Decision gate: Advance only when every ticket has either a resolution or a scheduled action.

### 3. Verbatim to backlog

Move 3 themes from tickets into product roadmap.

Tasks:
- Cluster ticket topics into 3 themes
- Capture verbatim quotes per theme
- Add or up-vote backlog items

Outputs:
- Top-3 themes
- Verbatim quote bank
- Backlog deltas

Decision gate: Advance only when themes are added to backlog with quotes attached.

### 4. FAQ + canned reply update

Stop answering the same question twice.

Tasks:
- Identify any question answered >=2 times this sweep
- Add an FAQ entry or update the doc page
- Save a canned reply template

Outputs:
- FAQ updates
- Canned reply additions
- Updated knowledge base link

Decision gate: Advance only when every asked-twice question is now self-serve.

### 5. Churn signal flag

Catch leaving users before they go silent.

Tasks:
- Tag tickets with churn-risk signal
- Trigger a save email or call for each
- Pass churn themes to the next retention review

Outputs:
- Churn-flag list
- Save actions log
- Themes for retention

Decision gate: Cycle closes when each churn flag has a save action initiated.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
