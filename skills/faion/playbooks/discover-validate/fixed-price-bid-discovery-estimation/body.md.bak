# Fixed-price bid discovery + estimation (1 week)

**Persona:** P4 Outsource Specialist · **Tier:** pro · **Complexity:** deep · **Angle:** global

## Why this playbook exists

Pre-sales discovery on a fixed-price proposal → discovery report, sized three-point estimate with risk reserves, defensible margin, and a bid/no-bid recommendation the delivery team will not regret six months later.

Week-long pre-sales sprint. Daria leads the discovery on a prospective fixed-price engagement. Output is: discovery report, three-point estimate with assumptions + risk reserves, defensible margin, and a bid/no-bid memo. The proposal must survive an internal red-team and a delivery-side retro six months later.

Most outsource seniors improvise this flow — fine at one engagement, costly across five. This playbook fixes the chain: explicit stages, explicit decision-gates, written artifacts at every step, AI agents on a leash, no silent work absorption.

## How to run it

Walk the stages in order. Each stage has a decision-gate; do not advance until the gate condition is met in writing. A stranger should be able to read the artifacts and understand both *what* you did and *why* you advanced. Atomic stages are designed to be completed in a single sitting; deep stages span multiple sessions.

## Stage map

### Stage 1 — Brief intake & qualifying

**Intent:** Read the brief, decide whether to invest the week.

**Tasks**
- Map decision-makers, influencers, blockers in the buyer org
- Identify strategic fit vs portfolio (industry, stack, regulatory exposure)
- Run 30-min sales-to-delivery handoff covering risk signals
- Pull comparable-projects business-model data

**Outputs**
- Stakeholder map
- Strategic fit memo
- Risk signals log

**Decision gate**

Advance if strategic fit ≥3/5 AND no fatal risk signal (broken AP history, hostile procurement, mandated stack we cannot staff). Else no-bid early.

### Stage 2 — Discovery interviews

**Intent:** Convert brief into a defendable scope outline.

**Tasks**
- Run 3-5 elicitation interviews with named stakeholders
- Document business-process current state where it touches scope
- Surface integration interfaces (systems, APIs, data feeds)
- Build a solution-assessment matrix (build vs buy vs hybrid)

**Outputs**
- Interview notes pack
- Integration interface inventory
- Solution-assessment matrix

**Decision gate**

Advance when scope outline is defendable on the integration interfaces. If interfaces are still vague, extend interviews or no-bid.

### Stage 3 — Architecture + NFR sizing

**Intent:** Sketch enough architecture to size; not enough to ship.

**Tasks**
- Pick candidate cloud architecture pattern
- Capture quality attributes (perf, sec, availability) the prospect implies
- Identify the riskiest unknowns (the things you'd want to spike if you could)
- Draft design-doc structure for the proposal annex

**Outputs**
- Architecture sketch (1 page)
- NFR table
- Top-3 spike candidates documented

**Decision gate**

Advance once you can write the architecture sketch in one page. If you cannot, the brief is too ambiguous for fixed-price — convert to T&M or no-bid.

### Stage 4 — Estimate + risk reserves

**Intent:** Three-point estimate, WBS, schedule, procurement, risk reserves — all defensible.

**Tasks**
- Build WBS to leaf-level for top deliverables
- Three-point estimate (optimistic, realistic, pessimistic) per leaf
- Stack risk reserves: scope, technical, schedule, FX
- Sketch milestone schedule with EVM tracking points
- Identify procurement exposure (third-party licenses, dependencies)

**Outputs**
- WBS to leaf-level
- Three-point estimate sheet
- Risk register with reserves
- Milestone schedule

**Decision gate**

Advance when P80 estimate + reserves yields margin above the floor. If P50 already underwater, no-bid.

### Stage 5 — Red-team + bid/no-bid

**Intent:** Stress-test the proposal and ship a clean recommendation.

**Tasks**
- Hand the package to a peer estimator for red-team review
- Apply red-team challenges; rerun the estimate where needed
- Score the deal on a bid/no-bid scorecard (margin, fit, risk, AP history)
- Write the recommendation memo (one page max)

**Outputs**
- Red-team notes
- Scorecard with numeric verdict
- Bid/no-bid recommendation memo

**Decision gate**

Final gate: bid only on green scorecard + green margin band. Yellow forces senior partner approval. Red is no-bid; archive the work for next time.

## Common pitfalls

- Skipping the red-team because 'we're under time' — that's exactly when you need it
- Padding the estimate uniformly instead of pricing the actual risks
- Treating bid/no-bid as a sales decision — it's a delivery decision with sales input

## Quality checklist

- Could a peer re-derive the estimate from my assumptions log?
- Did I name the risks that would burn the margin?
- Is the recommendation a verb, not a hedge?

## Related playbooks

- `scoping-workshop`
- `statement-of-work`
- `fixed-price-vs-tm-estimation-ai-buffer`

## Gaps

These methodologies are referenced in the chain above but not yet materialised. They block promotion of this playbook from `draft` to `published`.

- `fixed-price-three-point-estimation` (blocks stage 4)
- `bid-no-bid-scorecard` (blocks stage 5)
- `proposal-red-team-checklist` (blocks stage 5)
