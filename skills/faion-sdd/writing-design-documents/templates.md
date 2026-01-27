# Design Document Templates

Ready-to-use templates for different documentation needs.

---

## Template 1: SDD Design Document (Full)

LLM-optimized template for feature design.

```markdown
# Design: [Feature Name]

**Version:** 1.0
**Spec:** `{FEATURE_DIR}/spec.md`
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, patterns |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, NFR-X |
| Related Design | `done/{NN}-{feature}/design.md` | Patterns |

---

## Overview

[2-3 sentences: technical approach, key technologies, main decisions]

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

**Status:** Proposed | Accepted | Deprecated

**Context:** [Background, constraints, why decision needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Option A] | [+] | [-] | [Reason] |
| [Option B] | [+] | [-] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

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
| CREATE | `src/feature/handlers/create.ts` | Handler | FR-001 | AD-001 |
| MODIFY | `src/middleware/auth.ts` | Add check | FR-003 | AD-002 |

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

**Validation:**
| Field | Rules |
|-------|-------|
| field1 | Required, max 255 chars |

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
| 401 | Not authenticated | `{"error": "..."}` |

---

## Dependencies

### Packages

| Package | Version | Purpose |
|---------|---------|---------|
| [name] | ^X.Y.Z | [Why needed] |

### External Services

| Service | Purpose | Required | Fallback |
|---------|---------|----------|----------|
| [name] | [Why] | Yes/No | [Alternative] |

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

### Backwards Compatibility
- [Considerations]

### Rollback Plan
1. [Step 1]
2. [Step 2]

---

**Status:** [DRAFT | APPROVED] - Ready for Implementation Plan
```

---

## Template 2: RFC (Request for Comments)

Based on [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template).

```markdown
# RFC: [Title]

**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Accepted | Rejected
**Stakeholders:** [Teams/People affected]

---

## Overview

[1-2 paragraphs: What is the goal of this RFC, without diving into why/how]

---

## Background

[Comprehensive context that a random engineer needs to understand the RFC]

### Current State
[How things work now]

### Problem Statement
[What problem this solves]

### Why Now?
[Why is this the right time to address this]

---

## Goals

- [Goal 1]
- [Goal 2]

## Non-Goals

- [Explicitly NOT doing X]
- [Out of scope: Y]

---

## Proposal

[Overview of the "how" - the proposed solution]

### High-Level Design

[Architecture, components, flow]

### Implementation Details

[Rough API changes, package changes, etc.]

### Example Usage

```typescript
// How the proposal would be used
```

---

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [What this alternative is]

**Pros:**
- [Advantage]

**Cons:**
- [Disadvantage]

**Why Not Chosen:** [Reason]

### Alternative 2: [Name]

[Same structure]

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Security Considerations

[Security implications and how they're addressed]

---

## Dependencies

[Other teams, services, or work this depends on]

---

## Rollout Plan

### Phase 1: [Name]
- [What happens]
- [Success criteria]

### Phase 2: [Name]
- [What happens]

### Rollback Plan
- [How to revert if needed]

---

## Open Questions

- [ ] [Question that needs resolution]
- [ ] [Another question]

---

## Appendix

[Additional details, references, data]
```

---

## Template 3: Technical Design Document (TDD)

Detailed technical specification.

