---
slug: pivot-from-failed-v1-to-v2
tier: pro
group: solo-saas
persona: P1
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "v1 is not working: retention flat, growth stalled, founder energy bleeding."
content_id: 7a7ea7fdbfcd96c5
methodology_refs:
  - ops-churn-basics
  - growth-landing-page-design
  - retention-metrics
  - product-launch
  - competitive-intelligence
  - spec-writing
  - market-analysis
  - niche-evaluation
  - difficult-conversations
  - jobs-to-be-done
  - stakeholder-communication
  - pain-point-research
  - architecture-decision-records
  - mistake-memory
  - technical-debt
  - reflexion-learning
  - growth-email-marketing
  - writing-specifications
---

# Pivot from failed v1 to v2

## Intent

v1 is not working: retention flat, growth stalled, founder energy bleeding.

## Scope

v1 is not working: retention flat, growth stalled, founder energy bleeding. Decide and execute a structured pivot (segment / feature / model / sunset) without burning the brand or the customer trust.

## Stages

### 1. Honest diagnosis

Name what failed and why - no euphemisms.

Tasks:
- Compile retention, growth, and energy data
- Interview self + top 3 advisors
- Write a 1-page failure post-mortem

Outputs:
- Failure post-mortem
- Energy/burnout audit
- Top-3 contributing causes

Decision gate: Advance only with a written cause, not a vibe.

### 2. Pivot vs quit decision

Use a decision template before the heart picks for you.

Tasks:
- Walk the pivot-vs-quit template
- List 3 candidate pivot vectors (segment / feature / model / sunset)
- Score each against runway, energy, and evidence

Outputs:
- Decision template filled
- Scored vector table
- Chosen vector OR sunset call

Decision gate: Advance only if one vector has clearly higher score AND positive energy signal.

### 3. Re-validation interviews

Confirm the new direction with the same rigor as v1.

Tasks:
- Run 10 Mom-test interviews in the new niche
- Test the new JTBD framing
- Tag severity + willingness-to-pay

Outputs:
- 10 interview transcripts
- Validated JTBD v2
- Pricing signal v2

Decision gate: Advance only with >=5/10 strong painpoint matches. Else revisit vector.

### 4. Customer comms plan

Protect trust with existing v1 customers.

Tasks:
- Segment current customers (migrate / refund / sunset)
- Draft difficult-conversation comms per segment
- Schedule the announcement window

Outputs:
- Customer segmentation
- Comms templates per segment
- Refund/migration policy

Decision gate: Advance only when comms templates are reviewed by one outside reader.

### 5. Tech-debt audit

Decide what code to keep, refactor, or burn.

Tasks:
- Inventory the v1 codebase with ADRs
- Mark each module: reuse / refactor / kill
- Write a migration plan with explicit cuts

Outputs:
- Code inventory
- Migration plan
- Updated ADRs

Decision gate: Advance only when reuse % is clearly justified (or honestly accept a rewrite).

### 6. v2 spec + scope cut

Write a deliberately small v2 spec.

Tasks:
- Write a 1-page v2 spec
- List explicit non-goals
- Map acceptance criteria per feature

Outputs:
- spec-v2.md
- Non-goals list
- Acceptance criteria table

Decision gate: Advance only if v2 spec is smaller than v1 spec at equivalent stage.

### 7. Launch v2 quietly

Ship to a small, friendly audience first.

Tasks:
- Migrate or refund v1 users on schedule
- Soft-launch v2 to design partners
- Hold off a public re-launch until retention curve forms

Outputs:
- Migration log
- v2 soft-launch announcement
- Early retention chart

Decision gate: Advance when first cohort hits week-4 retention threshold.

### 8. Brand-trust audit

Check trust signals before going wide.

Tasks:
- Pull sentiment from socials, reviews, and inbox
- Surface any open trust debt from v1 sunset
- Address each item publicly or privately

Outputs:
- Trust audit report
- Resolved-issue list
- Public follow-up post (if needed)

Decision gate: Advance only when no open public trust debt remains.

### 9. Pattern + mistake memory

Lock the lesson so v2 does not repeat v1.

Tasks:
- Write a reflexion doc
- Update pattern memory with what saved time
- Update mistake memory with traps that bled v1

Outputs:
- Reflexion doc
- Pattern memory delta
- Mistake memory delta

Decision gate: Cycle closes when memories are committed and reviewed.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
