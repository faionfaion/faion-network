# Pattern Templates

## Pattern File Template (Full)

Use this template for patterns.md entries and detailed documentation.

```markdown
## PAT-XXX: [Pattern Name]

**Category:** [code|architecture|workflow]/[subcategory]
**Tags:** [tag1, tag2, tag3]
**Language:** [language] (if applicable)
**Framework:** [framework] (if applicable)
**Confidence:** [0.5-1.0]

### Problem

[Clear description of the problem this pattern solves]

**Symptoms:**
- [Observable symptom 1]
- [Observable symptom 2]

**Contexts:**
- [Context where this problem occurs 1]
- [Context where this problem occurs 2]

### Solution

[Brief description of the approach]

**Approach:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Code Example:**
```[language]
[Minimal working example - 20-50 lines max]
```

### Benefits

- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

### Trade-offs

- [Trade-off 1]
- [Trade-off 2]

### When to Use

- [Context 1]
- [Context 2]

### When NOT to Use

- [Anti-context 1]
- [Anti-context 2]

### Related Patterns

- [PAT-YYY: Related Pattern Name]
- [PAT-ZZZ: Another Related Pattern]

### Validation

| Metric | Value |
|--------|-------|
| Usage Count | [N] |
| Success Rate | [X%] |
| Last Used | [YYYY-MM-DD] |

### Provenance

**Discovered in:** TASK_XXX
**Verified in:** TASK_YYY, TASK_ZZZ
```

---

## Pattern File Template (Minimal)

Use for quick capture during development.

```markdown
## PAT-XXX: [Pattern Name]

**Category:** [code|architecture|workflow]/[subcategory]
**Confidence:** 0.5

**Problem:** [One sentence description]

**Solution:** [One sentence description]

```[language]
[10-20 line code example]
```

**When to Use:** [Brief context]

**Task:** TASK_XXX
```

---

## patterns.md File Template

Structure for the main patterns file.

```markdown
# Learned Patterns

Last updated: YYYY-MM-DD

## Summary

| Category | Count | Avg Confidence |
|----------|-------|----------------|
| code | X | 0.XX |
| architecture | X | 0.XX |
| workflow | X | 0.XX |

## High-Confidence Patterns (0.8+)

### PAT-001: [Name]
...

### PAT-002: [Name]
...

## Validated Patterns (0.6-0.79)

### PAT-010: [Name]
...

## Initial Patterns (0.5-0.59)

### PAT-020: [Name]
...

## Recently Used

| Pattern | Last Used | Context |
|---------|-----------|---------|
| PAT-001 | YYYY-MM-DD | TASK_XXX |
| PAT-005 | YYYY-MM-DD | TASK_YYY |
```

---

## mistakes.md File Template

Structure for anti-patterns and lessons learned.

```markdown
# Mistakes and Anti-Patterns

## Active Anti-Patterns

### ANTI-001: [Name]

**Problem:** [What went wrong]

**Symptoms:**
- [Observable symptom 1]
- [Observable symptom 2]

**Occurred in:** TASK_XXX

**Solution:**
[How to avoid or fix this]

**Related Pattern:** PAT-XXX (the correct approach)

---

## Resolved Mistakes

### RESOLVED-001: [Name]

**Problem:** [What went wrong]
**Occurred in:** TASK_XXX
**Resolution:** [How it was fixed]
**Lesson:** [What to remember]
**Date Resolved:** YYYY-MM-DD
```

---

## decisions.md File Template

Structure for architectural decision records.

```markdown
# Key Decisions

## DEC-001: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** [proposed|accepted|deprecated|superseded]

### Context

[What is the issue that we're seeing that is motivating this decision?]

### Decision

[What is the change that we're proposing/doing?]

### Consequences

**Positive:**
- [Positive consequence 1]

**Negative:**
- [Negative consequence 1]

**Risks:**
- [Risk 1]

### Related

- **Patterns:** PAT-XXX
- **Tasks:** TASK_XXX
- **Supersedes:** DEC-YYY (if applicable)
```

---

## session.md File Template

Structure for current session state.

```markdown
# Session State

Last updated: YYYY-MM-DD HH:MM

## Current Focus

**Feature:** feature-XXX-name
**Task:** TASK_XXX
**Phase:** [spec|design|impl-plan|execution|review]

## Active Patterns

Patterns loaded for this session:
- PAT-001: [Name] - [Why relevant]
- PAT-005: [Name] - [Why relevant]

## Observations

### Potential New Pattern

[Description of something that might become a pattern]

### Issue Encountered

[Description of issue and how it was resolved]

## To Review

- [ ] Consider capturing [observation] as pattern
- [ ] Update PAT-XXX with new context
- [ ] Document mistake: [brief description]
```

---

## CLAUDE.md Pattern Section Template

For syncing high-confidence patterns to project CLAUDE.md.

```markdown
## Learned Patterns

### Error Handling

**PAT-001: Async Error Boundary** (0.92)
- Wrap async with try-catch-finally
- Manage loading/error/data states
- See: `.aidocs/memory/patterns.md#PAT-001`

### API Design

**PAT-002: Response Normalization** (0.88)
- Use consistent envelope: { success, data, error, meta }
- Handle network errors uniformly
- See: `.aidocs/memory/patterns.md#PAT-002`

### Architecture

**PAT-010: Repository Pattern** (0.90)
- Abstract data access behind interface
- Enables testing with in-memory implementation
- See: `.aidocs/memory/patterns.md#PAT-010`

## Anti-Patterns

- **Silent error swallowing** - Always log or rethrow
- **Premature abstraction** - Wait for Rule of Three
- **Over-engineering** - Start simple, optimize when needed
```

---

## JSON Schema (for programmatic use)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string", "pattern": "^PAT_\\d{4}_\\d{3}$" },
    "version": { "type": "integer", "minimum": 1 },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "metadata": {
      "type": "object",
      "properties": {
        "category": { "enum": ["code", "architecture", "workflow"] },
        "subcategory": { "type": "string" },
        "language": { "type": "string" },
        "framework": { "type": "string" },
        "tags": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["category", "subcategory"]
    },
    "pattern": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "summary": { "type": "string" },
        "problem": { "type": "object" },
        "solution": { "type": "object" },
        "benefits": { "type": "array", "items": { "type": "string" } },
        "trade_offs": { "type": "array", "items": { "type": "string" } },
        "related_patterns": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["name", "problem", "solution"]
    },
    "validation": {
      "type": "object",
      "properties": {
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "usage_count": { "type": "integer", "minimum": 0 },
        "success_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "last_used": { "type": "string", "format": "date-time" }
      },
      "required": ["confidence", "usage_count", "success_rate"]
    },
    "provenance": {
      "type": "object",
      "properties": {
        "discovered_in": { "type": "string" },
        "verified_in": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["discovered_in"]
    }
  },
  "required": ["id", "metadata", "pattern", "validation", "provenance"]
}
```
