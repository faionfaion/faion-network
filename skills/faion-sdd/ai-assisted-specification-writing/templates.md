# Specification Templates

> Copy-paste templates for AI-assisted specification writing.

## Template 1: Feature Specification (spec.md)

```markdown
# [FEATURE_NAME] Specification

## Metadata
| Field | Value |
|-------|-------|
| Status | Draft / In Review / Approved |
| Author | [name] |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |
| Stakeholders | [list] |

## Overview

### Problem Statement
[What problem does this feature solve? Why does it matter?]

### Goals
1. [Primary goal]
2. [Secondary goal]

### Non-Goals (Out of Scope)
1. [What we are explicitly NOT building]
2. [Features deferred to later phases]

### Success Metrics
| Metric | Target | Current |
|--------|--------|---------|
| [metric] | [target] | [baseline] |

## User Stories

### US-1: [Story Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- AC-1.1: Given [context], when [action], then [outcome]
- AC-1.2: Given [context], when [action], then [outcome]

### US-2: [Story Title]
...

## Functional Requirements

### FR-1: [Requirement Title]
[Clear description of what the system shall do]

**Acceptance Criteria:**
- [Testable criterion]

### FR-2: [Requirement Title]
...

## Non-Functional Requirements

### Performance
- NFR-1: [Response time, throughput, etc.]

### Security
- NFR-2: [Authentication, authorization, data protection]

### Scalability
- NFR-3: [Growth expectations, scaling patterns]

### Reliability
- NFR-4: [Uptime, failover, recovery]

## Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-1 | [scenario] | [behavior] |
| EC-2 | [scenario] | [behavior] |

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| [service/feature] | Required / Optional | Available / Pending |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk] | High/Med/Low | High/Med/Low | [mitigation] |

## Assumptions

1. [Assumption that must hold true]
2. [Assumption about user behavior]

## Open Questions

- [ ] [Question needing resolution]
- [ ] [Question needing resolution]

## Appendix

### Glossary
| Term | Definition |
|------|------------|
| [term] | [definition] |

### References
- [Link to related document]
```

---

## Template 2: API Specification

```markdown
# [API_NAME] API Specification

## Overview
[Brief description of what this API does]

## Base URL
```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
```

## Authentication
[Describe auth method: Bearer token, API key, OAuth, etc.]

## Rate Limits
| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 60 | 1,000 |
| Pro | 600 | 50,000 |

## Endpoints

### [METHOD] /path/to/endpoint

**Description:** [What this endpoint does]

**Authentication:** Required / Optional / None

**Request:**

Headers:
```
Authorization: Bearer {token}
Content-Type: application/json
```

Path Parameters:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource identifier |

Query Parameters:
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page |

Request Body:
```json
{
  "field1": "string",
  "field2": 123,
  "nested": {
    "field3": true
  }
}
```

**Responses:**

200 OK:
```json
{
  "id": "abc123",
  "created_at": "2025-01-20T10:00:00Z",
  "data": {}
}
```

400 Bad Request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field 'field1' is required",
    "details": [
      {"field": "field1", "issue": "required"}
    ]
  }
}
```

401 Unauthorized:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

**Example:**

Request:
```bash
curl -X POST https://api.example.com/v1/resources \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}'
```

Response:
```json
{
  "id": "abc123",
  "field1": "value",
  "created_at": "2025-01-20T10:00:00Z"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMITED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

## Webhooks

### Event: resource.created

**Payload:**
```json
{
  "event": "resource.created",
  "timestamp": "2025-01-20T10:00:00Z",
  "data": {
    "id": "abc123"
  }
}
```

## SDK Examples

### Python
```python
from example_sdk import Client

client = Client(api_key="your-key")
result = client.resources.create(field1="value")
```

### JavaScript
```javascript
import { ExampleClient } from 'example-sdk';

const client = new ExampleClient({ apiKey: 'your-key' });
const result = await client.resources.create({ field1: 'value' });
```
```

---

## Template 3: Technical Design Document

```markdown
# [FEATURE_NAME] Technical Design

## Metadata
| Field | Value |
|-------|-------|
| Status | Draft / In Review / Approved |
| Author | [name] |
| Spec Reference | [link to spec.md] |
| Created | YYYY-MM-DD |

## Overview

### Context
[Background information, why this design is needed]

### Goals
[What this design achieves]

### Non-Goals
[What this design does NOT address]

## Architecture

### System Diagram
```
[ASCII diagram or link to image]

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API GW    │────▶│   Service   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │  Database   │
                                        └─────────────┘
