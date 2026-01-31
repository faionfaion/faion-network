# Design Document Structure

## What is a Design Document?

A design document answers: **"HOW are we building this?"**

It bridges the gap between specification (what) and implementation (code).

## Document Hierarchy

```
CONSTITUTION (project-wide)
    ↓ informs
SPEC (feature-specific) → DESIGN (feature-specific) → IMPL PLAN → TASKS
    FR-X requirements     ↓ implements               ↓ breaks down
                         AD-X decisions              TASK-XXX
```

## Design vs Spec vs Implementation Plan

| Aspect | Specification | Design | Implementation Plan |
|--------|---------------|--------|---------------------|
| Question | What to build? | How to build it? | In what order? |
| Audience | Stakeholders, PMs | Developers | Developers, AI agents |
| Content | Requirements, AC | Architecture, APIs | Tasks, estimates |
| Changes | Needs approval | Technical decision | May adjust during dev |
| Output | FR-X, NFR-X | AD-X, file list | TASK-XXX list |

## Design Document Structure v2.0

```markdown
# Design: [Feature Name]

## Reference Documents
[Links to spec, constitution, related designs]

## Overview
[Brief summary of technical approach]

## Spec Coverage
[FR-X → AD-X traceability matrix]

## Architectural Decisions
[AD-X with rationale, alternatives, consequences]

## File Structure
[What files to create/modify with patterns]

## Data Models
[Database schemas, TypeScript types]

## API Contracts
[Endpoints with OpenAPI-style documentation]

## Component Design (if frontend)
[React/Vue components, state management]

## Dependencies
[Libraries, services, infrastructure]

## Security Considerations
[Auth, validation, encryption]

## Performance Considerations
[Caching, optimization, scaling]

## Testing Strategy
[Unit, integration, E2E approach]

## Migration Strategy (if applicable)
[Data migration, backwards compatibility]

## Recommended Skills & Methodologies
[For implementation phase]
```

---

## Full Design Template v2.0

```markdown
# Design: [Feature Name]

**Version:** 1.0
**Spec:** `{FEATURE_DIR}/spec.md`
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, patterns |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, NFR-X to implement |
| Contracts | `.aidocs/contracts.md` | Existing API patterns |
| Related Design | `features/done/{NN}-{feature}/design.md` | Patterns to follow |

---

## Overview

[2-3 sentences summarizing technical approach and key decisions]

---

## Spec Coverage

| FR/NFR | Requirement | Implemented By |
|--------|-------------|----------------|
| FR-001 | [Summary] | AD-001, AD-002 |
| FR-002 | [Summary] | AD-001 |
| NFR-001 | [Summary] | AD-003 |

---

## Architectural Decisions

### AD-001: [Decision Title]

**Context:** [Why this decision is needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Considered:**
| Alternative | Why Rejected |
|-------------|--------------|
| [Option A] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]

**Traces to:** FR-001, FR-002

---

## File Structure

```
src/
├── feature/
│   ├── handlers/
│   │   └── create.ts    # CREATE - FR-001
│   ├── services/
│   │   └── logic.ts     # CREATE - FR-002
│   └── index.ts         # CREATE
└── tests/
    └── feature/
        └── create.test.ts  # CREATE
```

### File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/feature/handlers/create.ts` | Create handler | FR-001 | AD-001 |
| MODIFY | `src/middleware/auth.ts` | Add permission | FR-003 | AD-002 |

---

## Data Models

### [Model Name]

```typescript
interface ModelName {
  id: string;
  field1: string;
  createdAt: Date;
}
```

**Database:**
```sql
CREATE TABLE model_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  field1 VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Contracts

### [METHOD] /api/[endpoint]

**Summary:** [What this endpoint does]
**Authentication:** Required | None

**Request:**
```json
{
  "field1": "value"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field1": "value"
}
```

**Errors:**
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Invalid input | `{"error": "..."}` |

---

## Dependencies

### Packages
| Package | Version | Purpose |
|---------|---------|---------|
| [name] | ^X.Y.Z | [Why needed] |

### External Services
| Service | Purpose | Required |
|---------|---------|----------|
| [name] | [Why] | Yes/No |

---

## Security Considerations

| Concern | Mitigation | AD |
|---------|------------|-----|
| [Concern] | [Strategy] | AD-X |

---

## Performance Considerations

| Concern | Strategy | Target |
|---------|----------|--------|
| [Concern] | [Approach] | [Metric] |

---

## Testing Strategy

### Unit Tests
- [ ] [What to test]

### Integration Tests
- [ ] [What to test]

### E2E Tests
- [ ] [Critical flow]

---

## Migration Strategy

### Data Migration
- [Required migrations]

### Backwards Compatibility
- [Considerations]

### Rollback Plan
- [Steps to rollback]

---

## Related Designs

| Feature | Relationship | Patterns to Reuse |
|---------|-------------|-------------------|
| [feature] | [dependency/similar] | [patterns] |

---

## Recommended Skills & Methodologies

### Skills
| Skill | Purpose |
|-------|---------|
| faion-software-developer | Implementation |
| faion-devops-engineer | Infrastructure |

### Methodologies
| ID | Name | Purpose |
|----|------|---------|
| M-DEV-XXX | [Name] | [How it helps] |

---

## Open Questions

- [ ] [Question to resolve before implementation]

---

## References

- [Link to external documentation]
- [Link to similar design]
```

---

## Quality Checklist

### Design Quality Gate (Before Implementation Plan)

**Completeness:**
- [ ] All FR-X from spec have corresponding AD-X
- [ ] All NFR-X addressed (performance, security, scalability)
- [ ] All files listed with CREATE/MODIFY actions
- [ ] All API endpoints documented with request/response
- [ ] All data models defined (TypeScript + SQL)
- [ ] Dependencies listed with versions

**Clarity:**
- [ ] Each AD-X has context, decision, rationale
- [ ] Alternatives considered and rejected
- [ ] Consequences documented (positive and negative)
- [ ] File changes traced to FR-X and AD-X

**Traceability:**
- [ ] Spec Coverage matrix complete
- [ ] Every FR maps to at least one AD
- [ ] Every file change traces to FR and AD

**Context:**
- [ ] Constitution referenced
- [ ] Related designs identified
- [ ] Existing patterns documented
- [ ] Skills/methodologies recommended

**Risk:**
- [ ] Security considerations documented
- [ ] Performance targets defined
- [ ] Migration/rollback plan (if applicable)

---

## Sources

- [Google Design Docs Guide](https://www.industrialempathy.com/posts/design-docs-at-google/) - Google's approach to design docs
- [RFC 2119: Key words for RFCs](https://www.ietf.org/rfc/rfc2119.txt) - SHALL/SHOULD/MAY terminology
- [C4 Model](https://c4model.com/) - Software architecture diagrams
- [ADR GitHub Organization](https://adr.github.io/) - Architecture Decision Records
- [OpenAPI Specification](https://swagger.io/specification/) - API contract documentation
