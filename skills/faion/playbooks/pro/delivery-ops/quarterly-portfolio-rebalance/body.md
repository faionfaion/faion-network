# Quarterly portfolio rebalance (cash, clients, capacity)

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Why this playbook exists

End of every quarter: drop the worst client, raise rates on the rest, fill the freed slot with a higher-rate engagement, and lock the next quarter's revenue target and capacity allocation.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Audit current portfolio

**Intent:** Score every active client on rate, stress, growth, strategic value.

**Tasks**
- Pull client roster + last-quarter $/hour realized
- Score each on 4 axes
- Flag bottom-quartile clients

**Outputs**
- Client scorecard
- Bottom-quartile flag list

**Decision gate**

Advance only with a written ranked list. No subjective vibes.

### Stage 2 — Drop & raise

**Intent:** Drop the worst client; raise rates on the rest.

**Tasks**
- Write a graceful end-of-engagement note to bottom client
- Draft personalised rate-rise notes to the rest
- Schedule the conversations within one week

**Outputs**
- Drop letter sent
- Rate-rise notes drafted
- Calendar invites set

**Decision gate**

Required: at least one client dropped + one rate-rise sent. No exceptions.

### Stage 3 — Fill capacity

**Intent:** Refill the freed slot at a higher rate.

**Tasks**
- Reactivate dormant warm leads
- Publish a 'capacity opens X date' post
- Run targeted outreach to upper-band prospects

**Outputs**
- Reactivation outreach sent
- Public capacity announcement
- 1+ new engagement booked

**Decision gate**

Advance once freed capacity is booked at ≥ new-rate-floor. Stay if booking at old rate.

### Stage 4 — Lock next quarter

**Intent:** Set explicit revenue target + capacity allocation for next 90 days.

**Tasks**
- Write Q+1 revenue target with realistic floor + stretch
- Allocate weekly hours across delivery / sales / growth / rest
- Set check-in dates

**Outputs**
- Q+1 plan doc
- Capacity allocation table

**Decision gate**

Quarter closes only when plan is written. Verbal intent doesn't count.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-client-scorecard` (stage 1) — Stage 1 (Audit current portfolio) references this; no methodology exists yet.
- `rate-increase-notice-template` (stage 2) — Stage 2 (Drop & raise) references this; no methodology exists yet.
- `dormant-lead-reactivation` (stage 3) — Stage 3 (Fill capacity) references this; no methodology exists yet.
- `freelance-capacity-model` (stage 4) — Stage 4 (Lock next quarter) references this; no methodology exists yet.
- `ops-pricing-strategy` (stage 2) — Stage 2 (Drop & raise) cites solo/marketing/growth-marketer/ops-pricing-strategy but path does not resolve under KNOWLEDGE_ROOT.
- `growth-cold-outreach` (stage 3) — Stage 3 (Fill capacity) cites solo/marketing/growth-marketer/growth-cold-outreach but path does not resolve under KNOWLEDGE_ROOT.
- `okr-setting` (stage 4) — Stage 4 (Lock next quarter) cites pro/product/product-planning/okr-setting but path does not resolve under KNOWLEDGE_ROOT.
- `ops-financial-planning` (stage 4) — Stage 4 (Lock next quarter) cites solo/marketing/growth-marketer/ops-financial-planning but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.
