# $0 to $4K MRR bootstrap journey

**Playbook slug:** `bootstrap-to-4k-mrr`  
**Tier:** pro  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

Shipped MVP at $0 MRR → ramen-profitable $4K MRR / quit-day-job threshold without VC.

## Scope

Solo dev with shipped MVP grinds to ramen-profitable ($4K MRR / quit-day-job threshold) without VC. Combines a single-channel distribution flywheel, retention defense, and runway accounting until either MRR target hit or honest sunset. Exit artifact is a quit-day-job decision contract or written sunset note.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-channel paid acquisition — single-channel bet only
- Hiring or outsourcing — solo operator throughout

### Prerequisites

- MVP live and processing real payments
- At least 5 paying customers (Stage 6 of idea-to-validated-mvp complete)

## Success criteria

The playbook is done when:
- Single-channel acquisition bet chosen and documented
- Activation rate >40% on signup-to-paid funnel
- Net revenue churn <3% monthly
- MRR dashboard live and reviewed weekly
- $4K MRR reached OR documented sunset decision

## Stages

### Stage 1: Pick channel

**Intent:** Choose one acquisition channel and commit for 90 days.

**Tasks:**
- Score 5 candidate channels
- Pick one and write 90-day commitment
- Define minimum viable cadence

**Methodologies in chain:**
- `growth-content-marketing` → `marketing/growth-content-marketing`
- `growth-cold-outreach` → `marketing/growth-cold-outreach`
- `search-everywhere-optimization` → `marketing/search-everywhere-optimization`

**Outputs:**
- Channel bet doc
- 90-day cadence calendar

**Decision gate:**
> Advance once channel is chosen. Refuse to advance with 'I'll try a few' — single bet only.

### Stage 2: Activate

**Intent:** Fix the signup-to-paid funnel before pouring traffic in.

**Tasks:**
- Map current activation drop-offs
- Ship onboarding email sequence
- Add in-app activation nudges

**Methodologies in chain:**
- `onboarding-flows` → `marketing/onboarding-flows`
- `activation-framework` → `marketing/activation-framework`
- `growth-onboarding-emails` → `marketing/growth-onboarding-emails`

**Outputs:**
- Activation funnel doc
- Onboarding email sequence live

**Decision gate:**
> Advance when activation rate >40%. Stay if leaking.

### Stage 3: Retain

**Intent:** Defend revenue: churn prevention before growth.

**Tasks:**
- Identify top 3 churn reasons
- Ship 1 retention lever per reason
- Set churn alert thresholds

**Methodologies in chain:**
- `ops-churn-prevention` → `marketing/ops-churn-prevention`
- `retention-strategies` → `marketing/retention-strategies`
- `ops-metrics-basics` → `marketing/ops-metrics-basics`

**Outputs:**
- Churn cause doc
- 3 retention levers shipped

**Decision gate:**
> Advance when monthly net revenue churn <3%. Stay if revenue leaking faster than acquisition fills.

### Stage 4: Scale channel

**Intent:** Compound the chosen channel: loops, referrals, content velocity.

**Tasks:**
- Build 1 growth loop on the chosen channel
- Add referral incentive
- Double content cadence

**Methodologies in chain:**
- `growth-loops` → `marketing/growth-loops`
- `growth-referral-programs` → `marketing/growth-referral-programs`
- `growth-newsletter-growth` → `marketing/growth-newsletter-growth`

**Outputs:**
- Growth loop live
- Referral mechanic

**Decision gate:**
> Advance when MoM growth >15% for 2 consecutive months.

### Stage 5: Price

**Intent:** Optimise pricing for revenue-per-customer not signups.

**Tasks:**
- Audit current pricing tiers
- Run 1 price experiment
- Decide on subscription model

**Methodologies in chain:**
- `ops-pricing-strategy` → `marketing/ops-pricing-strategy`
- `ops-subscription-models` → `marketing/ops-subscription-models`
- `pricing-research-market-research` → `research/pricing-research-market-research`

**Outputs:**
- Pricing decision doc
- 1 experiment result

**Decision gate:**
> Advance if price experiment improves revenue/customer ≥10% OR is conclusively rejected.

### Stage 6: Operate

**Intent:** Customer support + financial planning to sustain solo cadence.

**Tasks:**
- Set support SLA
- Build runway calculation
- Set MRR dashboard alerts

**Methodologies in chain:**
- `ops-customer-support` → `marketing/ops-customer-support`
- `ops-financial-planning` → `marketing/ops-financial-planning`
- `portfolio-strategy-product-planning` → `pm/portfolio-strategy-product-planning`

**Outputs:**
- Support SLA doc
- Runway calculation
- MRR dashboard

**Decision gate:**
> Advance when ops cadence is sustainable (no operator burnout).

### Stage 7: Decide

**Intent:** $4K MRR hit OR honest sunset.

**Tasks:**
- Compile MRR trajectory + runway
- Write quit-day-job contract or sunset note

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- Decision doc

**Decision gate:**
> Required output: written decision. $4K reached = quit-day-job. Plateau = sunset or pivot.

## Common pitfalls

- Spreading across 4 channels because none works after a month — usually means 90 days hadn't passed
- Treating $4K as quitting moment without runway buffer — keep 6 months runway in the contract

## Quality checklist (self-review)

- Did I actually commit to ONE channel, or did I just write that I would?
- Is the MRR dashboard checked weekly, or only when I feel anxious?

## Related playbooks

- `solo-idea-to-validated-mvp`
- `pmf-hunt-post-mvp`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-mrr-dashboard-template** (tier `solo`, blocks stage 6) — Operate stage needs ready-to-use MRR dashboard template
- **quit-day-job-trigger-contract** (tier `solo`, blocks stage 7) — Decide stage needs written contract for the threshold decision
- **single-channel-bet-selector** (tier `solo`, blocks stage 1) — Pick-channel stage needs decision rubric to enforce single-channel commitment

## CLI usage

```
faion get-content bootstrap-to-4k-mrr --format md       # human-readable rendering
faion get-content bootstrap-to-4k-mrr --format context  # agent-optimised context bundle
faion get-content bootstrap-to-4k-mrr --format json     # raw structured form
```
