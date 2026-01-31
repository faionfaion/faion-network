# Design Document Template

Technical design defines HOW to build. Copy and customize after spec approval.

---

```markdown
---
version: "1.0"
status: draft | review | approved
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: {name}
feature: {feature-NNN-slug}
spec: spec.md
---

# Design: {Feature Name}

## Reference Documents

| Document | Path |
|----------|------|
| Specification | `spec.md` |
| Constitution | `.aidocs/constitution.md` |
| API Contracts | `.aidocs/contracts.md` |

---

## Overview

{2-3 sentences: technical approach summary. How will this be built at a high level.}

---

## Architecture Decisions

### AD-1: {Decision Name}

**Context:**
{Problem being solved. What forces are at play. Why a decision is needed.}

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| A: {Option} | {benefits} | {drawbacks} |
| B: {Option} | {benefits} | {drawbacks} |
| C: {Option} | {benefits} | {drawbacks} |

**Decision:** {Chosen option}

**Rationale:**
{Why this option was chosen. What factors were most important.}

**Consequences:**
- {Positive consequence}
- {Negative consequence or trade-off}

### AD-2: {Decision Name}

{Repeat format for each significant decision}

---

## System Design

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │Service A │   │Service B │   │Service C │
        └──────────┘   └──────────┘   └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌─────────────────┐
                    │    Database     │
                    └─────────────────┘
```

### Component Details

| Component | Purpose | Location | Dependencies |
|-----------|---------|----------|--------------|
| {Name} | {what it does} | {path} | {what it uses} |
| {Name} | {what it does} | {path} | {what it uses} |

---

## Data Flow

### Primary Flow: {Flow Name}

```
1. User → {action}
         ↓
2. {Component A} → validate input
         ↓
3. {Component B} → process request
         ↓
4. {Component C} → persist data
         ↓
5. Response → User
```

### Error Flow

```
1. Error detected
         ↓
2. Log error with context
         ↓
3. Return appropriate error response
         ↓
4. Client handles/displays error
```

---

## Data Models

### {Model Name}

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| {field} | {type} | {constraints} | {description} |
| {field} | {type} | {constraints} | {description} |
| created_at | datetime | NOT NULL | Creation timestamp |
| updated_at | datetime | NOT NULL | Last modification |

**Indexes:**
- `idx_{model}_{field}` - {purpose}

**Relations:**
- `{model} -> {related_model}` (1:N via `{field}`)

### {Model Name 2}

{Repeat for each model}

### Entity Relationship

```
┌─────────┐       ┌─────────┐
│ Model A │ 1───N │ Model B │
└─────────┘       └─────────┘
     │
     │ 1
     │
     N
┌─────────┐
│ Model C │
└─────────┘
```

---

## API Design

### Endpoints

| Method | Path | Description | Auth | FR |
|--------|------|-------------|------|-----|
| POST | `/api/v1/{resource}` | Create resource | Required | FR-001 |
| GET | `/api/v1/{resource}` | List resources | Required | FR-002 |
| GET | `/api/v1/{resource}/{id}` | Get resource | Required | FR-002 |
| PATCH | `/api/v1/{resource}/{id}` | Update resource | Required | FR-003 |
| DELETE | `/api/v1/{resource}/{id}` | Delete resource | Required | FR-004 |

### Request/Response Examples

#### POST `/api/v1/{resource}`

**Request:**
```json
{
  "field1": "value",
  "field2": 123
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "field1": "value",
  "field2": 123,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Response (400):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field validation failed",
    "details": [
      {"field": "field1", "message": "Required field"}
    ]
  }
}
```

---

## Files to Create/Modify

| File | Action | Description | FR |
|------|--------|-------------|-----|
| `{path/to/file.py}` | CREATE | {what to create} | FR-001 |
| `{path/to/file.py}` | MODIFY | {what to modify} | FR-002 |
| `{path/to/test.py}` | CREATE | {test coverage} | - |

