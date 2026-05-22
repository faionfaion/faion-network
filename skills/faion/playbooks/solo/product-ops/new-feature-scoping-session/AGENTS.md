---
slug: new-feature-scoping-session
tier: solo
group: product-ops
persona: P1
goal: plan-design
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Raw feature request → ready-to-ship slice with validated signal + spec + flag plan + success metric.
content_id: 59488785994ccb04
methodology_refs:
  - mom-test
  - continuous-discovery
  - market-researcher
  - feature-prioritization-rice
  - mvp-scoping
  - micro-mvps
  - minimum-product-frameworks
  - spec-writing
  - spec-structure
  - writing-specifications
  - feature-flags-rollout-targeting
  - feature-flags
---

# New feature scoping session (per-feature, on demand)

**Playbook slug:** `new-feature-scoping-session`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Raw feature request → ready-to-ship slice with validated signal + spec + flag plan + success metric.

## Scope

Per-feature on-demand session: signal validated, MVP cut to bone, spec written, flag plan decided, success metric defined — all before any code is generated. Exit artifact is build-ready spec.md with rollout + success criteria.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Full discovery — that's done upstream in continuous-discovery
- Implementation — handed off to daily SDD cycle

### Prerequisites

- Feature request exists (from inbox, dashboard, or roadmap)
- Existing backlog with priority context

## Success criteria

The playbook is done when:
- Signal validated: ≥3 customer quotes or analytics anomaly
- Micro-MVP defined: smallest slice that delivers value
- Spec written with acceptance criteria
- Feature flag rollout plan documented
- Success metric + decision date set

## Stages

### Stage 1: Validate signal

**Intent:** Is this real demand or a single loud voice?

**Tasks:**
- Find ≥3 customer quotes OR analytics signal
- Run mom-test on 2 prospects if unclear
- Decide build/waitlist/kill

**Methodologies in chain:**
- `mom-test` → `solo/comms/communicator/mom-test`
- `continuous-discovery` → `solo/product/product-manager/continuous-discovery`
- `market-researcher` → `solo/research/market-researcher`

**Outputs:**
- Signal evidence packet

**Decision gate:**
> Advance if signal is real. Park to waitlist if uncertain. Kill if only 1 loud voice.

### Stage 2: Prioritise

**Intent:** Does this beat current top-3 backlog item?

**Tasks:**
- Score with RICE
- Compare to current top-3
- Decide bump/queue

**Methodologies in chain:**
- `feature-prioritization-rice` → `solo/product/product-manager/feature-prioritization-rice`

**Outputs:**
- RICE score + priority decision

**Decision gate:**
> Advance when priority is decided. Refuse to scope below-cutoff items.

### Stage 3: Cut MVP

**Intent:** Smallest slice that delivers value.

**Tasks:**
- List all candidate sub-features
- Cut to 1-feature minimum-viable slice
- Write non-goals

**Methodologies in chain:**
- `mvp-scoping` → `solo/product/product-manager/mvp-scoping`
- `micro-mvps` → `solo/product/product-manager/micro-mvps`
- `minimum-product-frameworks` → `solo/product/product-planning/minimum-product-frameworks`

**Outputs:**
- Micro-MVP scope doc

**Decision gate:**
> Advance when scope fits 1-3 days of solo work. Cut more if not.

### Stage 4: Spec

**Intent:** Write acceptance criteria + non-goals.

**Tasks:**
- Write 1-page spec
- List acceptance criteria
- Define non-goals explicitly

**Methodologies in chain:**
- `spec-writing` → `solo/product/product-manager/spec-writing`
- `spec-structure` → `solo/sdd/sdd-planning/spec-structure`
- `writing-specifications` → `solo/sdd/sdd/writing-specifications`

**Outputs:**
- spec.md

**Decision gate:**
> Advance when criteria are atomic + checkable.

### Stage 5: Flag plan

**Intent:** Decide rollout: behind flag, % rollout, targets.

**Tasks:**
- Decide flag name + scope
- Define rollout percentages
- Set success metric + decision date

**Methodologies in chain:**
- `feature-flags-rollout-targeting` → `solo/dev/automation-tooling/feature-flags-rollout-targeting`
- `feature-flags` → `solo/dev/software-developer/feature-flags`

**Outputs:**
- Flag plan in spec

**Decision gate:**
> Required output: spec with flag + rollout + success metric. Hand off to daily cycle.

## Common pitfalls

- Skipping signal validation because the request is from a paying customer — even paying customers ask for noise
- Specifying without cutting first — produces 3x the scope

## Quality checklist (self-review)

- Could I delete 30% of the spec right now without losing the value?
- Is the success metric measurable inside 2 weeks of rollout?

## Related playbooks

- `daily-sdd-spec-code-review`
- `sunday-roadmap-ritual`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **build-or-waitlist-decision-tree** (tier `solo`, blocks stage 1) — Validate-signal stage needs decision tree for ambiguous requests
- **micro-mvp-cut-rubric** (tier `solo`, blocks stage 3) — Cut-MVP stage needs explicit rubric for cutting to bone

## CLI usage

```
faion get-content new-feature-scoping-session --format md       # human-readable rendering
faion get-content new-feature-scoping-session --format context  # agent-optimised context bundle
faion get-content new-feature-scoping-session --format json     # raw structured form
```
