---
slug: productized-service-launch
tier: pro
group: client-engagement
persona: P3
goal: build-ship
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Convert one repeated client problem into a fixed-price, fixed-scope offer with a landing page, a booking flow, and 3 paid pilots — moving the freelancer from per-hour to per-outcome billing.
content_id: d89a28a7f24d9cb2
methodology_refs:
  - business-process-analysis
  - competitive-positioning
  - minimum-product-frameworks
  - mvp-scoping
  - productized-service-canvas
  - funnel-tactics-basics
  - ops-financial-basics
  - plausible-analytics
  - frontend-design
  - growth-copywriting-fundamentals
  - growth-landing-page-design
  - ops-pricing-strategy
  - ops-subscription-models
  - freelance-pilot-pricing
  - product-analytics
  - release-planning
  - ops-automation-workflow
  - ops-dashboard-setup
  - delivery-system-templates
  - growth-gtm-strategy
  - growth-linkedin-strategy
  - feedback-management
  - growth-email-marketing
  - growth-cold-outreach
  - growth-indiehackers-strategy
  - from-hourly-to-fixed-transition
---

# Productized service launch (4-week sprint)

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Convert one repeated client problem into a fixed-price, fixed-scope offer with a landing page, a booking flow, and 3 paid pilots — moving the freelancer from per-hour to per-outcome billing.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Pick the pattern

**Intent:** Identify one repeated engagement worth productizing.

**Tasks**
- Review last 12 months of invoices for repeated work
- Score candidates by repeat frequency + margin
- Pick one; write a 1-page service brief

**Outputs**
- Candidate list with scoring
- Service brief

**Decision gate**

Advance when one candidate scores 2x above others on repeat + margin. Otherwise iterate.

### Stage 2 — Price + landing

**Intent:** Fixed price + landing page + booking flow live.

**Tasks**
- Define 3-tier fixed-price offer
- Build landing page with checkout/booking
- Set up analytics + email capture

**Outputs**
- Landing page live
- Booking flow
- Pricing rationale doc

**Decision gate**

Advance once landing is live and ≥3 prospects could complete booking end-to-end.

### Stage 3 — Pilot run

**Intent:** 3 paid pilots prove the offer ships in fixed scope without scope creep.

**Tasks**
- Sell 3 pilots to existing-network prospects
- Deliver against SOP; log time vs estimate
- Harvest testimonials + before/after metrics

**Outputs**
- 3 paid pilots delivered
- Time-vs-estimate log
- 3 testimonials

**Decision gate**

Advance when ≥2/3 pilots ship within estimated time. If all over, fix SOP before scaling.

### Stage 4 — Promote + transition

**Intent:** Make the productized offer the default sale; transition hourly clients.

**Tasks**
- Publish 3 case studies
- Announce to LinkedIn + newsletter
- Stop quoting hourly for this work; defer requests to the offer

**Outputs**
- 3 case studies live
- Launch announcement
- Hourly-stop policy

**Decision gate**

Productized offer must become default within 6 weeks of launch. If hourly still dominant, audit pricing.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `productized-service-canvas` (stage 1) — Stage 1 (Pick the pattern) references this; no methodology exists yet.
- `freelance-pilot-pricing` (stage 2) — Stage 2 (Price + landing) references this; no methodology exists yet.
- `delivery-system-templates` (stage 3) — Stage 3 (Pilot run) references this; no methodology exists yet.
- `from-hourly-to-fixed-transition` (stage 4) — Stage 4 (Promote + transition) references this; no methodology exists yet.
- `minimum-product-frameworks` (stage 1) — Stage 1 (Pick the pattern) cites pro/product/product-planning/minimum-product-frameworks but path does not resolve under KNOWLEDGE_ROOT.
- `mvp-scoping` (stage 1) — Stage 1 (Pick the pattern) cites pro/product/product-planning/mvp-scoping but path does not resolve under KNOWLEDGE_ROOT.
- `plausible-analytics` (stage 2) — Stage 2 (Price + landing) cites solo/dev/automation-tooling/plausible-analytics but path does not resolve under KNOWLEDGE_ROOT.
- `ops-pricing-strategy` (stage 2) — Stage 2 (Price + landing) cites solo/marketing/growth-marketer/ops-pricing-strategy but path does not resolve under KNOWLEDGE_ROOT.
- `ops-subscription-models` (stage 2) — Stage 2 (Price + landing) cites solo/marketing/growth-marketer/ops-subscription-models but path does not resolve under KNOWLEDGE_ROOT.
- `release-planning` (stage 3) — Stage 3 (Pilot run) cites pro/product/product-planning/release-planning but path does not resolve under KNOWLEDGE_ROOT.
- `ops-automation-workflow` (stage 3) — Stage 3 (Pilot run) cites solo/dev/automation-tooling/ops-automation-workflow but path does not resolve under KNOWLEDGE_ROOT.
- `ops-dashboard-setup` (stage 3) — Stage 3 (Pilot run) cites solo/dev/automation-tooling/ops-dashboard-setup but path does not resolve under KNOWLEDGE_ROOT.
- `growth-linkedin-strategy` (stage 4) — Stage 4 (Promote + transition) cites pro/marketing/smm-manager/growth-linkedin-strategy but path does not resolve under KNOWLEDGE_ROOT.
- `growth-cold-outreach` (stage 4) — Stage 4 (Promote + transition) cites solo/marketing/growth-marketer/growth-cold-outreach but path does not resolve under KNOWLEDGE_ROOT.
- `growth-indiehackers-strategy` (stage 4) — Stage 4 (Promote + transition) cites solo/marketing/growth-marketer/growth-indiehackers-strategy but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a deep-complexity global-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

## Anti-patterns to avoid

- Running the stages out of order because one feels more urgent. Order encodes risk: skipping earlier stages usually means absorbing risk in a later stage where the cost is higher.
- Treating outputs as optional. Every stage requires a written artifact — that artifact is what makes the next decision-gate verifiable.
- Letting the client write your scope, your timeline, or your contract clauses. The whole point of this playbook is that *you* run a deterministic pipeline; the client engages with the pipeline, not the other way around.
- Skipping the closure / retro step. The compounding value of running this playbook many times is in the lessons captured at the end. Without retros, you re-learn the same expensive lessons every quarter.

## Agent prompt hints

If you are routing this playbook through `faion get-content` for an agent:

- Ask the agent to produce *each* stage's outputs as named files before moving to the next stage. Reject hand-wave outputs.
- Have the agent state the decision-gate condition out loud after producing outputs, and pass the gate before continuing.
- For any gap in the methodology chain (see *Gaps in the methodology chain* above), the agent should explicitly mark its substitute approach so you can backfill the missing methodology later.
