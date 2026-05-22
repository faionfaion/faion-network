---
slug: synthesis-launch-week-orchestration-for-an-ai-feature-release
tier: pro
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: acquire-grow
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Coordinate a single product release across PH/HN/Reddit/LinkedIn/X/email/paid in one shared timeline, with role/owner per surface and a post-mortem ledger
content_id: 23c4758f213710f3
methodology_refs:
  - growth-brand-positioning
  - growth-hacker-news-launch
  - growth-product-hunt-launch
  - ai-feature-positioning-framework
  - launch-postmortem-template
  - launch-warroom-protocol
  - post-launch-content-drip
  - waitlist-warmup-sequence
---

# Synthesis: Launch-week orchestration for an AI-feature release

A 9-stage playbook for the synthesis angle. Tier: **pro**. Complexity: **deep**.

## Context

Coordinate a single product release across PH/HN/Reddit/LinkedIn/X/email/paid in one shared timeline, with role/owner per surface and a post-mortem ledger

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
- `pro/role-growth-marketing/ai-feature-positioning-framework`

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
- `pro/marketing/gtm-strategist/growth-brand-positioning`

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
- `solo/marketing/gtm-strategist/growth-hacker-news-launch`

Outputs:
- First-cycle output + friction log

Decision gate: Advance only when the cycle produced its intended output, even if ugly.

### 4. Variant test

Try one structural variant of the scaffold and pick the winner on evidence.

Tasks:
- Identify one variable in the scaffold worth testing
- Run cycles in both variants in parallel or AB
- Pick the winner with a written rationale

Methodologies:
- `solo/marketing/gtm-strategist/growth-product-hunt-launch`

Outputs:
- Variant test readout

Decision gate: Advance only with a written winner-pick; do not run both forever.

### 5. Reduce friction

Fix the top 3 friction points so the next cycle is faster, not just cleaner.

Tasks:
- Rank friction points by cost per cycle
- Fix the top 3; leave the rest documented
- Update the scaffold templates with the fixes

Methodologies:
- `pro/role-growth-marketing/launch-postmortem-template`

Outputs:
- Updated scaffold + friction-reduction log

Decision gate: Advance only after each fix has a 'why this saves time per cycle' rationale.

### 6. Repeat

Run cycles back-to-back to prove the discipline compounds, not just executes once.

Tasks:
- Run 3-5 cycles in a row at the agreed cadence
- Track output + friction + signal each cycle
- Do not skip cycles to make the dashboard look good

Methodologies:
- `pro/role-growth-marketing/launch-warroom-protocol`

Outputs:
- Cycle ledger with N entries

Decision gate: Advance only when 3+ consecutive cycles show the signal moving the right way.

### 7. Counter-pressure

Pressure-test the discipline against the failure modes that historically killed it.

Tasks:
- List the historical failure modes for this kind of cadence
- Stress-test the scaffold against each one
- Patch the scaffold against the failure mode that lands

Methodologies:
- `pro/role-growth-marketing/post-launch-content-drip`

Outputs:
- Stress-test memo + patches

Decision gate: Advance only after every historical failure mode has a documented mitigation.

### 8. Audit

Step outside the cadence and ask: is this discipline actually paying off?

Tasks:
- Compare signal trajectory vs the hypothesis
- Interview anyone running cycles for what's still painful
- Write the verdict: keep / change / kill the discipline

Methodologies:
- `pro/role-growth-marketing/waitlist-warmup-sequence`

Outputs:
- Audit memo with verdict

Decision gate: Required output: a written verdict, never "let's keep going and reassess".

### 9. Institutionalize

If the discipline pays off, embed it so it survives founder/team turnover.

Tasks:
- Promote scaffold + cadence into the official ops doc
- Train the next owner to run it from the doc alone
- Add the metric to the rolling team review

Methodologies:
- `pro/role-growth-marketing/ai-feature-positioning-framework`

Outputs:
- Discipline lives in the ops doc + review

Decision gate: Advance only after the next owner runs one full cycle solo.

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/pro/marketing/gtm-strategist/growth-brand-positioning`
- `knowledge/solo/marketing/gtm-strategist/growth-hacker-news-launch`
- `knowledge/solo/marketing/gtm-strategist/growth-product-hunt-launch`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
