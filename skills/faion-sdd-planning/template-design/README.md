# Design Document Template

Copy and customize for your project design documents.

---

## Template

```markdown
# Design: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Spec:** {link to spec.md}

---

## Reference Documents

| Document | Path |
|----------|------|
| Specification | `spec.md` |
| Constitution | `.aidocs/constitution.md` |
| Contracts | `.aidocs/contracts.md` |

---

## Overview

{2-3 sentences: technical approach summary}

---

## Architecture Decisions

### AD-1: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

### AD-2: {Decision Name}
...

---

## Components

### Component 1: {Name}
- **Purpose:** {what it does}
- **Location:** {path}
- **Dependencies:** {what it uses}

```
[Diagram if complex]
```

---

## Data Flow

```
{Component A} → {Component B} → {Component C}
       ↓              ↓              ↓
   validate       process        persist
```

---

## Data Models

### {Model Name}
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| {field} | {type} | {constraints} | {description} |

---

## API Endpoints

Reference: `contracts.md` section {X}

| Method | Path | Description | FR |
|--------|------|-------------|-----|
| POST | /api/v1/{resource} | Create | FR-001 |
| GET | /api/v1/{resource}/{id} | Read | FR-002 |

---

## Files

| File | Action | Description |
|------|--------|-------------|
| {path/to/file.py} | CREATE | {what to create} |
| {path/to/file.py} | MODIFY | {what to modify} |

---

## Testing Strategy

### Unit Tests
| Component | Test File | Coverage |
|-----------|-----------|----------|
| {component} | test_{component}.py | {target}% |

### Integration Tests
| Flow | Test File | Description |
|------|-----------|-------------|
| {flow} | test_{flow}_integration.py | {description} |

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {risk} | High/Med/Low | High/Med/Low | {mitigation} |

---

## FR Coverage

| FR | AD | Files | Status |
|----|-----|-------|--------|
| FR-001 | AD-1 | models.py, services.py | Covered |
| FR-002 | AD-2 | views.py | Covered |
```

---

## Usage Notes

### When to Use
- After spec.md is approved
- Before writing implementation-plan.md
- Defining HOW to implement WHAT

### What to Include
- Architecture decisions (ADRs)
- Component breakdown
- Data models and API endpoints
- File changes (CREATE/MODIFY/DELETE)
- Testing strategy
- Risk analysis

### What NOT to Include
- Requirements (already in spec.md)
- Task breakdown (goes in implementation-plan.md)
- Code snippets (goes in tasks)

### Design Patterns
See [design-docs-patterns.md](design-docs-patterns.md) for:
- Component design patterns
- Data flow patterns
- API design patterns
- Big Tech patterns (Google, Meta, etc.)

### Next Steps
After design is approved:
1. Write implementation-plan.md (task breakdown)
2. Generate TASK_*.md files
3. Execute tasks

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |
## Related

- **Spec template:** [template-spec.md](template-spec.md)
- **Task template:** [template-task.md](template-task.md)
- **Workflow guide:** [design-doc-structure.md](design-doc-structure.md)
- **Design patterns:** [design-docs-patterns.md](design-docs-patterns.md)
- **Big Tech patterns:** [design-docs-patterns-big-tech.md](design-docs-patterns-big-tech.md)
- **ADR guide:** [architecture-decision-records.md](architecture-decision-records.md)

---

*SDD Design Template v2.0*