```

### Components

#### Component A
**Responsibility:** [What it does]
**Technology:** [Stack/framework]
**Interfaces:** [APIs it exposes/consumes]

#### Component B
...

## Data Model

### Entity: [EntityName]
```sql
CREATE TABLE entity_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    field1 VARCHAR(255) NOT NULL,
    field2 INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_entity_field1 ON entity_name(field1);
```

### Entity Relationships
```
User 1──────* Document
     │
     └─────* Preference
```

## API Design

### Internal APIs
[APIs between services]

### External APIs
[See API Specification: link]

## Security Considerations

### Authentication
[How users/services authenticate]

### Authorization
[Permission model, RBAC/ABAC]

### Data Protection
[Encryption at rest/in transit, PII handling]

## Performance Considerations

### Expected Load
| Metric | Expected | Peak |
|--------|----------|------|
| RPS | 100 | 500 |
| Latency (p99) | 200ms | 500ms |

### Caching Strategy
[What to cache, TTL, invalidation]

### Database Optimization
[Indexes, query patterns, sharding]

## Reliability

### Failure Modes
| Failure | Impact | Mitigation |
|---------|--------|------------|
| [failure] | [impact] | [mitigation] |

### Monitoring
[Key metrics, alerts, dashboards]

### Recovery
[Backup strategy, recovery procedures]

## Migration Plan

### Phase 1: [Description]
- [ ] Step 1
- [ ] Step 2

### Phase 2: [Description]
...

### Rollback Plan
[How to revert if issues arise]

## Alternatives Considered

### Alternative A: [Name]
**Pros:**
- [advantage]

**Cons:**
- [disadvantage]

**Why Rejected:** [reason]

### Alternative B: [Name]
...

## Decision Log

| Decision | Date | Rationale |
|----------|------|-----------|
| [decision] | [date] | [why] |

## Open Questions

- [ ] [Question]
- [ ] [Question]

## References

- [Related design doc]
- [External documentation]
```

---

## Template 4: Implementation Plan

```markdown
# [FEATURE_NAME] Implementation Plan

## Metadata
| Field | Value |
|-------|-------|
| Spec Reference | [link] |
| Design Reference | [link] |
| Complexity | Low / Medium / High |
| Est. Tokens | ~Xk |

## Task Overview

```
Phase 1: Foundation
├── TASK-001: Setup database models
├── TASK-002: Create base API endpoints
└── TASK-003: Add authentication

Phase 2: Core Features
├── TASK-004: Implement feature A
├── TASK-005: Implement feature B
└── TASK-006: Add validation

Phase 3: Polish
├── TASK-007: Error handling
├── TASK-008: Logging & monitoring
└── TASK-009: Documentation
```

## Dependency Graph

```
TASK-001 ──┬──▶ TASK-004 ──┬──▶ TASK-007
           │               │
TASK-002 ──┤               ├──▶ TASK-008
           │               │
TASK-003 ──┴──▶ TASK-005 ──┴──▶ TASK-009
                    │
               TASK-006
```

## Parallelization Waves

### Wave 1 (Parallel)
| Task | Files | Complexity |
|------|-------|------------|
| TASK-001 | models.py | Low |
| TASK-002 | views.py, urls.py | Low |
| TASK-003 | auth.py | Medium |

### Wave 2 (After Wave 1)
| Task | Depends On | Complexity |
|------|------------|------------|
| TASK-004 | 001, 002 | Medium |
| TASK-005 | 002, 003 | Medium |

### Wave 3 (After Wave 2)
...

## Task Details

### TASK-001: Setup database models

**Objective:** Create database models for [feature]

**Files to Change:**
| Action | File | Scope |
|--------|------|-------|
| CREATE | app/models/entity.py | New model |
| MODIFY | app/models/__init__.py | Export |
| CREATE | migrations/0001_entity.py | Migration |

**Acceptance Criteria:**
- [ ] Model created with all fields from design
- [ ] Migration runs successfully
- [ ] Indexes created as specified

**Complexity:** Low
**Est. Tokens:** ~5k

### TASK-002: Create base API endpoints
...

## Quality Gates

### After Each Task
- [ ] Unit tests pass
- [ ] Linter passes
- [ ] Type checks pass

### After Each Phase
- [ ] Integration tests pass
- [ ] Code review completed
- [ ] Documentation updated

### Before Merge
- [ ] All acceptance criteria met
- [ ] E2E tests pass
- [ ] Performance validated

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| [risk] | High/Med/Low | [mitigation] |

## Notes

[Any additional context for implementers]
```

