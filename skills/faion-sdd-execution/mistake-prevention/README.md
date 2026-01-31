---
id: mistake-prevention
name: "Mistake Prevention"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Mistake Prevention

## Overview

Mistake prevention transforms documented errors into automated checks, warnings, and process improvements. The goal is to catch potential issues before they occur through proactive detection systems and pre-task warnings.

## When to Use

- Before starting any new task
- When setting up automation rules
- During pre-deployment checks
- For creating checklists
- When configuring CI/CD pipelines
- For onboarding (teaching what to avoid)

## Prevention Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Prevention System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │  Detection  │ →  │   Warning   │ →  │ Automation  │    │
│  │   Rules     │    │   System    │    │   Checks    │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│  Pattern          Pre-task           CI/CD                │
│  Matching         Warnings           Guards               │
│  Context          Context             Blocks              │
│  Analysis         Suggestions                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Prevention Rules

**Rule Schema:**
```json
{
  "rules": [
    {
      "id": "PREV_001",
      "source_mistake": "MIS_2024_001",
      "trigger": "file_contains_pattern",
      "pattern": "DROP (TABLE|COLUMN)",
      "file_types": ["*.sql", "migrations/*"],
      "action": "warn",
      "message": "Destructive migration detected. Ensure backup exists. See MIS_2024_001."
    },
    {
      "id": "PREV_002",
      "source_mistake": "MIS_2024_005",
      "trigger": "task_type",
      "task_type": "database_migration",
      "action": "require_checklist",
      "checklist": "database-migration-checklist"
    },
    {
      "id": "PREV_003",
      "source_mistake": "MIS_2024_010",
      "trigger": "estimate_context",
      "context_keywords": ["api integration", "third-party"],
      "action": "suggest",
      "message": "Consider spike first. Past integrations took 2x estimated. See MIS_2024_010."
    }
  ]
}
```

## Pre-Task Warning System

**Warning Generation:**
```python
def get_warnings_for_task(task: Task) -> List[Warning]:
    """Get relevant warnings before starting a task"""

    warnings = []
    mistakes = load_mistakes()

    # Match by category
    category_mistakes = [m for m in mistakes
                        if m.metadata.category in task.categories]

    # Match by keywords
    keyword_mistakes = find_mistakes_by_keywords(
        extract_keywords(task.description)
    )

    # Match by similar past tasks
    similar_task_mistakes = find_mistakes_from_similar_tasks(task)

    all_relevant = set(category_mistakes + keyword_mistakes + similar_task_mistakes)

    for mistake in all_relevant:
        warnings.append(Warning(
            severity=mistake.metadata.severity,
            title=f"Watch out: {mistake.title}",
            description=mistake.summary,
            prevention=mistake.prevention.immediate_actions,
            source=mistake.id
        ))

    return sorted(warnings, key=lambda w: severity_order(w.severity))
```

**Warning Display:**
```yaml
pre_task_warnings:
  task: "TASK_042_database_schema_migration"
  warnings:
    - severity: high
      title: "Watch out: Database Migration Without Backup"
      message: "Similar migrations in MIS_2024_001 led to data loss"
      checklist: "database-migration-checklist"
      actions:
        - "Take full backup before schema changes"
        - "Test rollback procedure"
        - "Run in staging first"

    - severity: medium
      title: "Watch out: Production Config Mismatch"
      message: "Past migrations failed due to environment differences (MIS_2024_008)"
      actions:
        - "Verify config matches production"
        - "Check dependency versions"
```

## Automated Prevention Checks

