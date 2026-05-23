# Product/Market Fit hunt (post-MVP, pre-traction)

**Playbook slug:** `pmf-hunt-post-mvp`  
**Tier:** pro  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

Live MVP stuck under ~$1K MRR → documented PMF signal OR triggered pivot.

## Scope

MVP is live but stuck under ~$1K MRR. Solo founder runs a structured discovery + positioning + experiment loop until either a fit signal is reached (retention curve flattens, NPS-style pull, organic referrals) or a documented pivot is triggered. Exit artifact is a PMF scorecard with evidence trail.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Scaling distribution before PMF — out of scope
- Hiring or fund-raising — single-operator playbook

### Prerequisites

- MVP live with at least 30 days of usage data
- Stripe (or equivalent) recording paid signups

## Success criteria

The playbook is done when:
- PMF scorecard filled (retention, pull, referral, NPS rows)
- 10+ recent power-user interviews logged
- Positioning statement rewritten with sharper ICP
- 1 fit experiment shipped per stage (≥3 experiments total)
- Written go/pivot decision with evidence references

## Stages

### Stage 1: Diagnose

**Intent:** Map current state: retention curves, cohort decay, paying-user concentration.

**Tasks:**
- Pull retention + cohort data from analytics
- Identify activation drop-off
- Score against PMF rubric

**Methodologies in chain:**
- `aarrr-pirate-metrics` → `pro/marketing/growth-marketer/aarrr-pirate-metrics`
- `cohort-basics` → `pro/marketing/growth-marketer/cohort-basics`
- `cohort-implementation` → `pro/marketing/growth-marketer/cohort-implementation`
- `north-star-metric` → `pro/marketing/growth-marketer/north-star-metric`
- `retention-metrics` → `pro/marketing/growth-marketer/retention-metrics`

**Outputs:**
- PMF baseline scorecard
- Cohort decay chart

**Decision gate:**
> Advance if signal is unclear (most common). Skip to Decide if PMF is unambiguous.

### Stage 2: Listen

**Intent:** 10 power-user interviews + 5 churned-user post-mortems for asymmetric signal.

**Tasks:**
- Schedule 10 power-user calls
- Run 5 churn post-mortems
- Tag interview themes

**Methodologies in chain:**
- `mom-test` → `solo/comms/communicator/mom-test`
- `continuous-discovery-habits` → `pro/product/product-planning/continuous-discovery-habits`
- `user-interviews` → `solo/research/researcher/user-interviews`
- `value-proposition-design` → `solo/research/researcher/value-proposition-design`

**Outputs:**
- 15 interview notes tagged by theme
- Top-3 pull triggers identified

**Decision gate:**
> Advance if a single dominant pull theme appears. Loop if signal is fragmented across >5 themes.

### Stage 3: Position

**Intent:** Rewrite ICP and value-prop against the dominant pull theme.

**Tasks:**
- Draft sharper ICP one-liner
- Rewrite landing-page hero against pull theme
- Diff against current copy

**Methodologies in chain:**
- `competitive-positioning` → `pro/product/product-planning/competitive-positioning`
- `competitive-intelligence` → `pro/research/market-researcher/competitive-intelligence`
- `competitor-analysis` → `pro/research/market-researcher/competitor-analysis`
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`

**Outputs:**
- New ICP + value-prop doc
- Landing-page variant

**Decision gate:**
> Advance once new copy is live. If founder cannot write the ICP in one sentence, return to Listen.

### Stage 4: Experiment

**Intent:** Run 3 fit experiments: activation, retention, acquisition.

**Tasks:**
- Pick one lever per layer (A/R/A)
- Define success metric + decision date
- Ship and measure

**Methodologies in chain:**
- `ab-testing-basics` → `pro/marketing/growth-marketer/ab-testing-basics`
- `ab-testing-setup` → `pro/marketing/growth-marketer/ab-testing-setup`
- `activation-framework` → `pro/marketing/growth-marketer/activation-framework`
- `activation-tactics` → `pro/marketing/growth-marketer/activation-tactics`

**Outputs:**
- 3 experiment results docs
- Updated PMF scorecard

**Decision gate:**
> Advance when all 3 experiments report. Re-run if any experiment lacks measurable result.

### Stage 5: Decide

**Intent:** Written go/pivot decision backed by scorecard + experiment evidence.

**Tasks:**
- Compile evidence packet
- Write decision doc
- If pivot, define new hypothesis

**Methodologies in chain:**
- `architecture-decision-records` → `solo/dev/software-architect/architecture-decision-records`
- `trade-off-decision-matrix` → `solo/dev/software-architect/trade-off-decision-matrix`

**Outputs:**
- Decision doc with PMF rubric output

**Decision gate:**
> Required output is a written decision. No 'maybe'. No 'wait and see'.

## Common pitfalls

- Treating noisy weekly numbers as PMF signal — use cohort retention instead
- Pivoting on a single loud customer voice — wait for theme convergence

## Quality checklist (self-review)

- Can I explain the pull theme in one sentence backed by 5 quotes?
- Did each experiment produce a measurable result, or did I move on early?

## Related playbooks

- `solo-idea-to-validated-mvp`
- `pivot-v1-to-v2`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **pmf-rubric-for-solos** (tier `solo`, blocks stage 1) — Diagnose stage needs explicit PMF rubric scored against solo-scale data
- **solo-pivot-decision-framework** (tier `solo`, blocks stage 5) — Decide stage needs framework for choosing pivot dimension (segment/feature/model)
- **asymmetric-churn-power-interview-protocol** (tier `solo`, blocks stage 2) — Listen stage needs a protocol that distinguishes churn vs power signals

## CLI usage

```
faion get-content pmf-hunt-post-mvp --format md       # human-readable rendering
faion get-content pmf-hunt-post-mvp --format context  # agent-optimised context bundle
faion get-content pmf-hunt-post-mvp --format json     # raw structured form
```
