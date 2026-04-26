# SDD Workflow Templates

## Purpose

Copy-paste templates for SDD artifacts. Customize for your project.

---

## Template 1: Constitution

```markdown
# Constitution: [Project Name]

## Overview

| Field | Value |
|-------|-------|
| Project | [Name] |
| Type | [Web App / API / CLI / Library] |
| Status | [Planning / Active / Maintenance] |

---

## Technology Stack

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | [React / Vue / Svelte / Next.js] |
| Language | [TypeScript / JavaScript] |
| Styling | [Tailwind / CSS Modules / Styled Components] |
| State | [Zustand / Redux / Context] |

### Backend
| Component | Technology |
|-----------|------------|
| Framework | [FastAPI / Django / Express / Go] |
| Language | [Python / TypeScript / Go] |
| Database | [PostgreSQL / SQLite / MongoDB] |
| ORM | [Prisma / SQLAlchemy / GORM] |

### Infrastructure
| Component | Technology |
|-----------|------------|
| Hosting | [Vercel / AWS / GCP] |
| CI/CD | [GitHub Actions / GitLab CI] |
| Monitoring | [Datadog / Prometheus] |

---

## Coding Standards

### General
- [ ] Use TypeScript strict mode
- [ ] 100 character line limit
- [ ] Prefer named exports
- [ ] No `any` types without justification

### Testing
- Minimum coverage: [X]%
- Unit tests: Required for business logic
- Integration tests: Required for API endpoints
- E2E tests: Required for critical user flows

### Git
- Commit format: `type: description`
- Branch naming: `feature/xxx`, `fix/xxx`, `docs/xxx`
- PR reviews: Required before merge

---

## Architecture Principles

1. **[Principle Name]**: [Description]
2. **[Principle Name]**: [Description]
3. **[Principle Name]**: [Description]

---

## Quality Thresholds

| Metric | Threshold |
|--------|-----------|
| Test coverage | [X]% |
| Build time | < [X] min |
| Page load | < [X] sec |
| API response | < [X] ms |

---

*Last updated: [Date]*
```

---

## Template 2: Specification

```markdown
# Specification: [Feature Name]

## Metadata

| Field | Value |
|-------|-------|
| Feature ID | [XXX] |
| Status | [Draft / Review / Approved] |
| Author | [Name] |
| Created | [Date] |

---

## Problem Statement

### Context
[Describe the current situation and why change is needed]

### Problem
[Specific problem being solved]

### Impact
[What happens if we don't solve this?]

---

## User Personas

### Persona 1: [Name]
- **Role**: [Description]
- **Goals**: [What they want to achieve]
- **Pain points**: [Current frustrations]

---

## Functional Requirements

### FR-1: [Requirement Title]

[Description of the requirement]

**Acceptance Criteria:**
- **AC-1.1:** Given [context], when [action], then [expected result]
- **AC-1.2:** Given [context], when [action], then [expected result]

### FR-2: [Requirement Title]

[Description]

**Acceptance Criteria:**
- **AC-2.1:** Given [context], when [action], then [expected result]

---

## Non-Functional Requirements

### NFR-1: Performance
- Page load time < [X] seconds
- API response time < [X] ms
- Support [X] concurrent users

### NFR-2: Security
- [Authentication requirement]
- [Authorization requirement]
- [Data protection requirement]

### NFR-3: Accessibility
- WCAG [2.0/2.1] Level [A/AA/AAA]
- Screen reader compatible
- Keyboard navigation

---

## Scope

### In Scope (MVP)
- [Feature/capability 1]
- [Feature/capability 2]
- [Feature/capability 3]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

### Future Considerations (MLP)
- [Potential future enhancement 1]
- [Potential future enhancement 2]

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| [External API] | External | Available |
| [Feature X] | Internal | In Progress |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| [Metric 1] | [Target] | [How measured] |
| [Metric 2] | [Target] | [How measured] |

---

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

---

*Specification | [Feature Name] | Version [X.X]*
```