**CI/CD Integration:**
```yaml
prevention_checks:
  pre_commit:
    - check: "hardcoded_secrets"
      pattern: "(api_key|password|secret)\\s*=\\s*['\"][^'\"]+['\"]"
      action: block
      message: "Hardcoded secret detected. Use environment variables."
      source: "MIS_2023_045"

    - check: "console_log_production"
      pattern: "console\\.log\\("
      files: "src/**/*.js"
      action: warn
      message: "Console.log found. Consider using logger."
      source: "MIS_2024_022"

  pre_deploy:
    - check: "migration_backup"
      trigger: "files_changed"
      pattern: "migrations/*"
      action: require_confirmation
      message: "Database migration detected. Backup created?"
      source: "MIS_2024_001"

    - check: "test_coverage"
      trigger: "coverage_check"
      threshold: 80
      action: block_if_below
      message: "Test coverage below 80%. Add tests."
      source: "MIS_2024_015"

  post_deploy:
    - check: "health_check"
      trigger: "deployment_complete"
      endpoint: "/health"
      timeout: 30
      action: rollback_if_fail
      message: "Health check failed. Rolling back."
      source: "MIS_2024_030"
```

**Pattern Detection:**
```python
def detect_anti_patterns(code: str, language: str) -> List[Detection]:
    """Detect known anti-patterns in code"""

    detections = []
    rules = load_prevention_rules()

    for rule in rules:
        if rule.trigger == "file_contains_pattern":
            matches = re.finditer(rule.pattern, code)
            for match in matches:
                detections.append(Detection(
                    rule_id=rule.id,
                    line=get_line_number(code, match.start()),
                    message=rule.message,
                    severity=rule.severity,
                    source_mistake=rule.source_mistake,
                    suggestion=rule.suggestion
                ))

    return detections
```

## Checklist Generation

**From Mistakes to Checklists:**
```python
def generate_checklist_from_mistakes(category: str) -> Checklist:
    """Generate checklist from category mistakes"""

    mistakes = load_mistakes_by_category(category)
    checklist_items = []

    for mistake in mistakes:
        for addition in mistake.checklist_additions:
            if addition["checklist"] == category:
                checklist_items.append({
                    "item": addition["item"],
                    "position": addition["position"],
                    "source": mistake.id,
                    "severity": mistake.metadata.severity
                })

    # Sort by position and severity
    sorted_items = sort_checklist_items(checklist_items)

    return Checklist(
        id=f"{category}-checklist",
        title=f"{category.title()} Checklist",
        items=sorted_items,
        generated_from=len(mistakes),
        last_updated=datetime.now()
    )
```

**Example Checklist:**
```markdown
## Database Migration Checklist

Generated from 5 documented mistakes

### Before Migration
- [ ] Full backup created and verified (MIS_2024_001)
- [ ] Migration tested in staging (MIS_2024_008)
- [ ] Rollback procedure documented (MIS_2024_001)
- [ ] Team notified of maintenance window (MIS_2024_012)
- [ ] Monitoring alerts configured (MIS_2024_030)

### During Migration
- [ ] Migration script reviewed by peer (MIS_2024_005)
- [ ] Lock timeout set (prevent long locks) (MIS_2024_018)
- [ ] Progress monitoring enabled (MIS_2024_025)

### After Migration
- [ ] Data integrity check passed (MIS_2024_001)
- [ ] Application health check passed (MIS_2024_030)
- [ ] Performance metrics normal (MIS_2024_042)
- [ ] Backup can be deleted (after 7 days)
```

## Context-Aware Suggestions

**Task Analysis:**
```python
def suggest_precautions(task: Task) -> List[Suggestion]:
    """Analyze task and suggest precautions"""

    suggestions = []

    # Technology stack analysis
    stack_mistakes = find_mistakes_by_tech_stack(task.tech_stack)
    if stack_mistakes:
        suggestions.append(Suggestion(
            type="tech_stack",
            message=f"Found {len(stack_mistakes)} past issues with {task.tech_stack}",
            actions=[m.prevention.immediate_actions for m in stack_mistakes]
        ))

    # Complexity analysis
    if task.estimated_tokens > 80000:
        suggestions.append(Suggestion(
            type="complexity",
            message="High complexity task. Consider splitting.",
            reference="MIS_2024_035"
        ))

    # Dependency analysis
    if "third-party" in task.tags:
        suggestions.append(Suggestion(
            type="dependencies",
            message="Third-party integration. Past tasks took 2x longer.",
            reference="MIS_2024_010"
        ))

    return suggestions
```

