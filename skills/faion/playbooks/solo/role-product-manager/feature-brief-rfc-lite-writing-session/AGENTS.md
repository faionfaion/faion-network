---
slug: feature-brief-rfc-lite-writing-session
tier: solo
group: role-product-manager
persona: role-product-manager
goal: plan-design
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One feature spec written end-to-end: problem, users, success metric, scope, out-of-scope, open questions; ready for engineering and design review."
content_id: aa0ee212dec1d60e
methodology_refs:
  - stakeholder-management
  - opportunity-solution-trees
  - mvp-scoping
  - product-discovery
  - product-launch
  - spec-writing
  - user-story-mapping
  - success-metrics-definition
---

# Feature brief / RFC-lite writing session

## Context

One feature spec written end-to-end: problem, users, success metric, scope, out-of-scope, open questions; ready for engineering and design review.

Tier: **solo**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Problem framed in user terms with evidence.
- One primary metric with target band.
- Explicit non-goals list.
- Acceptance criteria per scope item.

## Steps

### 1. Problem

Frame the problem in user terms, not solution terms.

Tasks:
- Write a one-paragraph problem statement.
- Name the user segment that owns the pain.
- Cite at least 2 evidence sources (interview, ticket, data).

Outputs:
- Problem section.

Decision gate: Advance when the problem is user-framed and evidenced.

### 2. Success metric

Lock the metric the feature must move.

Tasks:
- Pick one primary metric tied to the problem.
- Define the target band and read window.
- Identify a guardrail metric.

Outputs:
- Success-metric section.

Decision gate: Advance when the metric is one number with a target band.

### 3. Scope cuts

Define what is in and out explicitly.

Tasks:
- List the must-have user flows.
- List the explicit non-goals.
- Cut to the smallest scope that moves the metric.

Outputs:
- Scope + non-goals sections.

Decision gate: Advance when the non-goals list is non-empty and concrete.

### 4. Open questions

Surface the unknowns before review, not during.

Tasks:
- List engineering unknowns.
- List design unknowns.
- Assign an owner to each open question.

Outputs:
- Open-questions section.

Decision gate: Advance when each open question has an owner and a check-back date.

### 5. Acceptance + handoff

Make the spec engineering-ready.

Tasks:
- Write acceptance criteria per scope item.
- Walk the spec with engineering + design.
- Update based on feedback in one revision pass.

Outputs:
- Accepted spec (RFC-lite).

Decision gate: Required: a written 'accepted' note from at least one engineer and one designer.

## Decision points

- Full PRD vs RFC-lite — RFC-lite under 2 pages; full PRD only for cross-team flagship features.
- Spec now vs more discovery — if the open-questions list dominates, send the spec back to discovery first.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/stakeholder-management`
- `pro/research/researcher/opportunity-solution-trees`
- `solo/product/product-manager/mvp-scoping`
- `solo/product/product-manager/product-discovery`
- `solo/product/product-manager/product-launch`
- `solo/product/product-manager/spec-writing`
- `solo/product/product-manager/user-story-mapping`
- `solo/research/researcher/success-metrics-definition`
