<!--
purpose: ATAM-style utility tree — quality attributes scored (Importance, Difficulty), active (H,H) drivers, sensitivity points, trade-offs.
consumes: nothing beyond the system's identified quality attributes
produces: utility tree artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~260 tokens when filled
-->

# Utility Tree: <system_name>

**Priority notation:** (Importance, Difficulty) where H=High, M=Medium, L=Low.
**Rule:** At most 7 quality attributes. At most 3 (H,H) drivers. Cap (H,H) scenarios at 3 per tree.

## Utility

- **Performance** (H, ?)
  - Latency: [scenario title] (H/M/L, H/M/L)
  - Throughput: [scenario title] (H/M/L, H/M/L)

- **Availability** (H, ?)
  - Uptime: [scenario title] (H/M/L, H/M/L)
  - Recovery: [scenario title] (H/M/L, H/M/L)

- **Security** (H/M, ?)
  - Authentication: [scenario title] (H/M/L, H/M/L)
  - Data protection: [scenario title] (H/M/L, H/M/L)

- **Maintainability** (M, ?)
  - Modifiability: [scenario title] (H/M/L, H/M/L)
  - Testability: [scenario title] (H/M/L, H/M/L)

- **Scalability** (M/H, ?)
  - Horizontal: [scenario title] (H/M/L, H/M/L)

## Active (H,H) Drivers (max 3)

1. [Scenario title] — [one-line description]
2. [Scenario title] — [one-line description]
3. [Scenario title] — [one-line description]

## Sensitivity Points

- [Decision A] affects [attribute X] significantly; small change → large impact
- ...

## Trade-offs

- <decision_b> improves [attribute X] at the cost of <attribute_y> by <amount>
- ...

## Reviewed By

- [ ] Engineering lead: <name>
- [ ] Business owner: <name>
- [ ] Date: YYYY-MM-DD
- [ ] Next refresh: YYYY-MM-DD (recommend quarterly)
