# Specification Templates

Ready-to-use templates for different feature types. Copy and fill in the blanks.

---

## Template Selection Guide

| Feature Type | Template | When to Use |
|--------------|----------|-------------|
| Full Feature | [Full Feature Spec](#full-feature-spec) | Complex multi-component features |
| API Endpoint | [API Spec](#api-endpoint-spec) | REST/GraphQL endpoints |
| UI Component | [Component Spec](#ui-component-spec) | Reusable UI components |
| Page/Screen | [Page Spec](#page-spec) | Full pages or screens |
| Integration | [Integration Spec](#integration-spec) | Third-party integrations |
| Migration | [Migration Spec](#migration-spec) | Database/data migrations |
| Minimal | [MVS](#minimal-viable-spec-mvs) | Simple, single-task features |

---

## Full Feature Spec

For complex features spanning multiple components.

```markdown
# Feature: [Feature Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | [Relevant sections] |
| Related Feature | `done/{NN}-{feature}/spec.md` | [Patterns to follow] |

---

## Overview

[2-3 sentences describing the feature and its purpose. What does it enable?]

---

## Problem Statement

| Field | Value |
|-------|-------|
| **Who** | [User persona/role] |
| **Problem** | [What they cannot do today] |
| **Impact** | [Business/user impact - quantify if possible] |
| **Solution** | [High-level approach] |
| **Success Metric** | [How we measure success] |

---

## User Personas

### Persona 1: [Archetype Name]
- **Role:** [What they do]
- **Goal:** [What they want to achieve]
- **Pain Points:** [Current frustrations]
- **Context:** [When/where they use product]

### Persona 2: [Archetype Name]
[Same structure]

---

## User Stories

### US-001: [Story Title] (MVP)

**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:** AC-001, AC-002
**Priority:** Must | Should | Could
**Complexity:** Low | Medium | High

### US-002: [Story Title]
[Same structure]

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL [requirement] | US-001 | Must |
| FR-002 | System SHALL [requirement] | US-001 | Must |
| FR-003 | System SHOULD [requirement] | US-002 | Should |

### FR-001: [Requirement Title]

**Requirement:** System SHALL [specific, testable requirement].

**Rationale:** [Why this is needed]

**Traces to:** US-001

**Validation Rules:**
- [Rule 1 with specific values]
- [Rule 2 with specific values]

**Technical Notes:**
- [Implementation hints if needed]

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | [Metric] | [Target value] | Must |
| NFR-002 | Security | [Mechanism] | [Specification] | Must |
| NFR-003 | Scalability | [Capacity] | [Number] | Should |
| NFR-004 | Accessibility | [Standard] | [Level] | Should |

---

## Acceptance Criteria

### AC-001: [Scenario Title - Happy Path]

**Scenario:** [Brief description]

**Given:** [precondition]
**And:** [additional precondition]
**When:** [action with specific values]
**And:** [additional action]
**Then:** [expected result]
**And:** [additional result]

### AC-002: [Scenario Title - Error Case]

**Scenario:** [Brief description]

**Given:** [precondition that will cause error]
**When:** [action]
**Then:** [error handling behavior]

### AC-003: [Scenario Title - Edge Case]
[Same structure]

**Coverage Checklist:**
- [ ] Happy path
- [ ] Error handling
- [ ] Boundary conditions
- [ ] Security scenarios
- [ ] Performance scenarios (if NFRs exist)

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| [Feature 1] | [Why excluded] | Phase 2 | v1.1 | Never |
| [Feature 2] | [Why excluded] | [Timeline] |

---

## Assumptions & Constraints

### Assumptions
- [What we assume to be true]
- [Dependency we expect to be available]

### Constraints
- [Technical limitation]
- [Business constraint]
- [Timeline constraint]

---

## Dependencies

### Internal
- [Feature/component this depends on]

### External
- [Third-party service/API]
- [Library requirement]

---

## Boundaries

### Always (Safe Actions)
- [Action agent can always take]
- [Pattern to follow]

### Ask First (High Impact)
- [Change requiring review]

### Never (Hard Stops)
- [Action agent must not take]

---

## Open Questions

- [ ] [Question to resolve before design]
- [ ] [Clarification needed]

---

## Appendix

### Wireframes
[Link or description]

### Data Models (if known)
[Preliminary models]

### Related Resources
[Links to research, competitors, etc.]
```

---

## API Endpoint Spec

For REST or GraphQL endpoints.

```markdown
# API: [Endpoint Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Base Path:** `/api/v1`

---

## Overview

[Brief description of what this endpoint does]

---

## Endpoint Specification

| Field | Value |
|-------|-------|
| Method | GET | POST | PUT | PATCH | DELETE |
| Path | `/resource/:id/action` |
| Auth | Bearer JWT | API Key | None |
| Rate Limit | [X] requests/minute |
| Idempotent | Yes | No |

---

## Request

### Headers

| Header | Required | Value |
|--------|----------|-------|
| Authorization | Yes | `Bearer <token>` |
| Content-Type | Yes (POST/PUT) | `application/json` |
| X-Request-Id | No | UUID for tracing |

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource identifier |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page (max 100) |
| sort | string | No | created_at | Sort field |
| order | string | No | desc | asc | desc |

### Request Body

```json
{
  "field1": "string (required, max 255 chars)",
  "field2": 123,
  "nested": {
    "subfield": "value"
  }
}
```

### Validation Rules

| Field | Rules |
|-------|-------|
| field1 | Required, string, 1-255 characters |
| field2 | Optional, integer, 0-1000000 |
| nested.subfield | Required if nested present, string |

---

## Response

### Success Response (200/201)

```json
{
  "data": {
    "id": "res_abc123",
    "field1": "value",
    "field2": 123,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "request_id": "req_xyz789"
  }
}
```

### List Response (200)

```json
{
  "data": [
    { "id": "res_1", ... },
    { "id": "res_2", ... }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "field1", "message": "Field is required" },
      { "field": "field2", "message": "Must be between 0 and 1000000" }
    ]
  }
}
```

#### 401 Unauthorized
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

#### 403 Forbidden
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions for this resource"
  }
}
```

#### 404 Not Found
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

#### 429 Too Many Requests
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 60 seconds"
  }
}
```

#### 500 Internal Server Error
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "request_id": "req_xyz789"
  }
}
```

---

## Acceptance Criteria

### AC-001: Successful Request

**Given:** Valid JWT for user with permission
**And:** Valid request body with field1="test", field2=100
**When:** POST request to `/api/v1/resource`
**Then:** Response status is 201
**And:** Response contains created resource with id
**And:** created_at is set to current timestamp

### AC-002: Validation Error

**Given:** Valid JWT
**And:** Request body with missing required field1
**When:** POST request to `/api/v1/resource`
**Then:** Response status is 400
**And:** Error code is "VALIDATION_ERROR"
**And:** Details array contains field1 error

### AC-003: Unauthorized Access

**Given:** No Authorization header
**When:** POST request to `/api/v1/resource`
**Then:** Response status is 401
**And:** Error code is "UNAUTHORIZED"

### AC-004: Rate Limiting

**Given:** Valid JWT
**When:** [Rate limit + 1] requests in 1 minute
**Then:** Response status is 429 for requests exceeding limit
**And:** Retry-After header is set

---

## Technical Notes

- Use existing validation middleware from `src/middleware/validate.ts`
- Log all errors to Sentry with request_id
- Cache GET responses for 60 seconds (if applicable)
```

---

## UI Component Spec

For reusable UI components.

```markdown
# Component: [Component Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Location:** `src/components/[ComponentName]/`

---

## Overview

[Brief description of the component's purpose and when to use it]

---

## Props Interface

```typescript
interface [ComponentName]Props {
  /** Description of prop */
  propName: 'option1' | 'option2' | 'option3';

  /** Description - optional prop */
  optionalProp?: boolean;

  /** Description with default */
  withDefault?: string; // default: "value"

  /** Callback props */
  onChange?: (value: string) => void;

  /** Children */
  children: React.ReactNode;
}
```

---

## Visual Specifications

### Variants

| Variant | Background | Text | Border | Use Case |
|---------|------------|------|--------|----------|
| variant1 | `#hexcode` | `#hexcode` | `Xpx #hexcode` | [When to use] |
| variant2 | `#hexcode` | `#hexcode` | none | [When to use] |

### Sizes

| Size | Height | Padding | Font Size | Icon Size |
|------|--------|---------|-----------|-----------|
| sm | 32px | 8px 12px | 14px | 16px |
| md | 40px | 12px 16px | 16px | 20px |
| lg | 48px | 16px 24px | 18px | 24px |

### States

| State | Visual Change |
|-------|---------------|
| Default | [Base appearance] |
| Hover | [Background/border change] |
| Focus | [Focus ring: 2px solid #color, 2px offset] |
| Active | [Pressed state] |
| Disabled | [Opacity 0.5, cursor not-allowed] |
| Loading | [Spinner, content hidden] |
| Error | [Red border/text] |

---

## Accessibility Requirements

- [ ] Semantic HTML element (button, input, etc.)
- [ ] `aria-label` when no visible text
- [ ] `aria-disabled` when disabled (not just disabled attr)
- [ ] `aria-busy` when loading
- [ ] `aria-invalid` for error state
- [ ] Focus visible: `2px solid [color]` with offset
- [ ] Keyboard navigation: Tab, Enter, Space, Arrow keys
- [ ] Minimum touch target: 44x44px
- [ ] Color contrast: 4.5:1 for text, 3:1 for UI elements

---

## Usage Examples

### Basic Usage

```tsx
<ComponentName variant="primary" size="md">
  Label
</ComponentName>
```

### With All Props

```tsx
<ComponentName
  variant="primary"
  size="md"
  disabled={false}
  loading={isLoading}
  onChange={handleChange}
>
  Label
</ComponentName>
```

### Common Patterns

```tsx
// Pattern 1: [Description]
<ComponentName ... />

// Pattern 2: [Description]
<ComponentName ... />
```

---

## Acceptance Criteria

### AC-001: Default Render

**Given:** Component with variant="primary" size="md"
**When:** Component renders
**Then:** Height is 40px
**And:** Background color is [#hexcode]
**And:** Text color is [#hexcode]

### AC-002: Hover State

**Given:** Component in default state
**When:** User hovers over component
**Then:** Background changes to [#hexcode]
**And:** Transition duration is 150ms

### AC-003: Disabled State

**Given:** Component with disabled={true}
**When:** Component renders
**Then:** Opacity is 0.5
**And:** Cursor is not-allowed
**And:** Click events are prevented
**And:** aria-disabled="true" is set

### AC-004: Loading State

**Given:** Component with loading={true}
**When:** Component renders
**Then:** Spinner icon is visible
**And:** Children are visually hidden (maintain width)
**And:** aria-busy="true" is set
**And:** Interactions are disabled

### AC-005: Keyboard Navigation

**Given:** Component is focused
**When:** User presses Enter or Space
**Then:** onClick/onChange is triggered
**And:** Focus ring is visible

---

## File Structure

```
src/components/[ComponentName]/
├── [ComponentName].tsx       # Main component
├── [ComponentName].test.tsx  # Tests
├── [ComponentName].stories.tsx # Storybook (optional)
├── types.ts                  # TypeScript interfaces
└── index.ts                  # Barrel export
```

---

## Dependencies

- [ ] Design tokens from `src/styles/tokens.ts`
- [ ] Icon library: [library name]
- [ ] Animation library: [if applicable]
```

---

## Page Spec

For full pages or screens.

```markdown
# Page: [Page Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Route:** `/path/to/page`

---

## Overview

[Brief description of page purpose]

---

## Page Layout

```
┌─────────────────────────────────────────┐
│ Header / Navigation                     │
├─────────────────────────────────────────┤
│                                         │
│  [Section 1]                            │
│  [Description of section]               │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  [Section 2]                            │
│  [Description of section]               │
│                                         │
├─────────────────────────────────────────┤
│ Footer                                  │
└─────────────────────────────────────────┘
```

---

## Sections

### Section 1: [Name]

**Purpose:** [What this section does]

**Components Used:**
- `ComponentA` - [purpose]
- `ComponentB` - [purpose]

**Data Requirements:**
- [Data field]: [source]

**Interactions:**
- [User action] -> [Result]

### Section 2: [Name]
[Same structure]

---

## Data Requirements

| Data | Source | Cache | Refresh |
|------|--------|-------|---------|
| User profile | GET /api/users/me | 5 min | On focus |
| Items list | GET /api/items | 1 min | On scroll |

---

## States

### Loading State
- Show skeleton for [sections]
- Preserve layout dimensions

### Empty State
- [Message to display]
- [CTA button if applicable]

### Error State
- [Error message]
- [Retry action]

---

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| < 640px (mobile) | [Layout changes] |
| 640-1024px (tablet) | [Layout changes] |
| > 1024px (desktop) | [Default layout] |

---

## SEO Requirements

| Meta | Value |
|------|-------|
| Title | [Page title - Site name] |
| Description | [150-160 char description] |
| OG Image | [Path or dynamic] |
| Canonical | [URL pattern] |

---

## Acceptance Criteria

[Standard Given-When-Then format for key interactions]
```

---

## Integration Spec

For third-party service integrations.

```markdown
# Integration: [Service Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Service:** [Provider name and URL]

---

## Overview

[What this integration enables]

---

## Service Details

| Field | Value |
|-------|-------|
| Provider | [Company name] |
| API Version | [v1, v2, etc.] |
| Auth Method | OAuth 2.0 | API Key | JWT |
| Base URL | `https://api.service.com/v1` |
| Documentation | [URL] |

---

## Credentials Management

| Credential | Environment Variable | Storage |
|------------|---------------------|---------|
| API Key | `SERVICE_API_KEY` | `.env` / Secrets Manager |
| Client ID | `SERVICE_CLIENT_ID` | `.env` |
| Client Secret | `SERVICE_CLIENT_SECRET` | Secrets Manager |

**Security Notes:**
- Never commit credentials to repository
- Rotate keys every [period]
- Use separate keys for dev/staging/prod

---

## Required Scopes / Permissions

| Scope | Purpose | Required |
|-------|---------|----------|
| `read:users` | Read user data | Yes |
| `write:data` | Create/update | Yes |
| `admin:all` | Admin access | No |

---

## API Endpoints Used

### Endpoint 1: [Name]

| Field | Value |
|-------|-------|
| Method | GET |
| Path | `/resource` |
| Rate Limit | 100/min |

**Our Usage:**
- [When/why we call this]
- [What we do with response]

### Endpoint 2: [Name]
[Same structure]

---

## Data Mapping

| Our Field | Service Field | Transform |
|-----------|---------------|-----------|
| user_id | external_id | Direct |
| full_name | first_name + last_name | Concatenate |
| created_at | timestamp | ISO 8601 |

---

## Error Handling

| Service Error | Our Response | Action |
|---------------|--------------|--------|
| 401 Unauthorized | Refresh token | Auto-retry once |
| 429 Rate Limited | Backoff | Exponential retry |
| 500 Server Error | Log + fallback | Notify on-call |
| Timeout (30s) | Timeout error | Circuit breaker |

---

## Fallback Behavior

When service is unavailable:
- [Graceful degradation strategy]
- [Cached data usage]
- [User notification]

---

## Acceptance Criteria

[Standard Given-When-Then for integration scenarios]
```

---

## Migration Spec

For database or data migrations.

```markdown
# Migration: [Migration Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Type:** Schema | Data | Combined

---

## Overview

[What this migration accomplishes]

---

## Current State

[Describe current schema/data structure]

```sql
-- Current schema
CREATE TABLE old_table (
  ...
);
```

---

## Target State

[Describe target schema/data structure]

```sql
-- Target schema
CREATE TABLE new_table (
  ...
);
```

---

## Migration Steps

### Step 1: [Action]
```sql
-- SQL or description
```
**Reversible:** Yes | No
**Downtime:** None | Brief | Extended

### Step 2: [Action]
[Same structure]

---

## Data Transformation

| Source | Target | Transform |
|--------|--------|-----------|
| old_field | new_field | [Logic] |

---

## Rollback Plan

### If migration fails at Step X:
1. [Rollback action]
2. [Restore action]

### Point of no return:
- After Step [X], rollback requires [manual intervention / backup restore]

---

## Validation

### Pre-migration checks:
- [ ] Backup completed
- [ ] [Check 1]
- [ ] [Check 2]

### Post-migration validation:
- [ ] Row counts match expected
- [ ] [Validation query 1]
- [ ] [Validation query 2]

---

## Acceptance Criteria

[Standard Given-When-Then for migration success]
```

---

## Minimal Viable Spec (MVS)

For simple, single-task features.

```markdown
# Feature: [Name]

## Problem
[Who cannot do what, and why it matters - 2-3 sentences]

## Solution
[What to build - high level - 2-3 sentences]

## Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System SHALL [specific requirement] | Must |
| FR-002 | System SHALL [specific requirement] | Must |

## Acceptance Criteria

### AC-001: [Happy Path]
Given [context]
When [action]
Then [expected result]

### AC-002: [Error Case]
Given [error condition]
When [action]
Then [error handling]

## Out of Scope
- [Explicit exclusion 1]
- [Explicit exclusion 2]

## Boundaries
- Always: [Safe actions]
- Never: [Forbidden actions]
```

---

*Specification Templates | v1.0.0*