---

## Template 3: Design Document

```markdown
# Design Document: [Feature Name]

## Metadata

| Field | Value |
|-------|-------|
| Feature ID | [XXX] |
| Spec Reference | [Link to spec.md] |
| Status | [Draft / Review / Approved] |
| Author | [Name] |

---

## Overview

[Brief summary of the technical approach]

---

## Architecture Decisions

### AD-1: [Decision Title]

**Context:**
[What is the issue that we're seeing that is motivating this decision?]

**Decision:**
[What is the change that we're proposing and/or doing?]

**Rationale:**
[Why is this the best choice?]

**Alternatives Considered:**
1. [Alternative 1] - [Why rejected]
2. [Alternative 2] - [Why rejected]

**Consequences:**
- [Positive consequence]
- [Negative consequence / trade-off]

---

### AD-2: [Decision Title]

[Same structure as AD-1]

---

## System Design

### Component Diagram

```
[Component A] --> [Component B] --> [Component C]
       |                                  |
       v                                  v
[Database]                         [External API]
```

### Data Flow

```
1. User action
2. Frontend sends request
3. Backend processes
4. Database updated
5. Response returned
```

---

## File Structure

```
src/
├── [folder]/
│   ├── [file].ts          # [Purpose]
│   └── [file].ts          # [Purpose]
├── [folder]/
│   ├── [file].ts          # [Purpose]
│   └── [file].ts          # [Purpose]
└── [folder]/
    └── [file].ts          # [Purpose]
```

---

## Data Models

### [Entity Name]

```typescript
interface [EntityName] {
  id: string;
  [field]: [type];
  [field]: [type];
  createdAt: Date;
  updatedAt: Date;
}
```

### Database Schema

```sql
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [column] [TYPE] [CONSTRAINTS],
  [column] [TYPE] [CONSTRAINTS],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## API Contracts

### [Endpoint Name]

```
[METHOD] /api/[path]
```

**Request:**
```json
{
  "[field]": "[type]"
}
```

**Response (200):**
```json
{
  "[field]": "[type]"
}
```

**Errors:**
| Code | Meaning |
|------|---------|
| 400 | [Description] |
| 401 | [Description] |
| 404 | [Description] |

---

## Integration Points

| System | Type | Protocol | Notes |
|--------|------|----------|-------|
| [System] | [Internal/External] | [REST/GraphQL/gRPC] | [Notes] |

---

## Security Considerations

- [ ] [Security consideration 1]
- [ ] [Security consideration 2]
- [ ] [Security consideration 3]

---

## Testing Strategy

| Layer | Approach | Coverage Target |
|-------|----------|-----------------|
| Unit | [Approach] | [X]% |
| Integration | [Approach] | [X]% |
| E2E | [Approach] | Critical paths |

---

## Traceability

| Requirement | Design Component |
|-------------|-----------------|
| FR-1 | AD-1, [File] |
| FR-2 | AD-2, [File] |

---

*Design Document | [Feature Name] | Version [X.X]*
```

---

## Template 4: Implementation Plan

```markdown
# Implementation Plan: [Feature Name]

## Metadata

| Field | Value |
|-------|-------|
| Feature ID | [XXX] |
| Design Reference | [Link to design.md] |
| Total Tasks | [N] |
| Parallelization | [X] waves |

---

## Dependency Graph

```
TASK-001 ─┬─> TASK-003 ─┬─> TASK-005
          │             │
TASK-002 ─┘             └─> TASK-006
                             │
                    TASK-004 ┘
```

---

## Wave 1: [Wave Name]

*No dependencies. Can execute in parallel.*

| Task ID | Title | Complexity | References |
|---------|-------|------------|------------|
| TASK-001 | [Title] | [Low/Med/High] | FR-1, AD-1 |
| TASK-002 | [Title] | [Low/Med/High] | FR-2 |

---

## Wave 2: [Wave Name]

