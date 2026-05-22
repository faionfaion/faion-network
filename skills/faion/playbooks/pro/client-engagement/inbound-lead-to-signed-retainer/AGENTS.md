---
slug: inbound-lead-to-signed-retainer
tier: pro
group: client-engagement
persona: P5
goal: acquire-grow
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Cold inbound enquiry to signed Statement-of-Work + deposit invoiced OR graceful decline that protects the agency's positioning."
content_id: 56924e734a03f0f4
methodology_refs:
  - stakeholder-analysis
  - funnel-tactics-advanced
  - conversion-tracking
  - elicitation-techniques
  - strategy-analysis-current-state
  - strategy-analysis-business-need
  - strategy-analysis-future-state
  - strategy-analysis-change-strategy
  - solution-assessment
  - growth-gtm-strategy
  - ops-upselling-cross-selling
  - ops-legal-basics
  - ops-legal-compliance-checklist
  - ops-tax-basics
  - ops-financial-basics
  - ops-customer-success-basics
---

# Inbound lead to signed retainer (4-6 weeks)

**Playbook slug:** `inbound-lead-to-signed-retainer`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

Cold inbound enquiry to signed Statement-of-Work + deposit invoiced OR graceful decline that protects the agency's positioning.

## Scope

A cold inbound enquiry leaves the funnel either as a signed Statement-of-Work with deposit invoiced, or as a graceful 'not a fit' note that protects the agency's positioning. Bad-fit leads are filtered before they consume founder time. Exit artifact is either an executed SOW + deposit confirmation, or a logged decline with a written reason and referral note.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Outbound prospecting cycles - separate playbook
- Long-form RFP responses for enterprise procurement - out of scope

### Prerequisites

- Public site or landing page with a contact form
- A base proposal/SOW template + deposit-collection workflow

## Success criteria

The playbook is done when:
- Lead intake form responded to within 24h with qualification verdict
- Qualified leads booked into a 45-min discovery call
- Sent proposal + SOW within 48h of discovery
- Signed SOW with deposit cleared OR documented decline
- Pipeline log updated with stage + reason

## Stages

### Stage 1: Triage

**Intent:** Filter inbound noise: rank each enquiry by fit signal in under 10 min.

**Tasks:**
- Read enquiry against ICP one-pager
- Score budget, urgency, niche-fit
- Reply within 24h with verdict (book / decline / clarify)

**Methodologies in chain:**
- `stakeholder-analysis` -> `pro/ba/business-analyst/stakeholder-analysis`
- `funnel-tactics-advanced` -> `pro/marketing/conversion-optimizer/funnel-tactics-advanced`
- `conversion-tracking` -> `pro/marketing/growth-marketer/conversion-tracking`

**Outputs:**
- Triage verdict in pipeline log
- First-touch reply sent

**Decision gate:**
> Advance to Discovery if budget + niche fit clear. Decline if either fails.

### Stage 2: Discovery

**Intent:** Run a 45-min structured call: pain map, decision criteria, budget signal.

**Tasks:**
- Send 3-question pre-call form
- Run 45-min call with elicitation script
- Capture decision-maker + signoff path

**Methodologies in chain:**
- `elicitation-techniques` -> `pro/ba/business-analyst/elicitation-techniques`
- `strategy-analysis-current-state` -> `pro/ba/business-analyst/strategy-analysis-current-state`
- `strategy-analysis-business-need` -> `pro/ba/business-analyst/strategy-analysis-business-need`

**Outputs:**
- Discovery call notes
- Pain + budget summary

**Decision gate:**
> Advance to Scope if budget is at or above minimum engagement and stakeholders identified.

### Stage 3: Scope + price

**Intent:** Define future state, change strategy, outcome-based price.

**Tasks:**
- Map current to future state delta
- Pick fixed-price or retainer pricing model
- Draft scope with 3 explicit non-goals

**Methodologies in chain:**
- `strategy-analysis-future-state` -> `pro/ba/business-analyst/strategy-analysis-future-state`
- `strategy-analysis-change-strategy` -> `pro/ba/business-analyst/strategy-analysis-change-strategy`
- `solution-assessment` -> `pro/ba/business-analyst/solution-assessment`
- `growth-gtm-strategy` -> `pro/marketing/gtm-strategist/growth-gtm-strategy`

**Outputs:**
- Scope draft
- Price + payment terms

**Decision gate:**
> Advance if scope fits one page and price defensible against outcome.

### Stage 4: Propose + sign

**Intent:** Send proposal, handle objections, collect deposit.

**Tasks:**
- Send proposal + SOW within 48h of discovery
- Handle objections in single follow-up call
- Collect deposit before kickoff

**Methodologies in chain:**
- `ops-upselling-cross-selling` -> `pro/marketing/gtm-strategist/ops-upselling-cross-selling`
- `ops-legal-basics` -> `pro/marketing/gtm-strategist/ops-legal-basics`
- `ops-legal-compliance-checklist` -> `pro/marketing/gtm-strategist/ops-legal-compliance-checklist`
- `ops-tax-basics` -> `pro/marketing/gtm-strategist/ops-tax-basics`
- `ops-financial-basics` -> `pro/marketing/gtm-strategist/ops-financial-basics`

**Outputs:**
- Signed SOW
- Deposit cleared invoice

**Decision gate:**
> Done when SOW signed and deposit cleared. Decline gracefully if stalled beyond 14 days.

### Stage 5: Decline or refer

**Intent:** Graceful no preserves brand + opens referral loop.

**Tasks:**
- Send templated decline within 24h of verdict
- Offer 1 alternative referral if appropriate
- Log decline reason for ICP refinement

**Methodologies in chain:**
- `ops-customer-success-basics` -> `pro/marketing/gtm-strategist/ops-customer-success-basics`

**Outputs:**
- Decline sent
- Referral logged
- ICP refinement note

**Decision gate:**
> Required output: every declined lead receives a written decline. No ghosting.

## Common pitfalls

- Replying to bad-fit leads to 'just see' - burns 4h before declining
- Pricing in time-and-materials when the buyer wants an outcome - invites scope creep
- Skipping the deposit step to 'get started fast' - guarantees collection problems later

## Quality checklist (self-review)

- Did I qualify against ICP before booking the call?
- Is the proposal anchored to outcome, not hours?
- Did I get the deposit before any delivery work began?

## Related playbooks

- `discovery-call-run-45-min`
- `proposal-customization-from-base-template`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **agency-proposal-template-system** (tier `pro`, blocks stage 3) -- Scope+price stage needs a versioned proposal template with outcome-based options
- **agency-discovery-call-playbook** (tier `pro`, blocks stage 2) -- Discovery stage needs explicit 45-min run-of-show script
- **agency-decline-templates** (tier `pro`, blocks stage 5) -- Decline stage needs reusable language pack across niches
- **outcome-based-pricing-calculator** (tier `pro`, blocks stage 3) -- Scope+price stage needs a working calculator for outcome-based pricing

## CLI usage

```
faion get-content inbound-lead-to-signed-retainer --format md       # human-readable rendering
faion get-content inbound-lead-to-signed-retainer --format context  # agent-optimised context bundle
faion get-content inbound-lead-to-signed-retainer --format json     # raw structured form
```
