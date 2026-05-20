---
slug: fixed-price-three-point-estimation
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "21d29fd265e2761a"
summary: "Three-point + Monte Carlo cost recipe tuned for outsource fixed-price bids: every WBS leaf gets O/M/P estimates anchored to senior-dev hourly economics and an AI-agent productivity factor, then 10k-run simulation produces a P85 bid price plus a separate vendor risk reserve."
tags: [pm, pro, estimation, fixed-price, monte-carlo, outsource, bid]
---
# Fixed-Price Three-Point Estimation

## Summary

Faion's pm/pm-traditional/cost-estimation is too generic for outsource fixed-price bids: it gives PERT but says nothing about vendor risk reserves, AI-agent productivity factors, or how to anchor optimistic/most-likely/pessimistic numbers to a senior developer's hourly economics. This methodology specialises three-point + Monte Carlo for the P4 outsource specialist: every WBS leaf gets O/M/P in senior-dev hours, risk-loaded by category (integration, unknowns, change-request exposure), simulated 10k runs, and the bid is set at P85 with a separately disclosed vendor reserve. The output is a defensible price that survives buyer pushback because each number traces back to an assumption.

## Applies If

- The engagement is a fixed-price (firm-price) bid, not Time & Materials.
- A WBS exists or can be drafted with leaf tasks at "1-5 dev-day" granularity.
- The team's senior developer hourly rate (loaded, in the relevant currency) is known.
- A spreadsheet or scripting environment is available to run 10k Monte Carlo iterations.

## Skip If

- The contract is Time & Materials — three-point estimation overhead is not justified; use a velocity-based forecast instead.
- The WBS is too coarse to estimate at leaf level (no leaves &lt; 1 week) — refine the WBS first.
- The scope is so volatile that no most-likely estimate is honest — bid no-bid or restructure as discovery + delivery.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules covering anchoring, AI-productivity factor, risk reserves, Monte Carlo discipline, and the P85-plus-reserve disclosure pattern |

## Related

- parent skill: `pro/pm/`
- triggering activity: `Fixed-price bid discovery + estimation (1 week)`, `T&M to fixed-price contract conversion (6 weeks)`
- neighbouring: `pro/pm/fixed-price-vs-tnm-decision-framework`, `geek/ba/fixed-price-risk-loading-model`