*Depends on: Wave 1 completion*

| Task ID | Title | Complexity | Dependencies |
|---------|-------|------------|--------------|
| TASK-003 | [Title] | [Low/Med/High] | TASK-001, TASK-002 |
| TASK-004 | [Title] | [Low/Med/High] | TASK-002 |

---

## Wave 3: [Wave Name]

*Depends on: TASK-003, TASK-004*

| Task ID | Title | Complexity | Dependencies |
|---------|-------|------------|--------------|
| TASK-005 | [Title] | [Low/Med/High] | TASK-003 |
| TASK-006 | [Title] | [Low/Med/High] | TASK-003, TASK-004 |

---

## Quality Gates

| After Wave | Gate Level | Validation |
|------------|------------|------------|
| Wave 1 | L4 | Unit tests pass |
| Wave 2 | L5 | Integration tests pass |
| Wave 3 | L6 | All AC verified |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [Mitigation] |
| [Risk 2] | [High/Med/Low] | [Mitigation] |

---

*Implementation Plan | [Feature Name] | Version [X.X]*
```

---

## Template 5: Task File

```markdown
# TASK-[XXX]: [Title]

## Metadata

| Field | Value |
|-------|-------|
| Status | [todo / in-progress / done] |
| Complexity | [Low / Medium / High] |
| Est. Tokens | ~[X]k |

---

## SDD References

| Document | Section |
|----------|---------|
| Spec | [Link] FR-[X] |
| Design | [Link] AD-[X] |
| Impl Plan | [Link] Wave [X] |

---

## Dependencies

| Type | Task | Status |
|------|------|--------|
| Blocked by | TASK-[XXX] | [Status] |
| Blocks | TASK-[XXX] | - |

---

## Description

[Detailed description of what needs to be done]

---

## Acceptance Criteria

- [ ] AC-1: [Criterion from spec]
- [ ] AC-2: [Criterion from spec]

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | [path] | [Brief description] |
| MODIFY | [path] | [Brief description] |

---

## Implementation Notes

[Any specific guidance, patterns to follow, or gotchas]

---

## Testing Requirements

- [ ] Unit test: [Description]
- [ ] Integration test: [Description]

---

## Summary

*Fill after completion*

### Completed
- [What was done]

### Changes Made
- CREATE: [file]
- MODIFY: [file]

### Tests Added
- [Test description]

### Lessons Learned
- [Pattern discovered]
- [Mistake avoided]

---

*Task | [Feature Name] | Created [Date]*
```

---

## Template 6: 15-Minute Waterfall (Quick Spec)

```markdown
# Quick Spec: [Feature/Task Name]

## Problem (2 min)
[What problem are we solving? Who has it?]

## Requirements (5 min)
- [ ] R1: [Requirement]
- [ ] R2: [Requirement]
- [ ] R3: [Requirement]

## Design Sketch (5 min)
- Files: [List files to create/modify]
- Approach: [Brief technical approach]

## Tasks (3 min)
1. [ ] [Task 1]
2. [ ] [Task 2]
3. [ ] [Task 3]

## Done When
- [Acceptance criterion 1]
- [Acceptance criterion 2]
```

---

## Template 7: Memory Files

### patterns.md

```markdown
# Patterns Learned

## [Date]: [Pattern Name]
**Context:** [When this applies]
**Pattern:** [What to do]
**Example:**
```code
[Example code or structure]
```

---
```

### mistakes.md

```markdown
# Mistakes Log

## [Date]: [Mistake Title]
**What happened:** [Description]
**Root cause:** [Why it happened]
**Fix:** [How to avoid]
**Related:** TASK-[XXX]

---
```

### decisions.md

```markdown
# Key Decisions

## [Date]: [Decision Title]
**Context:** [Situation]
**Decision:** [What we decided]
**Rationale:** [Why]
**Revisit if:** [Conditions that would change this]

---
```

---

*Templates | SDD Foundation | Version 1.0*
