<!--
purpose: Quarterly OKR sheet — objectives with kill conditions, measurable key results, check-in log
consumes: company strategy statement + current baseline metrics
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-900 tokens when loaded as context
variables:
  - name: team_name
    type: string
    required: true
    description: The team or product these OKRs belong to. One owner set per sheet - OKRs shared between two teams are OKRs nobody can be held to when the quarter goes badly.
  - name: quarter
    type: string
    required: true
    description: The period, e.g. "Q4 2026". Scoring happens against this window; an undated OKR sheet becomes a wish list that rolls forward until it is quietly deleted.
  - name: objective_one
    type: text
    required: true
    description: The first Objective as a statement of the change you want, not a number. If it reads like a Key Result you have written the target and skipped the reason anyone should care about it.
  - name: kill_condition_one
    type: text
    required: true
    description: The leading indicator that, if it has not moved by week 6, means you drop this Objective. Deciding it now is the only real defence against spending a whole quarter on a dead bet.
  - name: objective_one_owner
    type: string
    required: true
    description: The single person accountable for Objective 1. Not the team. The owner is who calls the kill condition, and a committee has never killed anything on time.
  - name: date
    type: string
    required: true
    description: The date these were committed, ISO. Anything added after it is a mid-quarter change and should be visible as one, rather than appearing to have been the plan all along.
-->
# OKRs: {{team_name}} — {{quarter}}

## Objective 1: {{objective_one}}

**Why this matters:** [1-2 sentences linking to company strategy or current reality]
**Kill condition:** {{kill_condition_one}}
**Owner:** {{objective_one_owner}}

| Key Result | Baseline | Target | Confidence | Current | Score |
|------------|----------|--------|------------|---------|-------|
| KR 1.1: [Measurable outcome, not a task] | [Number today] | [Goal] | High/Med/Low | [Now] | [0-1] |
| KR 1.2: [Measurable outcome] | [Number today] | [Goal] | High/Med/Low | [Now] | [0-1] |
| KR 1.3: [Measurable outcome] | [Number today] | [Goal] | High/Med/Low | [Now] | [0-1] |

**Status:** On Track / At Risk / Off Track

---

## Objective 2: [Inspiring qualitative goal statement]

**Why this matters:** [1-2 sentences]
**Kill condition:** [Drop this Objective if the named leading indicator has not moved by Week 6]
**Owner:** [Name]

| Key Result | Baseline | Target | Confidence | Current | Score |
|------------|----------|--------|------------|---------|-------|
| KR 2.1: | | | | | |
| KR 2.2: | | | | | |
| KR 2.3: | | | | | |

---

## Summary

| Objective | Avg Score | Status |
|-----------|-----------|--------|
| O1 | [X] | [Status] |
| O2 | [X] | [Status] |

**Committed:** {{date}} | **Last Updated:** [Date]

## Check-in Log

| Week | O1 Confidence | O2 Confidence | Blockers | Actions |
|------|--------------|--------------|---------|---------|
| W1 | | | | |
| W2 | | | | |
