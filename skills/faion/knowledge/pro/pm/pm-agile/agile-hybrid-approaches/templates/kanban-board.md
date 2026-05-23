<!-- purpose: Kanban board template with WIP limits and explicit policies. -->
<!-- consumes: see content/02-output-contract.xml inputs for agile-hybrid-approaches -->
<!-- produces: decision-record -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Kanban Board

## Backlog (no limit)
- [ ] Feature A
- [ ] Feature B
- [ ] Bug X

## Ready (WIP: 5)
Items that meet the entry criteria and are ready to start.
- [ ] Feature C (assigned: [name])
- [ ] Feature D (assigned: [name])

## In Progress (WIP: 3)
- [>] Feature E — [name] (day 2 of 3)
- [>] Bug Y — [name] (day 1)

## Review (WIP: 2)
- [?] Feature F — waiting for [name] review

## Done
- [x] Feature G — shipped [date]
- [x] Bug Z — resolved [date]

---

**WIP Policy:** items exceeding the WIP limit block new starts.
Violation triggers a team discussion, not a silent override.
