# TASK_XXX: Research — {Topic}

| Field | Value |
|-------|-------|
| **Complexity** | simple |
| **Est. Tokens** | ~{X}k |
| **Type** | research |
| **Depends on** | {TASK-YYY or "none"} |
| **Blocks** | {TASK-ZZZ (execution task that needs this ADR)} |

## Description

Investigate {topic} to produce an Architecture Decision Record and a refined list of implementation tasks. Research tasks do not produce production code — they produce decisions that unblock execution tasks.

**Scope:** {What to investigate — options, trade-offs, constraints, proof-of-concept limits}

**Out of scope:** {What not to investigate}

## Research Questions

1. {Question 1 — concrete, answerable}
2. {Question 2}
3. {Question 3}

## Acceptance Criteria

**AC-1: ADR produced**
- Given: research questions are answered
- When: task completes
- Then: an ADR file exists at `.aidocs/{status}/{feature}/adr-XXX-{topic}.md` with context, decision, and consequences sections

**AC-2: Execution tasks updated**
- Given: ADR decision is recorded
- When: task completes
- Then: dependent execution tasks in `todo/` reflect the chosen approach in their Files to Change and Description sections

## Output Files

| Action | File | Description |
|--------|------|-------------|
| CREATE | `.aidocs/{status}/{feature}/adr-XXX-{topic}.md` | Architecture Decision Record |
| MODIFY | `todo/TASK_YYY-*.md` | Update with chosen approach |

## ADR Template (fill and save)

```markdown
# ADR-XXX: {Decision title}

**Status:** Accepted
**Date:** {YYYY-MM-DD}

## Context

{What problem we are solving, constraints, options considered}

## Decision

{What we decided and why}

## Consequences

**Good:** {benefits}
**Bad:** {trade-offs}
**Neutral:** {observations}
```

## Summary
<!-- Filled after completion -->
