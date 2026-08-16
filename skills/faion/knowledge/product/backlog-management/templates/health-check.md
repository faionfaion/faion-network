<!--
purpose: DEEP/INVEST backlog health check — bucket and type breakdown plus health metrics against targets.
consumes: backlog snapshot (bucket counts, item ages, AC coverage, source-link coverage)
produces: a backlog health check report
depends-on: content/01-core-rules.xml (r6-180d-archive and the DEEP/INVEST target thresholds)
token-budget-impact: ~250 tokens when filled
-->

# Backlog Health Check: <product>

## Snapshot
- **Date:** <date>
- **Total items:** [X]
- **Ready items:** [X]
- **Stale items (180+ days):** [X]

## By Status

| Status | Count | % |
|--------|-------|---|
| Ready | [X] | [X]% |
| Upcoming | [X] | [X]% |
| Backlog | [X] | [X]% |
| Icebox | [X] | [X]% |

## By Type

| Type | Count |
|------|-------|
| Feature | [X] |
| Bug | [X] |
| Tech debt | [X] |
| Research | [X] |

## Health Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Ready items | [X] | 8-25 | OK/Needs work |
| Avg item age (days) | [X] | <90 | OK/Needs work |
| Stale % | [X]% | <10% | OK/Needs work |
| Items with Given/When/Then AC | [X]% | >80% | OK/Needs work |
| Items without source link | [X] | 0 | OK/Needs work |

## Actions Needed
- [ ] <action_1>
- [ ] <action_2>
