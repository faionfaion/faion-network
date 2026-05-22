---
slug: adr-write-up-client-architecture
tier: pro
group: business-analysis
persona: P4
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Capture one architecture decision so the client ARB accepts it, AI agents can replay it, and the next dev finds it in 18 months.
content_id: 75a9c0a8e67f4700
methodology_refs:
  - requirements-traceability
  - quality-attributes-analysis
  - architecture-decision-records
  - stakeholder-engagement
  - business-storytelling
  - selling-ideas
  - adr-for-client-arb-review-template
  - living-documentation
  - stack-mandate-tradeoff-frame
---

# ADR write-up for client architecture decision

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** medium · **Angle:** atomic

## Why this playbook exists

Capture one architecture decision so the client ARB accepts it, AI agents can replay it, and the next dev finds it in 18 months.

Atomic doc task: one architecture decision committed to an ADR ready for client architecture review board. Output: ADR + decision-driver chain + tradeoff frame + AI-replayable summary. Used 1-3 times per sprint on a typical engagement.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

Architecture decisions inside a client engagement die one of two deaths: written so densely no one reads them, or so loosely nobody can reproduce the choice. An ADR that survives a client ARB AND lets the AI coding agent replay the decision 18 months later is rare — and shippable in 60-90 minutes if you have the frame.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Frame decision

**Intent:** Make the decision before you write the doc.

**Tasks**
- Walk the decision driver chain (what triggered it)
- List alternatives considered
- Map to quality attributes (perf, sec, availability, cost)
- Trace to requirements / business goals

**Outputs**
- Decision draft notes
- Alternatives shortlist

**Decision gate**

Advance only when ≥2 alternatives were honestly considered.

Framing the decision honestly is harder than it looks. Walk the driver chain: what triggered the decision, who pushed for it, what alternatives are real. If you cannot name two alternatives that were genuinely considered, the doc is going to look defensive at the ARB.

### Stage 2 — Write ADR

**Intent:** Convert the decision into a doc the ARB accepts.

**Tasks**
- Use the architecture-decision-records pattern
- Storytelling: context → decision → consequences
- Selling-ideas: defend the choice without overselling
- Capture stakeholder context for ARB review

**Outputs**
- ADR draft

**Decision gate**

Advance only when the ADR is self-contained (a stranger reads it without context).

Writing the ADR uses the storytelling frame: context, decision, consequences. Selling-ideas discipline matters — defend the choice without overselling. Stakeholder context goes in so the ARB reader does not have to chase background. Self-contained is the bar.

### Stage 3 — Tradeoff + AI-replayable summary

**Intent:** Make the doc resilient for AI agents and future devs.

**Tasks**
- Frame stack-mandate tradeoffs explicitly
- Write the AI-agent-replayable summary block
- Index in living-documentation
- File with the client ARB

**Outputs**
- Final ADR
- AI-replayable summary
- ARB submission record

**Decision gate**

Done when ADR is indexed AND an AI-agent can answer 'why this choice' from the doc alone.

Tradeoff + AI-replayable summary is the part that future-proofs the doc. AI agents read the summary block and reuse the decision; the next dev finds the doc by repo search; the ARB ratifies because the tradeoffs are explicit. Three audiences, one doc, by deliberate design.

## Common pitfalls

- Writing the ADR after the decision is forgotten — drift between doc and intent
- Skipping alternatives — looks defensive at ARB
- No AI-replayable summary — agents reinvent the decision next sprint

## Quality checklist

- Could the next dev find this ADR via repo search?
- Did the ARB ratify it without rewrites?
- Does the AI summary survive a context-free read?

## Related playbooks

- `jira-ticket-scoping-session`
- `compliance-grade-feature-delivery`

## Closing note

Run this 1-3 times per sprint on a typical engagement. Pair with the JIRA scoping playbook for upstream context and the compliance-grade feature delivery playbook when the decision touches a regulated boundary.

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `adr-for-client-arb-review-template` (blocks stage 2)
- `stack-mandate-tradeoff-frame` (blocks stage 3)
