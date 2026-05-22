---
slug: multi-product-portfolio-rotation-ship-n-small-bets-per-year
tier: solo
group: indie-hacker
persona: P2
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Run a recurring rotation that ships 4–6 small products per year, keeps 2–3 alive based on traction, sunsets the rest, and compounds the surviving ones into a portfolio that reaches ramen profitabil...
content_id: 6b6b158b45858370
methodology_refs:
  - automation-tooling
  - idea-generation
  - growth-content-marketing
  - idea-generation-methods
  - ops-customer-support
  - feature-discovery
  - feature-prioritization-moscow
  - feature-prioritization-rice
  - product-analytics
  - product-lifecycle
  - micro-mvps
  - outcome-based-roadmaps
---

# Multi-product portfolio rotation: ship N small bets per year

## Intent

Run a recurring rotation that ships 4–6 small products per year, keeps 2–3 alive based on traction, sunsets the rest, and compounds the surviving ones into a portfolio that reaches ramen profitability.

## Scope

Run a recurring rotation that ships 4–6 small products per year, keeps 2–3 alive based on traction, sunsets the rest, and compounds the surviving ones into a portfolio that reaches ramen profitability.

## Stages

### 1. Portfolio scorecard

See every bet on one page.

Tasks:
- List every shipped product with revenue + load
- Score each on traction, founder energy, and growth potential
- Tag each: grow / maintain / sunset / new

Outputs:
- Scorecard
- Per-product tags
- Quarterly summary

Decision gate: Advance only when every product has a tag.

### 2. Maintain-mode SOPs

Make survivors run themselves.

Tasks:
- Define maintain-mode (uptime, support SLA, no new features)
- Automate or hand-off recurring tasks
- Set monthly maintenance checkpoints

Outputs:
- Maintain SOP per product
- Automation tickets
- Maintenance calendar

Decision gate: Advance only when each survivor has <=1 hour/week of human load.

### 3. Idea pipeline refill

Always have 5-10 candidate bets queued.

Tasks:
- Run idea-generation against current themes
- Score candidates by founder-fit + market signal
- Pick the next bet

Outputs:
- Candidate idea list
- Scored pipeline
- Next-bet pick

Decision gate: Advance only when pipeline has >=5 named candidates.

### 4. Tiny-bet ship cadence

Ship a new MVP every 6-8 weeks.

Tasks:
- Cut scope ruthlessly to micro-MVP
- Ship within the cadence window
- Set an early kill date

Outputs:
- Micro-MVP shipped
- Ship-date stamp
- Kill-date stamp

Decision gate: Advance only when shipped within cadence window.

### 5. Traction read at kill date

Honest cull at the predetermined date.

Tasks:
- Read traction metrics at the kill date
- Compare to pre-set survive threshold
- Tag: grow / maintain / sunset

Outputs:
- Kill-date readout
- Survive/sunset call
- Updated portfolio scorecard

Decision gate: Advance only when call is made on schedule (no extensions).

### 6. Sunset clean

Close down losers without lingering cost.

Tasks:
- Run the refund/migrate/notify pack
- Archive code + docs
- Cancel underlying paid services

Outputs:
- Sunset comms
- Archive log
- Cancelled-services log

Decision gate: Advance only when zero recurring cost remains for the killed product.

### 7. Reinvest in survivors

Compound winners with the freed capacity.

Tasks:
- Pick the strongest survivor
- Pour 1 cycle into its growth lever
- Measure lift

Outputs:
- Survivor growth experiment
- Lift measurement
- Updated scorecard

Decision gate: Advance only when survivor lift is measurable.

### 8. Quarterly portfolio review

Re-balance like an investor.

Tasks:
- Walk the scorecard with an outsider mindset
- Re-tag every product
- Commit the next-quarter rotation

Outputs:
- Quarterly review doc
- Updated tags
- Next-quarter plan

Decision gate: Cycle closes when next-quarter plan is committed.

### 9. Annual portfolio reset

Once a year, ask the brutal questions.

Tasks:
- Audit profitability vs personal goals
- Decide which products to keep into next year
- Write the annual portfolio thesis

Outputs:
- Annual audit
- Keep-list
- Portfolio thesis

Decision gate: Cycle closes when thesis is committed for the new year.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
