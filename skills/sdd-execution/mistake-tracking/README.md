---
id: mistake-tracking
name: "Mistake Tracking"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Mistake Tracking

## Overview

Captures, analyzes, and documents errors and failures in development process. Creates collective knowledge base that helps teams avoid known pitfalls through structured root cause analysis and occurrence monitoring.

## When to Use

- After encountering any bug, error, or failure
- When tasks take significantly longer than estimated
- During incident post-mortems
- When reviewing code with common anti-patterns
- For onboarding (teaching what to avoid)
- When updating process documentation

## Mistake Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mistake Memory System                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Capture   │ →  │   Analysis  │ →  │ Prevention  │    │
│  │   Layer     │    │   Layer     │    │   Layer     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│  Incident         Root Cause          Checklists          │
│  Detection        Analysis            Automations         │
│  & Logging                            Pre-task Warnings   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Storage:**
```
~/.sdd/memory/
├── mistakes_learned.jsonl
├── mistakes_index.json
├── mistakes_stats.json
├── prevention_rules.json
└── incidents/
```

## Mistake Schema

```json
{
  "id": "MIS_2024_001",
  "version": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z",

  "metadata": {
    "category": "implementation",
    "subcategory": "data-handling",
    "severity": "high",
    "language": "python",
    "domain": "database",
    "tags": ["migration", "data-loss", "production"]
  },

  "mistake": {
    "title": "Database Migration Without Backup",
    "summary": "Ran destructive migration on production without backup",

    "what_happened": {
      "description": "Executed ALTER TABLE DROP COLUMN without backup. Lost 2 weeks of data.",
      "timeline": [
        "10:00 - Started migration script",
        "10:02 - Migration completed (appeared successful)",
        "10:30 - User report: missing data",
        "11:00 - Confirmed data loss",
        "14:00 - Restored from nightly backup (lost 12 hours)"
      ],
      "impact": {
        "data_loss": "12 hours of column data",
        "downtime": "4 hours",
        "cost": "16 developer hours for recovery",
        "user_impact": "50 users affected"
      }
    },

    "root_cause_analysis": {
      "immediate_cause": "No backup before destructive migration",
      "contributing_factors": [
        "No pre-migration checklist",
        "Overconfidence in tested migration",
        "Production database same as staging (bad practice)",
        "No migration rollback plan"
      ],
      "root_cause": "Missing process for destructive database operations"
    },

    "prevention": {
      "immediate_actions": [
        "Implement pre-migration backup requirement",
        "Add migration approval workflow"
      ],
      "process_changes": [
        "Create database migration checklist",
        "Require peer review for destructive migrations",
        "Implement automatic pre-migration snapshots"
      ],
      "automation": [
        "CI check: detect DROP/DELETE in migrations",
        "Pre-deployment: automatic backup trigger",
        "Alert: flag production-targeted destructive queries"
      ]
    }
  },

  "validation": {
    "occurrence_count": 1,
    "last_occurrence": "2024-01-15T10:00:00Z",
    "prevention_effectiveness": null
  }
}
```

## Mistake Categories

```yaml
estimation:
  - underestimating_complexity
  - missing_dependencies
  - optimistic_assumptions
  - unfamiliar_technology

implementation:
  - edge_cases_missed
  - error_handling_gaps
  - race_conditions
  - resource_leaks

data_handling:
  - no_backup
  - bad_migration
  - data_corruption
  - privacy_violation

security:
  - hardcoded_secrets
  - missing_validation
  - improper_auth
  - exposed_endpoints

deployment:
  - no_rollback_plan
  - untested_in_staging
  - config_mismatch
  - missing_dependencies

communication:
  - unclear_requirements
  - late_escalation
  - assumption_not_validated
  - missing_handoff

testing:
  - insufficient_coverage
  - flaky_tests
  - wrong_test_data
  - skipped_tests

process:
  - skipped_review
  - ignored_warnings
  - shortcut_taken
  - documentation_gap
```

## Root Cause Analysis

### Five Whys Framework

