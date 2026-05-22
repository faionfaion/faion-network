---
slug: productmarket-fit-hunt-post-mvp-pre-traction
tier: pro
group: solo-saas
persona: P1
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: MVP is live but stuck under ~$1K MRR.
content_id: 371fa3c2b7b7d333
methodology_refs:
  - aarrr-pirate-metrics
  - north-star-metric
  - architecture-decision-records
  - ab-testing-basics
  - retention-metrics
  - trade-off-decision-matrix
  - ab-testing-setup
  - competitive-positioning
  - growth-landing-page-design
  - activation-framework
  - continuous-discovery-habits
  - user-interviews
  - activation-tactics
  - competitive-intelligence
  - value-proposition-design
  - cohort-basics
  - competitor-analysis
  - cohort-implementation
  - mom-test
---

# Product/Market Fit hunt (post-MVP, pre-traction)

## Intent

MVP is live but stuck under ~$1K MRR.

## Scope

MVP is live but stuck under ~$1K MRR. Run a structured discovery+positioning+experiment loop until either a fit signal is reached (retention curve flattens, NPS-style pull, organic referrals) or a documented pivot is triggered.

## Stages

### 1. Diagnose stuck signal

Confirm we are truly stuck and identify the leak.

Tasks:
- Pull cohort retention, activation, and growth curves
- Compare current data to PMF rubric thresholds
- Identify the single biggest leak (acquisition / activation / retention / revenue)

Outputs:
- Diagnostic report
- AARRR funnel snapshot
- Leak-of-the-quarter call

Decision gate: Advance with a named leak. If retention flat AND no leak found, sunset path opens.

### 2. Power interviews

Asymmetric churn + power-user interviews to find the missing job.

Tasks:
- Interview 5 power users who love the product
- Interview 5 churned/lapsed users on why they left
- Surface the dominant job-to-be-done vs the imagined one

Outputs:
- 10 interview transcripts
- JTBD revision
- Churn theme list

Decision gate: Advance if a clear job we are actually hired for emerges, else recruit another 5.

### 3. Positioning sharpen

Re-write positioning around the real job, not the imagined one.

Tasks:
- Update the one-liner, headline, and category claim
- Map differentiators against top-3 competitors
- Re-shoot landing page above the fold

Outputs:
- New positioning doc
- Updated landing hero
- Competitor delta map

Decision gate: Advance when 3 outsiders can repeat the positioning back unprompted.

### 4. Experiment design

Pick 1-3 focused experiments per fortnight, not 10.

Tasks:
- List candidate experiments tied to the named leak
- Score by RICE, pick top 1-3
- Pre-register hypothesis + success metric for each

Outputs:
- Experiment backlog
- Pre-registered hypotheses
- Sample-size estimate

Decision gate: Advance only with a north-star metric movement target per experiment.

### 5. Run + measure

Ship experiments and let them cook for one full cohort.

Tasks:
- Implement experiment behind a flag
- Hold for at least one cohort cycle
- Read results against pre-registered metric

Outputs:
- Experiment readout per test
- Cohort impact chart
- Decision per experiment

Decision gate: Advance when each experiment has a clear keep/kill/iterate call.

### 6. Re-score against PMF rubric

Honest re-check against the PMF rubric for solos.

Tasks:
- Re-run the PMF rubric scoring
- Compare to baseline at start of hunt
- Decide if the curve flattened, lifted, or stayed flat

Outputs:
- Updated rubric score
- Trend chart
- Confidence call

Decision gate: Advance if score moved up >=1 band. If flat for 2 consecutive cycles, escalate to pivot.

### 7. Decide: continue / pivot / sunset

Written commitment based on the rubric trend.

Tasks:
- Write the decision with evidence trail
- If continue, commit to the next 90-day milestone
- If pivot, hand off to the v1-to-v2 playbook
- If sunset, plan a clean shutdown

Outputs:
- Decision doc
- 90-day commitment OR pivot brief OR sunset plan

Decision gate: No maybe allowed. Document must name a single path forward.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
