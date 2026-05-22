---
slug: friday-metrics-mrr-pulse
tier: solo
group: solo-ops-finance
persona: P1
goal: operate-ritual
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Foggy sense of last week's KPIs → 30-minute scan + one experiment chosen for next week."
content_id: 08095f0c9067c836
methodology_refs:
  - plausible-analytics
  - ops-dashboard-setup
  - product-analytics
  - ab-testing-basics
  - ab-testing-implementation
  - growth-landing-page-design
  - ops-subscription-models
  - okr-setting
  - outcome-based-roadmaps
---

# Friday metrics check and MRR pulse

**Playbook slug:** `friday-metrics-mrr-pulse`  
**Tier:** solo  
**Complexity:** light  
**Persona:** P1 — Solo SaaS Builder

## Intent

Foggy sense of last week's KPIs → 30-minute scan + one experiment chosen for next week.

## Scope

30-minute KPI scan: MRR / churn / activation / signup funnel reviewed, anomalies flagged, one experiment chosen for next week, one growth lever pushed. Exit artifact is weekly pulse note + next-week experiment ticket.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Quarterly pricing decisions — separate quarterly playbook
- Deep cohort analysis — monthly cadence

### Prerequisites

- Analytics live (Plausible / GA + Stripe events)
- Dashboard configured (ops-dashboard-setup complete)

## Success criteria

The playbook is done when:
- MRR + churn + activation + signups noted weekly
- Anomalies flagged with hypothesis
- 1 experiment chosen for next week with owner + metric
- Pulse completed in ≤30 minutes

## Stages

### Stage 1: Pull

**Intent:** Pull the numbers; don't interpret yet.

**Tasks:**
- Open dashboard
- Note MRR / churn / activation / signups
- Compare to last week

**Methodologies in chain:**
- `plausible-analytics` → `solo/marketing/growth-marketer/plausible-analytics`
- `ops-dashboard-setup` → `solo/marketing/growth-marketer/ops-dashboard-setup`
- `product-analytics` → `solo/product/product-operations/product-analytics`

**Outputs:**
- Weekly pulse row

**Decision gate:**
> Advance when all 4 numbers are on paper. Don't theorise before they're listed.

### Stage 2: Flag

**Intent:** Anomaly hunt: what's off vs expected.

**Tasks:**
- Mark anomalies (red/yellow)
- Write 1-sentence hypothesis per anomaly
- Tag for follow-up

**Methodologies in chain:**
- `ab-testing-basics` → `solo/dev/automation-tooling/ab-testing-basics`
- `ab-testing-implementation` → `solo/dev/automation-tooling/ab-testing-implementation`

**Outputs:**
- Anomaly list with hypotheses

**Decision gate:**
> Advance when each anomaly has a hypothesis. Refuse to leave unflagged.

### Stage 3: Choose

**Intent:** Pick ONE experiment for next week. Define metric.

**Tasks:**
- List 3 candidate experiments
- Pick highest impact-per-effort
- Write success metric + decision date

**Methodologies in chain:**
- `growth-landing-page-design` → `solo/marketing/conversion-optimizer/growth-landing-page-design`
- `ops-subscription-models` → `solo/marketing/gtm-strategist/ops-subscription-models`
- `okr-setting` → `solo/product/product-manager/okr-setting`
- `outcome-based-roadmaps` → `solo/product/product-manager/outcome-based-roadmaps`

**Outputs:**
- Next-week experiment ticket

**Decision gate:**
> Required output: 1 experiment ticket. Refuse multi-experiment weeks (single-operator constraint).

## Common pitfalls

- Looking at MRR daily and panicking — weekly cadence is the rule
- Choosing 3 experiments because all looked interesting — kills focus

## Quality checklist (self-review)

- Is the chosen experiment actually shippable in one week solo?
- Did I write hypotheses for anomalies, or just stare at red numbers?

## Related playbooks

- `sunday-roadmap-ritual`
- `quarterly-persona-pricing-recal`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-kpi-dashboard-template** (tier `solo`, blocks stage 1) — Pull stage needs ready-to-use one-page solo dashboard template
- **single-operator-funnel-rubric** (tier `solo`, blocks stage 2) — Flag stage needs rubric for spotting anomalies at solo-scale traffic

## CLI usage

```
faion get-content friday-metrics-mrr-pulse --format md       # human-readable rendering
faion get-content friday-metrics-mrr-pulse --format context  # agent-optimised context bundle
faion get-content friday-metrics-mrr-pulse --format json     # raw structured form
```
