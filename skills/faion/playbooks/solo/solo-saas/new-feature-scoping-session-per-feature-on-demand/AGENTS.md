---
slug: new-feature-scoping-session-per-feature-on-demand
tier: solo
group: solo-saas
persona: P1
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "From request to ready-to-ship slice: signal validated, MVP cut to bone, spec written, flag plan decided, success metric defined — all before any code is generated."
content_id: 7b8dd637dec31e64
methodology_refs:
  - mom-test
  - spec-writing
  - feature-flags-rollout-targeting
  - minimum-product-frameworks
  - feature-flags
  - market-researcher
  - continuous-discovery
  - spec-structure
  - feature-prioritization-rice
  - writing-specifications
  - micro-mvps
  - mvp-scoping
---

# New feature scoping session (per-feature, on demand)

## Intent

From request to ready-to-ship slice: signal validated, MVP cut to bone, spec written, flag plan decided, success metric defined — all before any code is generated.

## Scope

From request to ready-to-ship slice: signal validated, MVP cut to bone, spec written, flag plan decided, success metric defined — all before any code is generated.

## Stages

### 1. Validate the request

Confirm the signal is real, not vocal-minority.

Tasks:
- Count how many users asked for this in the last 30 days
- Run 2 quick Mom-test calls if signal is thin
- Tag the JTBD this feature touches

Outputs:
- Signal count
- 2 call notes (if needed)
- JTBD tag

Decision gate: Advance only when signal >=3 distinct users OR clear JTBD match.

### 2. Cut to the bone

Find the smallest scope that delivers the JTBD.

Tasks:
- List the full feature surface as imagined
- Cut to a micro-MVP that delivers the JTBD
- Capture explicit non-goals

Outputs:
- Full feature surface
- Micro-MVP scope
- Non-goals list

Decision gate: Advance only when scope fits in 1 page AND cuts >=50% of original surface.

### 3. Write the spec

Write the spec with acceptance criteria.

Tasks:
- Use the spec-structure template
- Define acceptance criteria per AC line
- List dependencies and risks

Outputs:
- feature-spec.md
- Acceptance criteria table
- Risk list

Decision gate: Advance only when every AC is testable.

### 4. Flag plan

Decide the rollout shape before code.

Tasks:
- Pick the feature-flag strategy (canary / all-users / off)
- Define the kill-switch trigger
- Document the rollback path

Outputs:
- Flag plan
- Kill-switch trigger
- Rollback runbook

Decision gate: Advance only when there is a documented rollback in <=15 minutes.

### 5. Success metric

Define how you will know it worked.

Tasks:
- Pick one north-star metric that should move
- Set the threshold for this was worth it
- Wire metrics in the spec

Outputs:
- Success metric
- Threshold
- Metric wiring note

Decision gate: Advance only with a single north-star metric committed.

### 6. Build-or-waitlist gate

Confirm we are actually building, not waitlisting.

Tasks:
- Compare effort to other top-3 outcomes
- Decide build-now / waitlist / cut
- Write the rationale

Outputs:
- Build/waitlist/cut call
- Rationale doc
- Backlog update

Decision gate: Cycle closes when the call is committed in writing.

### 7. Schedule + briefing pack

Hand the spec to the executor (you or AI agent).

Tasks:
- Prepare the agent briefing pack (spec + context + tests)
- Schedule the build slot
- Pre-load the first task file

Outputs:
- Briefing pack
- Calendar slot
- First task file

Decision gate: Cycle closes when the next slot is on the calendar and pre-loaded.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
