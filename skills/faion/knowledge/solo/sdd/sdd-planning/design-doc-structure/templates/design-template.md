# Design: [Feature Name]

**Version:** 1.0
**Spec:** `{FEATURE_DIR}/spec.md`
**Status:** Draft
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
- [Reason 1 — project-specific]
- [Reason 2 — project-specific]

**Alternatives Considered:**
| Alternative | Why Rejected |
|-------------|--------------|
| [Option A] | [Concrete project-specific reason] |
| [Option B] | [Concrete project-specific reason] |

**Consequences:**
- Positive: [Benefits]
- Negative: [Trade-offs]

**Traces to:** FR-001, FR-002

---

## File Structure

```
src/
├── feature/
│   ├── handlers/
│   │   └── create.ts    # CREATE - FR-001
│   └── services/
│       └── logic.ts     # CREATE - FR-002
└── tests/
    └── feature/
        └── create.test.ts  # CREATE
```

### File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/feature/handlers/create.ts` | Create handler | FR-001 | AD-001 |
| MODIFY | `src/middleware/auth.ts` | Add permission check | FR-003 | AD-002 |

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
**Authentication:** Required

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
| 400 | Invalid input | `{"code": "INVALID_INPUT", "message": "..."}` |
| 401 | Unauthenticated | `{"code": "UNAUTHORIZED", "message": "..."}` |

---

## Dependencies

### Packages
| Package | Version | Purpose |
|---------|---------|---------|
| [name] | ^X.Y.Z | [Why needed] |

### External Services
| Service | Purpose | Required |
|---------|---------|----------|
| [name] | [Why] | Yes |

---

## Security Considerations

| Threat | Mitigation | AD |
|--------|------------|-----|
| SQL injection | Parameterized queries via ORM | AD-X |
| CSRF | Double-submit cookie pattern | AD-X |

---

## Performance Considerations

| Concern | Strategy | Target |
|---------|----------|--------|
| [Concern] | [Approach] | [Metric from NFR-X] |

---

## Testing Strategy

### Unit Tests
- [ ] [What to test and why]

### Integration Tests
- [ ] [API endpoint + expected behavior]

### E2E Tests
- [ ] [Critical user flow]

---

## Migration Strategy

### Data Migration
- [Required migrations, if any]

### Rollback Plan
- [Steps to rollback if deployment fails]

---

## Open Questions

- [ ] [Question to resolve before implementation starts]

---

## References

- [Link to external documentation]
