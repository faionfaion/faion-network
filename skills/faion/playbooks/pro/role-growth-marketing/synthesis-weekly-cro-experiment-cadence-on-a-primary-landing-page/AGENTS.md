---
slug: synthesis-weekly-cro-experiment-cadence-on-a-primary-landing-page
tier: pro
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: A growth team or solopreneur runs one disciplined landing-page experiment per week (hypothesis → variant → traffic split → readout → rollout/kill) with cumulative compounding lift logged in an expe...
content_id: a17f110d93135398
methodology_refs:
  - funnel-tactics-advanced
  - growth-conversion-optimization
  - competitor-creative-scrape-ai
  - stat-power-precheck
  - cro-guardrail-metrics
  - experiment-hypothesis-scoring
  - experiment-ledger-discipline
  - experiment-readout-template
---

# Synthesis: Weekly CRO experiment cadence on a primary landing page

A 7-stage playbook for the synthesis angle. Tier: **pro**. Complexity: **medium**.

## Context

A growth team or solopreneur runs one disciplined landing-page experiment per week (hypothesis → variant → traffic split → readout → rollout/kill) with cumulative compounding lift logged in an experiment ledger

## Outcome

A compound discipline that survives the founder's attention shifting elsewhere: scaffold in repo, cadence in the calendar, signal in the dashboard, next owner trained.

## Steps

### 1. Hypothesis

State the compound discipline you want to install and why it compounds.

Tasks:
- Write the explicit thesis: what compounding behaviour you are installing
- List the prior interventions this builds on
- Set a measurable signal that says the discipline is taking hold

Methodologies:
- `pro/role-growth-marketing/competitor-creative-scrape-ai`
- `pro/role-growth-marketing/stat-power-precheck`

Outputs:
- One-page thesis doc

Decision gate: Advance only with a written compound thesis and signal.

### 2. Scaffolding

Set up the templates, dashboards, and rituals before any output.

Tasks:
- Build the template/ledger/dashboard once
- Define the cadence (daily / weekly / per-event)
- Pre-stage the inputs you will need each cycle

Methodologies:
- `pro/role-growth-marketing/cro-guardrail-metrics`

Outputs:
- Templates + cadence committed to repo/wiki

Decision gate: Advance only after the scaffold survives a dry-run cycle.

### 3. First cycle

Run the first cycle exactly as specified; capture friction without fixing it yet.

Tasks:
- Run the cycle end-to-end without optimising
- Capture every friction point in the ledger
- Resist the urge to redesign the scaffold mid-cycle

Methodologies:
- `pro/role-growth-marketing/experiment-hypothesis-scoring`

Outputs:
- First-cycle output + friction log

Decision gate: Advance only when the cycle produced its intended output, even if ugly.

### 4. Reduce friction

Fix the top 3 friction points so the next cycle is faster, not just cleaner.

Tasks:
- Rank friction points by cost per cycle
- Fix the top 3; leave the rest documented
- Update the scaffold templates with the fixes

Methodologies:
- `pro/role-growth-marketing/experiment-ledger-discipline`

Outputs:
- Updated scaffold + friction-reduction log

Decision gate: Advance only after each fix has a 'why this saves time per cycle' rationale.

### 5. Repeat

Run cycles back-to-back to prove the discipline compounds, not just executes once.

Tasks:
- Run 3-5 cycles in a row at the agreed cadence
- Track output + friction + signal each cycle
- Do not skip cycles to make the dashboard look good

Methodologies:
- `pro/role-growth-marketing/experiment-readout-template`

Outputs:
- Cycle ledger with N entries

Decision gate: Advance only when 3+ consecutive cycles show the signal moving the right way.

### 6. Audit

Step outside the cadence and ask: is this discipline actually paying off?

Tasks:
- Compare signal trajectory vs the hypothesis
- Interview anyone running cycles for what's still painful
- Write the verdict: keep / change / kill the discipline

Methodologies:
- `pro/marketing/conversion-optimizer/funnel-tactics-advanced`

Outputs:
- Audit memo with verdict

Decision gate: Required output: a written verdict, never "let's keep going and reassess".

### 7. Institutionalize

If the discipline pays off, embed it so it survives founder/team turnover.

Tasks:
- Promote scaffold + cadence into the official ops doc
- Train the next owner to run it from the doc alone
- Add the metric to the rolling team review

Methodologies:
- `pro/marketing/conversion-optimizer/growth-conversion-optimization`

Outputs:
- Discipline lives in the ops doc + review

Decision gate: Advance only after the next owner runs one full cycle solo.

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/pro/marketing/conversion-optimizer/funnel-tactics-advanced`
- `knowledge/pro/marketing/conversion-optimizer/growth-conversion-optimization`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