```markdown
## Root Cause Analysis: [Incident Title]

### Immediate Cause
[What directly caused the issue]

### Five Whys
1. Why did [immediate cause]?
   → [Answer 1]

2. Why [Answer 1]?
   → [Answer 2]

3. Why [Answer 2]?
   → [Answer 3]

4. Why [Answer 3]?
   → [Answer 4]

5. Why [Answer 4]?
   → [Root Cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]
- [Factor 3]

### Systemic Issues
- [Process gap]
- [Tool limitation]
- [Knowledge gap]
```

## Occurrence Tracking

```python
def track_mistake_occurrence(mistake_id: str, occurred: bool):
    """Track if a known mistake occurred or was prevented"""

    mistake = load_mistake(mistake_id)

    if occurred:
        mistake.validation.occurrence_count += 1
        mistake.validation.last_occurrence = datetime.now()
        # Escalate if recurring
        if mistake.validation.occurrence_count >= 3:
            escalate_recurring_mistake(mistake)
    else:
        # Mistake was prevented
        if not mistake.validation.prevention_effectiveness:
            mistake.validation.prevention_effectiveness = {"prevented": 0, "total": 0}
        mistake.validation.prevention_effectiveness["prevented"] += 1
        mistake.validation.prevention_effectiveness["total"] += 1

    save_mistake(mistake)
```

## Metrics Dashboard

```yaml
mistake_metrics:
  overview:
    total_documented: 45
    this_month: 3
    prevented_this_month: 12

  by_category:
    implementation: 15
    estimation: 10
    data_handling: 8
    security: 5
    deployment: 4
    process: 3

  by_severity:
    critical: 5
    high: 15
    medium: 18
    low: 7

  recurring:
    - MIS_2024_005: 3 occurrences
    - MIS_2024_012: 2 occurrences

  most_prevented:
    - MIS_2024_001: 8 times (backup reminder)
    - MIS_2024_015: 6 times (test coverage check)

  trends:
    estimation_accuracy: "improving"
    production_incidents: "decreasing"
    review_findings: "stable"
```

## Quick Mistake Capture

```markdown
## Mistake: [Brief Title]

**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Category:** [implementation / estimation / etc.]

**What Happened:**
[Brief description]

**Impact:**
[Time lost / data affected / users impacted]

**Root Cause:**
[Brief root cause]

**Prevention:**
- [ ] [Action 1]
- [ ] [Action 2]

**Discovered In:** TASK_XXX
```

## Monthly Review Template

```markdown
## Mistake Review: [Month Year]

### Summary
- New mistakes documented: X
- Recurring mistakes: Y
- Successfully prevented: Z

### Top Issues
1. [Mistake category]: [Count]
2. [Mistake category]: [Count]

### Prevention Effectiveness
| Prevention | Triggered | Prevented |
|------------|-----------|-----------|
| Backup reminder | 10 | 10 |
| Test coverage | 8 | 7 |

### Action Items
- [ ] Review MIS_XXX prevention (not effective)
- [ ] Add automation for MIS_YYY
- [ ] Update checklist for [category]

### Trends
[Are we getting better? Worse? Areas of concern?]
```

## Best Practices

### Blameless Culture
- **Focus on systems** - Not individuals
- **Assume good intent** - Everyone wants to succeed
- **Share openly** - Transparency aids learning
- **Celebrate finding** - Better to catch than hide

### Documentation Quality
- **Be specific** - Vague descriptions don't help
- **Include context** - What led to the situation
- **Actionable prevention** - Concrete steps to avoid
- **Keep updated** - Prevention evolves

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Executing design patterns | haiku | Pattern application, code generation |
| Reviewing implementation against spec | sonnet | Quality assurance, consistency check |
| Resolving design-execution conflicts | opus | Trade-off analysis, adaptive decisions |

## Sources

- [Blameless Post-Mortems (Google SRE)](https://sre.google/sre-book/postmortem-culture/)
- [The Five Whys](https://en.wikipedia.org/wiki/Five_whys)
- [Learning from Incidents](https://www.learningfromincidents.io/)
- [Incident Analysis Handbook](https://www.pagerduty.com/resources/learn/incident-postmortem-guide/)
- [Root Cause Analysis Methods](https://asq.org/quality-resources/root-cause-analysis)