## Automation Strategies

**Prevention Automation Levels:**

| Level | Description | Example |
|-------|-------------|---------|
| L1 - Detect | Pattern matching | Find hardcoded secrets |
| L2 - Warn | Show warning | Alert on console.log |
| L3 - Suggest | Offer alternatives | Suggest logger instead |
| L4 - Block | Prevent action | Block commit with secrets |
| L5 - Auto-fix | Fix automatically | Remove trailing whitespace |
| L6 - Require | Mandate checklist | Require backup confirmation |

**Implementation:**
```python
def apply_prevention_automation(mistake: Mistake) -> List[Automation]:
    """Generate automation from mistake"""

    automations = []

    # L1: Detection rules
    if mistake.prevention.automation:
        for auto in mistake.prevention.automation:
            if "detect" in auto.lower():
                automations.append(create_detection_rule(mistake, auto))

    # L4: Blocking rules
    if mistake.metadata.severity == "critical":
        automations.append(create_blocking_rule(mistake))

    # L6: Checklist requirements
    if mistake.checklist_additions:
        automations.append(create_checklist_requirement(mistake))

    return automations
```

## Prevention Effectiveness Tracking

**Effectiveness Metrics:**
```yaml
prevention_effectiveness:
  PREV_001:
    rule: "Backup before migration"
    triggered: 15
    prevented: 14
    occurred: 1
    effectiveness: 93%
    last_30_days:
      triggered: 3
      prevented: 3

  PREV_003:
    rule: "Integration estimation warning"
    triggered: 8
    heeded: 6
    ignored: 2
    avg_saved_time: "4 hours"
    effectiveness: 75%
```

**Improvement Loop:**
```python
def review_prevention_effectiveness():
    """Review and improve prevention rules"""

    rules = load_prevention_rules()
    stats = load_prevention_stats()

    for rule in rules:
        effectiveness = calculate_effectiveness(rule, stats)

        if effectiveness < 0.5:
            # Rule not effective, needs improvement
            improve_or_retire_rule(rule)

        elif effectiveness > 0.9:
            # Very effective, consider expanding
            expand_rule_coverage(rule)

        elif rule.triggered_count == 0:
            # Never triggered, might be too specific
            review_rule_relevance(rule)
```

## Prevention Focus

1. **Automate where possible** - Reduce human error
2. **Multiple layers** - Defense in depth
3. **Regular review** - Are preventions working?
4. **Low friction** - Easy to follow

## Templates

### Prevention Rule Template

```json
{
  "id": "PREV_XXX",
  "source_mistake": "MIS_YYYY_ZZZ",
  "trigger": "[file_contains_pattern|task_type|estimate_context|deployment]",
  "pattern": "[regex pattern]",
  "file_types": ["*.ext"],
  "action": "[warn|block|require_checklist|suggest]",
  "message": "[Human-readable message with context]",
  "severity": "[critical|high|medium|low]"
}
```

### Pre-Task Warning Template

```markdown
## Pre-Task Warnings: [TASK_ID]

### High Severity
- **[Warning Title]** (from [MIS_ID])
  - [Description]
  - Actions:
    - [ ] [Action 1]
    - [ ] [Action 2]

### Medium Severity
- **[Warning Title]** (from [MIS_ID])
  - [Description]
  - Suggestion: [Suggestion]
```

## References

- [mistake-tracking: Mistake Tracking](./mistake-tracking.md)
- [quality-gates: Quality Gates](./quality-gates.md)
- [confidence-checks: Confidence Checks](./confidence-checks.md)
- [reflexion-learning: Reflexion Learning](./reflexion-learning.md)
- [pattern-memory: Pattern Memory](./pattern-memory.md)
