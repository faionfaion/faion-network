<!-- purpose: Prioritization matrix template. -->
<!-- consumes: input from methodology -->
<!-- produces: artefact for downstream agent -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-500 tokens when loaded as context -->

## Debt Prioritization: [Quarter]

### Scoring

| ID | Debt | Interest (40%) | Contagion (20%) | Effort (20%) | Alignment (20%) | Score |
|----|------|----------------|-----------------|--------------|-----------------|-------|
| TD-001 | [Name] | 5 | 3 | 2 | 5 | 8.5 |
| TD-002 | [Name] | 3 | 2 | 4 | 3 | 4.0 |

Score formula: (Interest × 0.4 + Contagion × 0.2) × Alignment / max(Effort, 1)

### This Quarter's Plan

**Capacity allocated:** [X]% = [Y] days

| ID | Debt | Effort | Sprint | Owner |
|----|------|--------|--------|-------|
| TD-001 | [Name] | 2 days | Sprint 1 | [Name] |
| TD-004 | [Name] | 3 days | Sprint 2 | [Name] |

### Deferred

| ID | Debt | Reason | Revisit |
|----|------|--------|---------|
| TD-003 | [Name] | Low alignment | Q3 |

### Sprint Debt Budget

**Sprint [X] Debt Work:**
- Available: [X] days (20% of capacity)
- Planned: [X] days

| Item | Description | Effort | Owner | Status |
|------|-------------|--------|-------|--------|
| [TD-X] | [Description] | 1d | [Name] | Done |
| Boy Scout | Ad-hoc improvements during feature work | 0.5d | Team | Ongoing |