```markdown
# Technical Design Document: [System Name]

**Version:** 1.0
**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | Approved

---

## 1. Introduction

### 1.1 Purpose
[Purpose of this document]

### 1.2 Scope
[What is and isn't covered]

### 1.3 Definitions
| Term | Definition |
|------|------------|
| [Term] | [Definition] |

---

## 2. System Overview

### 2.1 Description
[High-level description of the system]

### 2.2 Context Diagram

```
[External Systems] --> [This System] --> [Downstream]
```

### 2.3 Assumptions
- [Assumption 1]
- [Assumption 2]

### 2.4 Constraints
- [Constraint 1]
- [Constraint 2]

---

## 3. Architecture

### 3.1 High-Level Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 3.2 Component Diagram

[Components and their relationships]

### 3.3 Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | React | 18.x |
| Backend | Node.js | 20.x |
| Database | PostgreSQL | 15.x |

---

## 4. Data Design

### 4.1 Data Model

```
User                     Order
├── id (PK)              ├── id (PK)
├── email                ├── user_id (FK)
├── name                 ├── total
└── created_at           └── created_at
```

### 4.2 Database Schema

```sql
-- Table definitions
```

### 4.3 Data Flow

[How data moves through the system]

---

## 5. API Design

### 5.1 API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/users | GET | List users |
| /api/users | POST | Create user |

### 5.2 API Specifications

[Detailed endpoint specs]

---

## 6. Security Design

### 6.1 Authentication
[How authentication works]

### 6.2 Authorization
[How authorization works]

### 6.3 Data Protection
[Encryption, PII handling, etc.]

---

## 7. Performance Considerations

### 7.1 Performance Requirements

| Metric | Target |
|--------|--------|
| Response time (p95) | < 200ms |
| Throughput | 1000 req/s |

### 7.2 Scalability
[How the system scales]

### 7.3 Caching Strategy
[What is cached and how]

---

## 8. Reliability

### 8.1 Availability Target
[SLA/SLO]

### 8.2 Failure Modes
[What can fail and what happens]

### 8.3 Recovery
[How the system recovers]

---

## 9. Monitoring and Observability

### 9.1 Logging
[What is logged and where]

### 9.2 Metrics
[Key metrics to track]

### 9.3 Alerting
[Alert conditions and thresholds]

---

## 10. Testing Strategy

### 10.1 Test Levels
[Unit, integration, E2E]

### 10.2 Test Coverage
[Coverage requirements]

---

## 11. Deployment

### 11.1 Deployment Process
[How deployment works]

### 11.2 Configuration
[Environment variables, secrets]

---

## 12. References

- [Link 1]
- [Link 2]
```

---

## Template 4: Architecture Decision Record (ADR)

Based on [Michael Nygard's template](https://github.com/joelparkerhenderson/architecture-decision-record).

```markdown
# ADR-001: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context

[Description of the issue motivating this decision. What is the context?
What problem are we trying to solve? What are the forces at play?]

## Decision

[Description of our response to these forces. What is the change that
we're proposing and/or doing? State the decision clearly.]

## Consequences

[Description of the resulting context after applying the decision.
All consequences should be listed, not just the "positive" ones.]

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Drawback 1]
- [Drawback 2]

### Neutral

- [Observation]
```

---

## Template 5: Lightweight Design (Mini)

For small changes that still need documentation.

```markdown
# Design: [Feature Name]

**Date:** YYYY-MM-DD | **Status:** Approved

## Overview

[1-2 sentences describing the change]

## Decision

[What we're doing and why]

## Files Changed

| Action | File |
|--------|------|
| CREATE | path/to/file.ts |
| MODIFY | path/to/other.ts |

## API Changes (if any)

[Endpoint changes]

---

**Approved:** Ready for implementation
```

---

## Template 6: Component Design (Frontend)

For React/Vue/Svelte components.

```markdown
# Component Design: [ComponentName]

**Version:** 1.0
**Status:** Approved

---

## Purpose

[What this component does]

---

## Component API

### Props

```typescript
interface ComponentNameProps {
  /** Description of prop */
  propName: string;
  /** Optional prop with default */
  optionalProp?: boolean;
  /** Callback handler */
  onAction?: (value: string) => void;
}
```

### Default Props

```typescript
const defaultProps = {
  optionalProp: false,
};
```

---

## State

```typescript
interface State {
  isOpen: boolean;
  value: string;
}
```

---

## Behavior

1. [Behavior 1]
2. [Behavior 2]
3. [Behavior 3]

---

## Visual States

| State | Appearance |
|-------|------------|
| Default | [Description] |
| Hover | [Description] |
| Active | [Description] |
| Disabled | [Description] |
| Error | [Description] |

---

## Accessibility

- [ ] Keyboard navigation
- [ ] ARIA labels
- [ ] Focus management
- [ ] Screen reader support

---

## Usage Example

```tsx
<ComponentName
  propName="value"
  onAction={(v) => console.log(v)}
/>
```

---

## File Location

`src/components/[Category]/ComponentName.tsx`

---

**Status:** APPROVED
```

---

## Choosing a Template

| Situation | Template |
|-----------|----------|
| New feature (full SDD) | Template 1: SDD Design Document |
| Proposing major change | Template 2: RFC |
| Detailed system spec | Template 3: TDD |
| Single architecture decision | Template 4: ADR |
| Small change | Template 5: Lightweight |
| UI component | Template 6: Component Design |

---

*Templates | SDD Documentation | Version 3.0.0*