---

## Template 5: Task File (TASK_XXX.md)

```markdown
# TASK-XXX: [Task Title]

## SDD References
| Document | Path |
|----------|------|
| Spec | [path/to/spec.md] |
| Design | [path/to/design.md] |
| Impl Plan | [path/to/implementation-plan.md] |

## Task Context

### Dependencies Completed
- [x] TASK-001: [Title] - [Brief summary of what it provides]
- [x] TASK-002: [Title] - [Brief summary]

### This Task Provides
- [What this task delivers for dependent tasks]

## Requirements Coverage

### FR-X: [Full requirement text]
This task implements [specific aspect] of FR-X.

## Acceptance Criteria

### AC-1: [Criterion title]
**Given** [initial context]
**When** [action performed]
**Then** [expected outcome]

### AC-2: [Criterion title]
...

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | path/to/new_file.py | [Description] |
| MODIFY | path/to/existing.py | [What to change] |
| DELETE | path/to/obsolete.py | [Why removing] |

## Implementation Notes

[Technical details, patterns to follow, gotchas to avoid]

## Testing Requirements

- [ ] Unit tests for [component]
- [ ] Integration test for [flow]
- [ ] Edge case: [scenario]

## Complexity & Estimates

| Metric | Value |
|--------|-------|
| Complexity | Low / Medium / High |
| Est. Tokens | ~Xk |

---

## Execution Log

### Status: TODO / IN_PROGRESS / DONE / BLOCKED

### Implementation
[Fill during execution]

### Summary
[Fill after completion]

### Lessons Learned
[Fill if applicable]
```

---

## Template 6: AI Context Document

```markdown
# Project Context for AI Specification Writing

## Project Overview
**Name:** [project name]
**Type:** [web app / mobile / API / library / etc.]
**Domain:** [industry/domain]
**Stage:** [greenfield / enhancement / maintenance]

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | [React, Vue, etc.] |
| Backend | [Django, Node, etc.] |
| Database | [PostgreSQL, MongoDB, etc.] |
| Infrastructure | [AWS, GCP, on-prem] |

## Existing Patterns

### Code Structure
```
src/
├── models/      # Data models
├── services/    # Business logic
├── api/         # REST endpoints
└── utils/       # Helpers
```

### Naming Conventions
- Models: PascalCase, singular (User, not Users)
- Endpoints: kebab-case (/user-profiles)
- Functions: snake_case (get_user_by_id)

### Testing Standards
- Unit tests required for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows

## Constraints

### Technical
- Must support IE11 / Safari 12+
- Max response time: 200ms p99
- Max file size: 50MB

### Business
- GDPR compliance required
- Multi-tenant architecture
- Support for 10 languages

### Team
- 3 backend developers
- 2 frontend developers
- No dedicated QA (developers write tests)

## Quality Standards
- Code coverage: >80%
- Linting: ESLint/Pylint with strict config
- Type checking: TypeScript strict / Python mypy

## Domain Terminology

| Term | Definition |
|------|------------|
| Workspace | Top-level container for user data |
| Project | Collection of tasks within a workspace |
| Task | Unit of work with assignee and deadline |

## Past Decisions (ADRs)
- ADR-001: Use PostgreSQL for relational data
- ADR-002: Use Redis for caching and sessions
- ADR-003: JWT for API authentication

## Anti-Patterns to Avoid
- No ORM queries in views/controllers
- No business logic in models
- No hardcoded configuration values
```

---

## Quick-Copy Sections

### User Story Template
```markdown
### US-X: [Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- AC-X.1: Given [context], when [action], then [outcome]
```

### Requirement Template
```markdown
### FR-X: [Title]
[Clear description of what the system shall do]

**Acceptance Criteria:**
- [Testable criterion 1]
- [Testable criterion 2]
```

### Edge Case Template
```markdown
| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-X | [scenario] | [behavior] |
```

### Risk Template
```markdown
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk] | H/M/L | H/M/L | [action] |
```

---

*Part of the [ai-assisted-specification-writing](README.md) methodology.*
