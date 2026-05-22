---
slug: pivot-v1-to-v2
tier: pro
group: product-management
persona: P1
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: v1 with flat retention and stalled growth → executed pivot (segment / feature / model / sunset) with brand intact.
content_id: 6abbe9e82e826b38
methodology_refs:
  - ops-churn-basics
  - retention-metrics
  - competitive-intelligence
  - market-analysis
  - niche-evaluation
  - pain-point-research
  - jobs-to-be-done
  - spec-writing
  - writing-specifications
  - architecture-decision-records
  - trade-off-decision-matrix
  - difficult-conversations
  - stakeholder-communication
  - growth-email-marketing
  - growth-landing-page-design
  - technical-debt
  - product-launch
  - mistake-memory
  - reflexion-learning
---

# Pivot from failed v1 to v2

**Playbook slug:** `pivot-v1-to-v2`  
**Tier:** pro  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

v1 with flat retention and stalled growth → executed pivot (segment / feature / model / sunset) with brand intact.

## Scope

v1 is not working: retention flat, growth stalled, founder energy bleeding. Solo founder decides and executes a structured pivot (segment / feature / model / sunset) without burning the brand or customer trust. Exit artifact is a v2 brief or a sunset comms plan.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Marketing campaigns for v2 — covered in launch playbook
- Co-founder recruitment — solo operator throughout

### Prerequisites

- v1 live for ≥6 months with revenue data
- Honest founder audit: retention < target AND growth flat for 3+ months

## Success criteria

The playbook is done when:
- Pivot dimension chosen (segment / feature / model / sunset)
- v2 brief OR sunset comms plan written
- Existing customer cohort migrated or honestly off-boarded
- Founder energy plan: defined commitment runway for v2
- Lessons-learned doc shipped (mistake-memory updated)

## Stages

### Stage 1: Diagnose

**Intent:** Cold-eyed look at why v1 stalled.

**Tasks:**
- Pull churn + retention data
- Pull market data: competitors, segment shift
- Score against 4 pivot dimensions

**Methodologies in chain:**
- `ops-churn-basics` → `pro/marketing/growth-marketer/ops-churn-basics`
- `retention-metrics` → `pro/marketing/growth-marketer/retention-metrics`
- `competitive-intelligence` → `pro/research/market-researcher/competitive-intelligence`
- `market-analysis` → `pro/research/market-researcher/market-analysis`
- `niche-evaluation` → `solo/research/market-researcher/niche-evaluation`
- `pain-point-research` → `solo/research/researcher/pain-point-research`

**Outputs:**
- Failure diagnosis doc
- Pivot dimension scoring

**Decision gate:**
> Advance when pivot dimension is chosen. Refuse to skip diagnosis — drift back to v1 patterns otherwise.

### Stage 2: Choose

**Intent:** Pick the pivot or pick sunset. No 'partial' pivots.

**Tasks:**
- Write pivot hypothesis
- Define v2 scope cuts
- Set commitment runway (months + $)

**Methodologies in chain:**
- `jobs-to-be-done` → `solo/research/researcher/jobs-to-be-done`
- `spec-writing` → `solo/product/product-manager/spec-writing`
- `writing-specifications` → `solo/sdd/sdd/writing-specifications`
- `architecture-decision-records` → `solo/dev/software-architect/architecture-decision-records`
- `trade-off-decision-matrix` → `solo/dev/software-architect/trade-off-decision-matrix`

**Outputs:**
- Pivot decision doc
- Commitment runway contract

**Decision gate:**
> Required output: signed decision doc with runway. No 'see how it goes'.

### Stage 3: Communicate

**Intent:** Tell existing customers what's changing — honest, early, specific.

**Tasks:**
- Draft customer comms (3 versions: migrate / sunset / continue)
- Send personally to top 10 accounts
- Public announcement post

**Methodologies in chain:**
- `difficult-conversations` → `solo/comms/communicator/difficult-conversations`
- `stakeholder-communication` → `solo/comms/communicator/stakeholder-communication`
- `growth-email-marketing` → `solo/marketing/content-marketer/growth-email-marketing`
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`

**Outputs:**
- Customer comms sent
- Public announcement post

**Decision gate:**
> Advance when ≥80% of paying customers acknowledge comms. Stay if silence.

### Stage 4: Execute

**Intent:** Build v2 OR off-board v1 cleanly.

**Tasks:**
- Cut v2 scope to minimum-viable-pivot
- Ship per pivot brief
- Off-board v1 users with refund policy

**Methodologies in chain:**
- `technical-debt` → `solo/dev/software-developer/technical-debt`
- `product-launch` → `solo/product/product-manager/product-launch`

**Outputs:**
- v2 shipped on staging OR v1 sunset complete

**Decision gate:**
> Advance once v2 lives on staging OR v1 is fully off-boarded with refunds processed.

### Stage 5: Reflect

**Intent:** Lessons learned. Update memory. Don't repeat this.

**Tasks:**
- Run reflexion on v1 mistakes
- Update mistake-memory
- Write public retro post (optional)

**Methodologies in chain:**
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Outputs:**
- Mistake-memory entry
- Lessons-learned doc

**Decision gate:**
> Required output: written retro. Without it, the same mistake recurs.

## Common pitfalls

- Building v2 before deciding to pivot — accidental scope drift
- Silent sunset — ghosting customers destroys future trust

## Quality checklist (self-review)

- Did I write down WHY v1 failed in specific terms, or stay vague?
- Did existing customers hear from me personally before reading a public post?

## Related playbooks

- `pmf-hunt-post-mvp`
- `bootstrap-to-4k-mrr`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **pivot-vs-quit-decision-template** (tier `solo`, blocks stage 2) — Choose stage needs rubric to distinguish pivot from quit
- **v1-to-v2-migration-playbook** (tier `solo`, blocks stage 4) — Execute stage needs concrete migration steps for existing data + customers
- **sunset-customer-comms-template** (tier `solo`, blocks stage 3) — Communicate stage needs template for sunset variant

## CLI usage

```
faion get-content pivot-v1-to-v2 --format md       # human-readable rendering
faion get-content pivot-v1-to-v2 --format context  # agent-optimised context bundle
faion get-content pivot-v1-to-v2 --format json     # raw structured form
```
