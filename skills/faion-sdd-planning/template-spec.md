# Specification Template

Copy and customize for your project specification documents.

---

## Template

```markdown
# Feature: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Project:** {project-name}

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |
| Related Feature | `features/done/{NN}-{feature}/spec.md` |

---

## Overview

{2-3 sentences describing the feature and its purpose}

---

## Problem Statement

**Who:** {User persona}
**Problem:** {What they cannot do}
**Impact:** {Business/user impact}
**Solution:** {High-level approach}
**Success Metric:** {How we measure success}

---

## User Personas

### Persona 1: {Name/Archetype}
- **Role:** {What they do}
- **Goal:** {What they want}
- **Pain Points:** {Current frustrations}
- **Context:** {When/where they use product}

---

## User Stories

### US-001: {Story Title}
**As a** {persona}
**I want to** {action}
**So that** {benefit}

**Priority:** Must | Should | Could
**Acceptance Criteria:** AC-001

### US-002: {Story Title}
...

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL {requirement} | US-001 | Must |
| FR-002 | System SHALL {requirement} | US-001 | Must |
| FR-003 | System SHOULD {requirement} | US-002 | Should |

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Security | Password storage | bcrypt 12 rounds | Must |

---

## Acceptance Criteria

### AC-001: {Scenario Title}

**Scenario:** {Brief description}

**Given:** {precondition}
**And:** {additional precondition}
**When:** {action}
**Then:** {expected result}
**And:** {additional result}

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| {Feature} | {Why excluded} | {Future phase or Never} |

---

## Assumptions & Constraints

### Assumptions
- {Assumption 1}
- {Assumption 2}

### Constraints
- {Technical constraint}
- {Business constraint}

---

## Dependencies

### Internal
- {Other feature this depends on}

### External
- {Third-party service}
```

---

## Usage Notes

### When to Use
- Starting a new feature
- Defining WHAT and WHY before HOW
- Communicating with stakeholders

### What to Include
- Clear problem statement
- User personas and stories
- Functional and non-functional requirements
- Acceptance criteria (testable)
- Scope boundaries (out of scope)

### What NOT to Include
- Implementation details (goes in design.md)
- Code snippets (goes in tasks)
- Time estimates (use token estimates)

### Next Steps
After spec is approved:
1. Write design.md (HOW to implement)
2. Create implementation-plan.md (task breakdown)
3. Generate TASK_*.md files

---

## Related

- **Design template:** [template-design.md](template-design.md)
- **Task template:** [template-task.md](template-task.md)
- **Workflow guide:** [writing-specifications.md](writing-specifications.md)
- **AI assistance:** [ai-assisted-specification-writing.md](ai-assisted-specification-writing.md)

---

*SDD Specification Template v2.0*
