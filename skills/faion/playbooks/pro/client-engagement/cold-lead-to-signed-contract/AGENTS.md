---
slug: cold-lead-to-signed-contract
tier: pro
group: client-engagement
persona: P3
goal: acquire-grow
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: From first outbound touch on Upwork/LinkedIn to a counter-signed SOW with deposit landing in escrow; pipeline of 3-5 qualified leads in parallel, one close per cycle.
content_id: 47a6e4a62b456809
methodology_refs:
  - growth-brand-positioning
  - growth-gtm-strategy
  - competitive-positioning
  - growth-linkedin-strategy
  - freelancer-niche-positioning
  - upwork-search-targeting
  - growth-cold-outreach
  - growth-copywriting-fundamentals
  - ops-pricing-strategy
  - elicitation-techniques
  - requirements-prioritization
  - active-listening
  - mom-test
  - difficult-conversations
  - stakeholder-communication
  - acceptance-criteria
  - ops-legal-basics
  - ops-legal-compliance-checklist
  - negotiation
  - freelance-proposal-template
  - freelance-msa-sow-templates
---

# Cold lead to signed contract (3-week acquisition flow)

**Persona:** P3 Technical Freelancer · **Tier:** pro · **Complexity:** medium · **Angle:** global

## Why this playbook exists

From first outbound touch on Upwork/LinkedIn to a counter-signed SOW with deposit landing in escrow; pipeline of 3-5 qualified leads in parallel, one close per cycle.

Most technical freelancers improvise this flow. That works at low volume and breaks at scale. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, no silent absorption of work, no vague pricing.

## How to run it

Run the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced.

## Stage map

### Stage 1 — Target & list

**Intent:** Build a 30-prospect list with niche fit signals before sending anything.

**Tasks**
- Re-state niche positioning in one sentence
- Generate 30 prospects via Upwork search and LinkedIn
- Score each prospect on fit, budget signal, decision-maker access

**Outputs**
- Prospect list (30 rows) in CRM
- Niche positioning one-pager

**Decision gate**

Advance once 30 named prospects are scored. Refuse to send if list <20.

### Stage 2 — Outreach

**Intent:** First-touch + follow-up cadence that gets ≥10% reply rate without burning the niche.

**Tasks**
- Draft first-touch message variant (3 angles, 1 picked)
- Send across 5 days in batches of 6 per day
- Track replies; A/B test subject line midway

**Outputs**
- First-touch message library
- Outreach log with reply tracking

**Decision gate**

Advance once ≥3 replies indicate willingness to schedule a call. Re-tune copy if reply rate <5%.

### Stage 3 — Discovery + qualify

**Intent:** 30-min calls converting replies into qualified-yes or polite-no.

**Tasks**
- Prepare hypothesis-led call agenda per prospect
- Run discovery using Mom Test framing
- Score fit; send 24h follow-up email with explicit next step

**Outputs**
- Call notes per prospect
- Fit score column populated

**Decision gate**

Advance only the prospects scoring ≥7/10 on fit + budget. Polite-decline the rest.

### Stage 4 — Proposal + close

**Intent:** Send a 1-3 page proposal, negotiate redlines, get countersigned SOW + deposit.

**Tasks**
- Draft proposal with 3 pricing options
- Send proposal within 48h of discovery
- Negotiate redlines; close with deposit clause

**Outputs**
- Signed SOW
- Deposit invoice paid
- Project kickoff scheduled

**Decision gate**

Required artifact: countersigned SOW + deposit landed. Without deposit, no work begins.

## Common pitfalls

- Treating decision_gate as a suggestion — playbook collapses to a checklist if gates are not enforced
- Skipping written artifacts because 'it's in my head' — kills traceability and future re-use

## Quality self-review

- Did every stage produce a written artifact a stranger could read?
- Did I actually advance only when the decision_gate criterion was met?

## Gaps in the methodology chain

This playbook is **draft** because the methodology chain references slugs that are not yet authored:

- `freelancer-niche-positioning` (stage 1) — Stage 1 (Target & list) references this; no methodology exists yet.
- `upwork-search-targeting` (stage 1) — Stage 1 (Target & list) references this; no methodology exists yet.
- `freelance-proposal-template` (stage 4) — Stage 4 (Proposal + close) references this; no methodology exists yet.
- `freelance-msa-sow-templates` (stage 4) — Stage 4 (Proposal + close) references this; no methodology exists yet.
- `growth-linkedin-strategy` (stage 1) — Stage 1 (Target & list) cites pro/marketing/smm-manager/growth-linkedin-strategy but path does not resolve under KNOWLEDGE_ROOT.
- `growth-cold-outreach` (stage 2) — Stage 2 (Outreach) cites solo/marketing/growth-marketer/growth-cold-outreach but path does not resolve under KNOWLEDGE_ROOT.
- `ops-pricing-strategy` (stage 2) — Stage 2 (Outreach) cites solo/marketing/growth-marketer/ops-pricing-strategy but path does not resolve under KNOWLEDGE_ROOT.

BLOCK policy: this playbook cannot move to `published` until `gaps[]` is empty.

## How this connects to the wider Faion catalog

The methodology chain links into `solo/comms/communicator`, `solo/marketing/*`, `pro/ba/business-analyst`, `pro/pm/project-manager`, `pro/marketing/*`, `pro/product/*`. Run `faion get-content <slug> --format context` to pull the full set into an agent-readable payload.

## When to use this playbook

This is a medium-complexity global-angle playbook for the P3 Technical Freelancer persona — solo contractors who deliver client work for revenue, run a small portfolio of accounts, and need repeatable rituals more than novel theory. Use it when the situation matches the *Why this playbook exists* statement. Do not use it for full-time-employee workflows or large-team delivery — those have different decision gates.

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
