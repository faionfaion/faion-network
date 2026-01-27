# Memory Templates

Templates for SDD learning system. Patterns, mistakes, decisions, and session state.

---

## Overview

Memory files enable continuous learning across sessions:

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `patterns.md` | Successful approaches to reuse | After each task |
| `mistakes.md` | Errors to avoid | When mistakes occur |
| `decisions.md` | Key decisions with context | When decisions made |
| `session.md` | Current session state | During work |

**Location:** `.aidocs/memory/`

---

## patterns.md Template

```markdown
---
version: "1.0"
updated: YYYY-MM-DD
project: {project-name}
---

# Learned Patterns

## Development Patterns

### PAT-001: {Pattern Name}

| Attribute | Value |
|-----------|-------|
| Category | {development/testing/architecture/workflow} |
| Context | {when to apply} |
| Discovered | YYYY-MM-DD |
| Task | TASK-{NNN} |
| Success Count | {N} |

**Description:**
{What worked and why}

**Example:**
```{language}
{code example}
```

**Tags:** `{tag1}`, `{tag2}`, `{tag3}`

---

### PAT-002: {Pattern Name}

{Repeat format}

---

## Testing Patterns

### PAT-010: {Pattern Name}

{Testing-specific patterns}

---

## Architecture Patterns

### PAT-020: {Pattern Name}

{Architecture-specific patterns}

---

## Workflow Patterns

### PAT-030: {Pattern Name}

{Process-specific patterns}

---

## Pattern Index

| ID | Name | Category | Tags |
|----|------|----------|------|
| PAT-001 | {name} | Development | {tags} |
| PAT-002 | {name} | Development | {tags} |
| PAT-010 | {name} | Testing | {tags} |
```

---

## mistakes.md Template

```markdown
---
version: "1.0"
updated: YYYY-MM-DD
project: {project-name}
---

# Recorded Mistakes

## Recent Mistakes

### ERR-001: {Short Description}

| Attribute | Value |
|-----------|-------|
| Category | {validation/integration/logic/config/security} |
| Severity | {critical/high/medium/low} |
| Occurred | YYYY-MM-DD |
| Task | TASK-{NNN} |
| Occurrence Count | {N} |

**What Happened:**
{Description of the error}

**Root Cause:**
{Why it happened}

**Solution:**
```{language}
{fix or correct approach}
```

**Prevention:**
{How to avoid in future}

**Tags:** `{tag1}`, `{tag2}`

---

### ERR-002: {Short Description}

{Repeat format}

---

## Common Mistakes by Category

### Validation Errors

| ID | Description | Prevention |
|----|-------------|------------|
| ERR-001 | {summary} | {quick prevention} |

### Integration Errors

| ID | Description | Prevention |
|----|-------------|------------|
| ERR-010 | {summary} | {quick prevention} |

### Configuration Errors

| ID | Description | Prevention |
|----|-------------|------------|
| ERR-020 | {summary} | {quick prevention} |

---

## Mistake Checklist

Before completing a task, verify:

- [ ] {Common mistake 1 check}
- [ ] {Common mistake 2 check}
- [ ] {Common mistake 3 check}
```

---

## decisions.md Template

```markdown
---
version: "1.0"
updated: YYYY-MM-DD
project: {project-name}
---

# Key Decisions

## Recent Decisions

### DEC-001: {Decision Title}

| Attribute | Value |
|-----------|-------|
| Date | YYYY-MM-DD |
| Status | Active / Superseded by DEC-XXX |
| Category | {architecture/technology/process/business} |
| Impact | {high/medium/low} |
| Reversibility | {easy/moderate/difficult} |

**Context:**
{What prompted this decision}

**Decision:**
{What was decided}

**Rationale:**
{Why this choice}

**Alternatives Rejected:**
- {Alternative 1}: {why not}
- {Alternative 2}: {why not}

**Consequences:**
- Positive: {benefits}
- Negative: {trade-offs}

**Related:**
- ADR: {link to design doc ADR if applicable}
- Task: TASK-{NNN}

---

### DEC-002: {Decision Title}

{Repeat format}

---

## Decisions by Category

### Architecture

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-001 | {summary} | YYYY-MM-DD | Active |

### Technology

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-010 | {summary} | YYYY-MM-DD | Active |

### Process

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-020 | {summary} | YYYY-MM-DD | Active |
```

---

## session.md Template

```markdown
---
version: "1.0"
updated: YYYY-MM-DDTHH:MM:SSZ
project: {project-name}
---

# Session State

## Current Work

| Attribute | Value |
|-----------|-------|
| Feature | feature-{NNN}-{name} |
| Task | TASK-{NNN} |
| Status | {in-progress/blocked/reviewing} |
| Started | YYYY-MM-DDTHH:MM:SSZ |

---

## Progress

### Completed This Session

- [x] {completed item 1}
- [x] {completed item 2}

### In Progress

- [ ] {current item}

### Pending

- [ ] {next item 1}
- [ ] {next item 2}

---

## Context

### Files Being Modified

| File | Status | Notes |
|------|--------|-------|
| `{path}` | Modified | {what changed} |
| `{path}` | Created | {what it contains} |

### Key Information

- {Important context 1}
- {Important context 2}

---

## Blockers

| Blocker | Since | Waiting On |
|---------|-------|------------|
| {blocker} | YYYY-MM-DD | {what's needed} |

---

## Notes

{Free-form notes for session continuity}

---

## Resume Instructions

To continue this work:
1. {Step 1}
2. {Step 2}
3. {Step 3}

---

*Session last updated: YYYY-MM-DDTHH:MM:SSZ*
```

---

## JSON Format (Alternative)

For machine processing, patterns and mistakes can also use JSON:

### Pattern Record (JSON)

```json
{
  "id": "PAT-001",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "category": "{category}",
  "name": "{pattern name}",
  "description": "{what worked}",
  "context": "{when to use}",
  "code_example": "{code snippet}",
  "success_count": 1,
  "tags": ["tag1", "tag2"]
}
```

### Mistake Record (JSON)

```json
{
  "id": "ERR-001",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "category": "{category}",
  "severity": "{severity}",
  "description": "{what went wrong}",
  "root_cause": "{why it happened}",
  "solution": "{how to fix}",
  "prevention": "{how to prevent}",
  "occurrence_count": 1,
  "tags": ["tag1", "tag2"]
}
```

---

## Usage Notes

### When to Update

| Event | Update |
|-------|--------|
| Task completed successfully | Add pattern if reusable approach found |
| Error occurred | Add mistake with prevention |
| Significant choice made | Add decision with context |
| Starting/ending session | Update session state |

### Memory Hygiene

- **Merge duplicates**: Similar patterns/mistakes should be consolidated
- **Archive old entries**: Move stale entries to archive section
- **Review periodically**: Clean up irrelevant entries monthly
- **Tag consistently**: Use consistent tags for searchability

### Cross-Project Learning

For patterns that apply across projects:
1. Record in project memory first
2. If validated multiple times, promote to skill methodology
3. Reference skill methodology from project memory

### Privacy Considerations

- Don't include sensitive data in memory files
- No credentials, API keys, or PII
- Memory files may be version-controlled