---

## Interfaces

### Internal Interfaces

| Interface | Provider | Consumer | Contract |
|-----------|----------|----------|----------|
| {name} | {component} | {component} | {description} |

### External Interfaces

| Interface | Type | Auth | Rate Limit |
|-----------|------|------|------------|
| {Third-party API} | REST | API Key | 100/min |

---

## Error Handling

| Error Type | Code | HTTP Status | User Message |
|------------|------|-------------|--------------|
| Validation | VALIDATION_ERROR | 400 | {message} |
| Not Found | NOT_FOUND | 404 | {message} |
| Unauthorized | UNAUTHORIZED | 401 | {message} |
| Forbidden | FORBIDDEN | 403 | {message} |
| Rate Limited | RATE_LIMITED | 429 | {message} |
| Internal | INTERNAL_ERROR | 500 | {message} |

---

## Security Considerations

### Authentication

| Mechanism | Scope | Implementation |
|-----------|-------|----------------|
| {method} | {endpoints} | {details} |

### Authorization

| Role | Permissions |
|------|-------------|
| {role} | {what they can do} |

### Data Protection

| Data Type | Protection | Justification |
|-----------|------------|---------------|
| {data} | {method} | {why needed} |

---

## Performance Considerations

### Caching Strategy

| Data | Cache Type | TTL | Invalidation |
|------|------------|-----|--------------|
| {data} | {type} | {duration} | {trigger} |

### Optimization

| Optimization | Target | Approach |
|--------------|--------|----------|
| {name} | {metric} | {how} |

---

## Testing Strategy

### Unit Tests

| Component | Test File | Key Scenarios |
|-----------|-----------|---------------|
| {component} | `test_{name}.py` | {scenarios} |

### Integration Tests

| Flow | Test File | Dependencies |
|------|-----------|--------------|
| {flow} | `test_{name}_integration.py` | {deps} |

### E2E Tests

| Scenario | Test File | Prerequisites |
|----------|-----------|---------------|
| {scenario} | `test_{name}_e2e.py` | {setup} |

---

## Migration Strategy

{If modifying existing functionality}

### Database Migrations

| Migration | Description | Reversible |
|-----------|-------------|------------|
| {name} | {what it does} | Yes/No |

### Data Migration

| Data | From | To | Strategy |
|------|------|-----|----------|
| {data} | {old} | {new} | {approach} |

### Rollback Plan

1. {Step 1}
2. {Step 2}
3. {Step 3}

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {risk} | High/Med/Low | High/Med/Low | {mitigation} |

---

## Alternatives Not Chosen

| Alternative | Why Not Chosen |
|-------------|----------------|
| {option} | {reason} |

---

## FR Coverage Matrix

| FR | AD | Components | Files | Status |
|----|-----|------------|-------|--------|
| FR-001 | AD-1 | {components} | {files} | Designed |
| FR-002 | AD-2 | {components} | {files} | Designed |

---

## Open Design Questions

| # | Question | Impact | Status |
|---|----------|--------|--------|
| 1 | {question} | {what it affects} | Open/Resolved |

---

*Design Document v1.0*
*Feature: {feature-NNN-slug}*
```

---

## Usage Notes

### ADR Format

Architecture Decision Records follow the pattern:
- **Context**: Why is this decision needed?
- **Options**: What alternatives were considered?
- **Decision**: What was chosen?
- **Consequences**: What are the trade-offs?

### Design vs Implementation

Design documents describe:
- **Structure**: What components exist and how they connect
- **Interfaces**: How components communicate
- **Data**: What data is stored and how

Design documents do NOT:
- Contain actual code (use examples/pseudocode)
- Specify every implementation detail
- Lock in minor decisions

### Traceability

Every design decision should trace to functional requirements:
- FR -> AD (which decision addresses which requirement)
- AD -> Files (which files implement which decision)
- Files -> Tests (which tests verify which files)
