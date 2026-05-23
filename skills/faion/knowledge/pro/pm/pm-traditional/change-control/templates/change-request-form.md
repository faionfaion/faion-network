<!-- purpose: Change Request Form template: trigger, impact, alternatives, recommendation -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Change Request Form

**CR ID:** CR-[YYYY]-[NNN]
**Date:** [Date]
**Requester:** [Name] ([Role])
**Priority:** Critical / High / Medium / Low

## Description
[Clear description of the proposed change.]

## Business Justification
[Why is this change needed? What business outcome does it enable or what problem does it solve?]

## Impact Analysis

| Area | Impact | Detail |
|------|--------|--------|
| Scope | [WBS IDs affected] | [Description] |
| Schedule | +[X] days | [Which milestones move] |
| Cost | +$[X] | [Which budget lines] |
| Quality | [None / Low / Medium / High] | [Description] |
| Test impact | +[X] days | [Regression/integration scope] |
| Risk | [New risks introduced] | [Description] |
| Resources | [Who, how long] | [Opportunity cost] |

## Options

| Option | Days | Cost | Notes |
|--------|------|------|-------|
| A: [Recommended] | [X] | $[X] | [Description] |
| B: [Alternative] | [X] | $[X] | [Description] |
| C: Do nothing | 0 | $0 | [Cost of inaction] |

**Recommendation:** Option [A/B/C] — [one-line rationale]

## Decision Authority
- [ ] Minor (< 1 day, < $500) — PM approves
- [ ] Medium (1-5 days, $500-$5k) — Sponsor approves
- [ ] Major (> 5 days, > $5k) — CCB approves

## Decision

- [ ] Approved (Option _____)
- [ ] Rejected (reason: _________________________)
- [ ] Deferred (to: ___________________________)

**Decided by:** _________________ **Date:** ________________

**Baseline update commit:** _________________ (required if Approved)
