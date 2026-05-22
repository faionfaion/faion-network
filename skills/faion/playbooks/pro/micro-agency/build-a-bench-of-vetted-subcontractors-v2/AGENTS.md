---
slug: build-a-bench-of-vetted-subcontractors-v2
tier: pro
group: micro-agency
persona: p5-micro-agency-founder
goal: hire-onboard
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Stand up a 5–10 person freelance bench you can call within 48h, with a documented audition flow, rate card, NDA/IP boilerplate, and quality-bar mechanism. Goal: deliver 2x revenue with no W-2 hires..."
content_id: f545af817e63d424
methodology_refs:
  - onboarding
  - recruiting-process
  - star-interview-framework
  - structured-interview-design
  - ops-contractor-basics
  - ops-contractor-management
  - ops-legal-basics
  - resource-management
---

# Build a bench of vetted subcontractors without becoming an agency-of-agencies

## Context

Stand up a 5–10 person freelance bench you can call within 48h, with a documented audition flow, rate card, NDA/IP boilerplate, and quality-bar mechanism. Goal: deliver 2x revenue with no W-2 hires and no founder bottleneck on quality.

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Define the Bench Need

Which roles, how often, at what rate.

Tasks:
- List the 3-5 roles you most often need at short notice
- Define ICP per role: stack, timezone, rate ceiling, language
- Set the target bench size per role (2-3 vetted each)

Outputs:
- roles list
- ICP-per-role doc
- bench-size target

Decision gate: Advance only when every role has an ICP and a target headcount.

### 2. Source Candidates

Build the bench without becoming an agency-of-agencies.

Tasks:
- Run a small sourcing batch per role (referrals + 1 channel each)
- Screen for stack, timezone, rate, and English fluency before interview
- Send a paid test task to top 3 per role

Outputs:
- sourcing log per role
- screening notes
- paid test results

Decision gate: Advance when each role has ≥2 candidates clearing the test bar.

### 3. Sign & File

Make calls fast in the future.

Tasks:
- Sign master service agreements with each accepted bench contractor
- Store rate cards, availability, and references in one place
- Onboard them lightly: comms norms, IP, NDA

Outputs:
- signed MSAs
- bench directory file
- comms/IP/NDA acknowledgements

Decision gate: Advance only when each role has ≥2 contractors with signed MSAs on file.

### 4. Rotate & Refresh

Keep the bench warm without faking work.

Tasks:
- Run a one-line monthly check-in: still available, still same rate
- Drop contractors who can't be reached or whose rate moved out of band
- Refill any role whose bench drops below target

Outputs:
- monthly check-in log
- drop list
- refilled roles

Decision gate: Required output: bench directory is current as of this month.

## Decision points

- Stage 1 (Define the Bench Need): Advance only when every role has an ICP and a target headcount.
- Stage 2 (Source Candidates): Advance when each role has ≥2 candidates clearing the test bar.
- Stage 3 (Sign & File): Advance only when each role has ≥2 contractors with signed MSAs on file.
- Stage 4 (Rotate & Refresh): Required output: bench directory is current as of this month.

## References

- `onboarding`
- `recruiting-process`
- `star-interview-framework`
- `structured-interview-design`
- `ops-contractor-basics`
- `ops-contractor-management`
- `ops-legal-basics`
- `resource-management`

Gaps (status: draft until empty):
- `contractor-audition-flow` (see `gaps[]` in `playbook.yaml`)
- `bench-management-tiering` (see `gaps[]` in `playbook.yaml`)
- `agency-ip-nda-boilerplate` (see `gaps[]` in `playbook.yaml`)
- `worker-misclassification-self-audit` (see `gaps[]` in `playbook.yaml`)
