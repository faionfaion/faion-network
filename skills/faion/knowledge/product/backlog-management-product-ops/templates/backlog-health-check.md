<!--
purpose: Backlog health check snapshot — status/type breakdown and health metrics against the Now/Next/Icebox age-cap targets.
consumes: backlog snapshot (status counts, item ages, AC coverage, priority mix)
produces: a backlog health check report
depends-on: content/01-core-rules.xml (r2-age-cap, r4-capacity-ratio)
token-budget-impact: ~220 tokens when filled
-->

## Backlog Health Check: <product> — <date>

### Snapshot
- **Total items:** {X}
- **Ready items:** {X}
- **Stale items (6+ mo, no roadmap link):** {X}

### By Status

| Status | Count | % |
|--------|-------|---|
| Ready | {X} | {X}% |
| Upcoming | {X} | {X}% |
| Backlog | {X} | {X}% |
| Icebox | {X} | {X}% |

### By Type

| Type | Count |
|------|-------|
| Feature | {X} |
| Bug | {X} |
| Tech Debt | {X} |
| Research | {X} |

### Health Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Ready items | {X} | 10-20 | OK/Not |
| Average item age | {X} days | <90 | OK/Not |
| Stale % | {X}% | <10% | OK/Not |
| Items with AC | {X}% | >80% | OK/Not |
| P1 % | {X}% | <20% | OK/Not |

### Actions Needed
- [ ] <action_1>
- [ ] <action_2>
