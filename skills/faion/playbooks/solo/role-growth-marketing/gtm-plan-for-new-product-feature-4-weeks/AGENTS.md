---
slug: gtm-plan-for-new-product-feature-4-weeks
tier: solo
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "From feature-freeze to multi-channel launch: positioning, target ICP segments, launch assets, channel mix, success metrics, and post-launch iteration loop. 'Done' = feature is live, all assigned ch..."
content_id: 4dec15b4085692b5
methodology_refs:
  - aarrr-pirate-metrics
  - conversion-tracking
  - google-analytics
  - north-star-metric
  - growth-brand-positioning
  - ads-attribution-models
  - growth-landing-page-design
  - ads-meta-campaign-setup
  - ops-dashboard-setup
  - ads-retargeting
  - plausible-analytics
  - growth-content-marketing
  - growth-hacker-news-launch
  - growth-copywriting-fundamentals
  - growth-indiehackers-strategy
  - growth-gtm-strategy
  - growth-email-marketing
  - growth-product-hunt-launch
  - growth-influencer-marketing
  - growth-reddit-marketing
  - growth-social-media-strategy
---

# GTM Plan for New Product Feature (4 weeks)

A 7-stage playbook for the global angle. Tier: **solo**. Complexity: **medium**.

## Context

From feature-freeze to multi-channel launch: positioning, target ICP segments, launch assets, channel mix, success metrics, and post-launch iteration loop. 'Done' = feature is live, all assigned channels have shipped launch content, baseline metrics (signups, activation, paid-vs-organic split) are flowing into a dashboard, and a week-2 retro has fed three optimizations back into the plan.

## Outcome

A complete delivery cycle from frame to decision: artifacts shipped, metrics flowing, a written continue/pivot/kill verdict that next quarter's planning can act on.

## Steps

### 1. Frame

Lock the goal, owner, success metric, and time-box.

Tasks:
- Draft a one-paragraph charter with goal, owner, success metric, time-box
- List explicit non-goals so scope cannot creep
- Identify stakeholders and their decision rights

Methodologies:
- `pro/marketing/growth-marketer/aarrr-pirate-metrics`
- `pro/marketing/ppc-manager/ads-attribution-models`
- `solo/marketing/conversion-optimizer/growth-landing-page-design`

Outputs:
- Charter doc (1 page)

Decision gate: Advance only with a written charter that all stakeholders read and signed off.

### 2. Research

Gather the inputs needed to plan: data, prior work, competitors, constraints.

Tasks:
- Pull the relevant data extract / dashboards / prior decks
- Scan competitors and prior internal attempts
- Document constraints (legal, tech, brand) up front

Methodologies:
- `pro/marketing/growth-marketer/conversion-tracking`
- `pro/marketing/ppc-manager/ads-meta-campaign-setup`
- `solo/marketing/growth-marketer/ops-dashboard-setup`

Outputs:
- Research brief with sources

Decision gate: Advance once research surfaces no blocker; otherwise loop with stakeholders.

### 3. Plan

Convert the charter + research into a sequenced plan with owners.

Tasks:
- Break the work into 3-7 phases with explicit exit-criteria
- Assign an owner per phase
- Wire metrics + dashboards before execution starts

Methodologies:
- `pro/marketing/growth-marketer/google-analytics`
- `pro/marketing/ppc-manager/ads-retargeting`
- `solo/marketing/growth-marketer/plausible-analytics`

Outputs:
- Plan doc with Gantt or phase table

Decision gate: Advance only when each phase has a named owner and exit-criterion.

### 4. Produce

Create the core artifacts: assets, content, code, campaigns, configs.

Tasks:
- Build the core deliverables per phase plan
- Hold a draft review with the named owner before publish
- Track WIP visibly so blockers surface fast

Methodologies:
- `pro/marketing/growth-marketer/north-star-metric`
- `solo/marketing/content-marketer/growth-content-marketing`
- `solo/marketing/gtm-strategist/growth-hacker-news-launch`

Outputs:
- Drafts of all core artifacts

Decision gate: Advance when drafts pass internal review against the charter, not personal taste.

### 5. Ship

Push live: deploy, publish, launch the campaign, flip the switch.

Tasks:
- Run the launch checklist (dependencies, tracking, comms)
- Publish on schedule; do not pre-leak
- Confirm tracking is flowing in real-time on a dashboard

Methodologies:
- `pro/marketing/gtm-strategist/growth-brand-positioning`
- `solo/marketing/content-marketer/growth-copywriting-fundamentals`
- `solo/marketing/gtm-strategist/growth-indiehackers-strategy`

Outputs:
- Launch evidence (URLs / receipts)

Decision gate: Advance only with tracking visibly flowing; otherwise hold launch.

### 6. Measure

Read the metrics against the plan; separate noise from signal.

Tasks:
- Compare actuals vs charter success metric
- Split cohort/segment/channel to find what drove the result
- Document confounders before drawing conclusions

Methodologies:
- `pro/marketing/gtm-strategist/growth-gtm-strategy`
- `solo/marketing/content-marketer/growth-email-marketing`
- `solo/marketing/gtm-strategist/growth-product-hunt-launch`

Outputs:
- Measurement readout (1 page)

Decision gate: Advance when readout passes a peer sniff-test against confounders.

### 7. Iterate-or-close

Decide: continue, kill, or hand off to BAU.

Tasks:
- Hold the retro on what shipped vs what was planned
- Decide continue / pivot / kill / hand-off in writing
- If continue: define next 30-day milestone with metrics

Methodologies:
- `pro/marketing/gtm-strategist/growth-influencer-marketing`
- `solo/marketing/content-marketer/growth-reddit-marketing`
- `solo/marketing/smm-manager/growth-social-media-strategy`

Outputs:
- Decision doc with next steps

Decision gate: Required output: a written decision; no "let's see".

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/pro/marketing/growth-marketer/aarrr-pirate-metrics`
- `knowledge/pro/marketing/growth-marketer/conversion-tracking`
- `knowledge/pro/marketing/growth-marketer/google-analytics`
- `knowledge/pro/marketing/growth-marketer/north-star-metric`
- `knowledge/pro/marketing/gtm-strategist/growth-brand-positioning`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
