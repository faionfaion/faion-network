# SDD Trends Implementation Templates

Copy-paste templates for implementing modern Specification-Driven Development practices.

**Version:** 1.0

---

## Table of Contents

1. [Specification Templates](#1-specification-templates)
2. [ADR Templates](#2-adr-templates)
3. [Design Document Templates](#3-design-document-templates)
4. [Implementation Plan Templates](#4-implementation-plan-templates)
5. [Task File Templates](#5-task-file-templates)
6. [CLAUDE.md Templates](#6-claudemd-templates)
7. [Platform Engineering Templates](#7-platform-engineering-templates)
8. [Observability Templates](#8-observability-templates)

---

## 1. Specification Templates

### 1.1 Feature Specification

```markdown
# SPEC: [Feature Name]

## Metadata
| Field | Value |
|-------|-------|
| ID | SPEC-XXX |
| Status | Draft / Review / Approved |
| Author | [Name] |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |

---

## Problem Statement

[2-3 sentences describing the problem this feature solves. Include metrics if available.]

## Goals

- [ ] Goal 1: [Measurable outcome]
- [ ] Goal 2: [Measurable outcome]
- [ ] Goal 3: [Measurable outcome]

## Non-Goals

- [What this feature explicitly will NOT do]
- [Boundaries and limitations]

---

## User Stories

### US-1: [Story Title]

As a [user type], I want to [action] so that [benefit].

**Acceptance Criteria:**
- Given [context]
- When [action]
- Then [expected result]
- And [additional result]

### US-2: [Story Title]

As a [user type], I want to [action] so that [benefit].

**Acceptance Criteria:**
- Given [context]
- When [action]
- Then [expected result]

---

## Non-Functional Requirements

| ID | Category | Requirement | Target |
|----|----------|-------------|--------|
| NFR-1 | Performance | [Requirement] | [Metric] |
| NFR-2 | Security | [Requirement] | [Standard] |
| NFR-3 | Scalability | [Requirement] | [Metric] |

---

## Out of Scope

- [Feature/capability 1]
- [Feature/capability 2]
- [Explicitly excluded items]

---

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| [Metric 1] | [Value] | [Value] | [How measured] |
| [Metric 2] | [Value] | [Value] | [How measured] |

---

## Dependencies

- [Dependency 1]: [Status]
- [Dependency 2]: [Status]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Related Documents

- Design: [link]
- ADRs: [ADR-XXX](link)
- Previous specs: [link]

---

*Specification Document | SPEC-XXX | Version 1.0*
```

### 1.2 API Specification Outline

```markdown
# API SPEC: [API Name]

## Overview
[Brief description of the API's purpose]

## Base URL
- Production: `https://api.example.com/v1`
- Staging: `https://api-staging.example.com/v1`

## Authentication
[Authentication method: Bearer token, API key, OAuth 2.0]

## Rate Limits
| Tier | Limit | Window |
|------|-------|--------|
| Free | 100 | 1 minute |
| Pro | 1000 | 1 minute |

## Endpoints

### [Method] /[endpoint]

**Description:** [What this endpoint does]

**Request:**
```json
{
  "field": "type - description"
}
```

**Response (200):**
```json
{
  "field": "type - description"
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400 | [Bad request reason] |
| 401 | [Unauthorized reason] |
| 404 | [Not found reason] |

---

## Data Models

### [Model Name]
```typescript
interface ModelName {
  id: string;           // Unique identifier
  field: type;          // Description
  createdAt: string;    // ISO 8601 timestamp
}
```

---

## Webhooks

### [Event Name]
**Trigger:** [When this webhook fires]
**Payload:**
```json
{
  "event": "event.name",
  "data": {}
}
```

---

*API Specification | Version 1.0*
```

---

## 2. ADR Templates

### 2.1 Standard ADR

```markdown
# ADR-[NUMBER]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
YYYY-MM-DD

## Context
[Describe the issue that motivates this decision. What is the problem?
What constraints exist? What forces are at play?]

## Decision
[State the decision clearly. What are we doing? Be specific.]

## Rationale
[Why this decision? List the key factors that led to this choice.]

- Factor 1: [Explanation]
- Factor 2: [Explanation]
- Factor 3: [Explanation]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Neutral
- [Change that is neither good nor bad]

## Alternatives Considered

### [Alternative 1]
- Pros: [List]
- Cons: [List]
- Why rejected: [Reason]

### [Alternative 2]
- Pros: [List]
- Cons: [List]
- Why rejected: [Reason]

## Related Decisions
- [ADR-XXX](link): [Brief description]

## References
- [Link to relevant documentation]
- [Link to discussion/RFC]

---

*Architecture Decision Record | ADR-[NUMBER] | [Date]*
```

### 2.2 Lightweight ADR (Y-Statement)

```markdown
# ADR-[NUMBER]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Decision
In the context of [situation/problem],
facing [concern/constraint],
we decided [decision]
and neglected [alternatives],
to achieve [goals/benefits],
accepting [downsides/tradeoffs].

## Consequences
- [Consequence 1]
- [Consequence 2]
- [Consequence 3]

---

*ADR-[NUMBER] | YYYY-MM-DD*
```

---

## 3. Design Document Templates

### 3.1 Technical Design Document

```markdown
# DESIGN: [Feature Name]

## Metadata
| Field | Value |
|-------|-------|
| Spec | [SPEC-XXX](link) |
| Author | [Name] |
| Status | Draft / Review / Approved |
| Reviewers | [Names] |

---

## Overview

[1-2 paragraph summary of the technical approach]

## Architecture

### System Context
[How this fits into the broader system]

```
[ASCII diagram or link to diagram]
```

### Component Design

#### Component 1: [Name]
**Responsibility:** [What it does]
**Interface:**
```typescript
interface ComponentName {
  method(params): ReturnType;
}
```

#### Component 2: [Name]
**Responsibility:** [What it does]

---

## Data Model

### New Entities

```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY,
  field_name TYPE CONSTRAINTS,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Migrations
- Migration 1: [Description]
- Migration 2: [Description]

---

## API Design

### New Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /resource | Create resource |
| GET | /resource/:id | Get resource |

### Request/Response Examples

```json
// POST /resource
{
  "field": "value"
}
```

---

## Security Considerations

- [ ] Authentication: [Approach]
- [ ] Authorization: [Approach]
- [ ] Data protection: [Approach]
- [ ] Input validation: [Approach]

---

## Performance Considerations

| Aspect | Requirement | Approach |
|--------|-------------|----------|
| Latency | < 200ms p99 | [Strategy] |
| Throughput | 1000 RPS | [Strategy] |
| Storage | < 10GB/month | [Strategy] |

---

## Error Handling

| Error | Code | Response | Recovery |
|-------|------|----------|----------|
| [Error 1] | 400 | [Message] | [Action] |
| [Error 2] | 500 | [Message] | [Action] |

---

## Testing Strategy

| Type | Scope | Tools |
|------|-------|-------|
| Unit | Components | Jest/pytest |
| Integration | API | Supertest |
| E2E | Critical paths | Playwright |

---

## Observability

### Metrics
- `metric_name`: [Description]

### Logs
- [Log event 1]: [When logged]

### Traces
- [Span 1]: [What it traces]

---

## Rollout Plan

1. **Phase 1:** [Description] - Feature flag: `flag_name`
2. **Phase 2:** [Description] - % rollout
3. **Phase 3:** [Description] - GA

### Rollback Plan
[How to rollback if issues occur]

---

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## Related Documents

- Spec: [SPEC-XXX](link)
- ADRs: [ADR-XXX](link)

---

*Technical Design | [Feature Name] | Version 1.0*
```

---

## 4. Implementation Plan Templates

### 4.1 Standard Implementation Plan

```markdown
# IMPL-PLAN: [Feature Name]

## Metadata
| Field | Value |
|-------|-------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Author | [Name] |
| Status | Draft / Approved |

---

## Overview

**Scope:** [Brief description of what will be implemented]
**Complexity:** Low / Medium / High
**Est. Tokens:** ~XXXk

---

## Task Breakdown

### Wave 1: Foundation (Parallel)

| Task ID | Description | Files | Est. Tokens |
|---------|-------------|-------|-------------|
| TASK-001 | [Task description] | [files] | ~Xk |
| TASK-002 | [Task description] | [files] | ~Xk |

### Wave 2: Core (Sequential on Wave 1)

| Task ID | Description | Files | Depends On |
|---------|-------------|-------|------------|
| TASK-003 | [Task description] | [files] | TASK-001 |
| TASK-004 | [Task description] | [files] | TASK-002 |

### Wave 3: Integration (Sequential on Wave 2)

| Task ID | Description | Files | Depends On |
|---------|-------------|-------|------------|
| TASK-005 | [Task description] | [files] | TASK-003, TASK-004 |

### Wave 4: Polish (Parallel)

| Task ID | Description | Files | Est. Tokens |
|---------|-------------|-------|-------------|
| TASK-006 | Tests | [test files] | ~Xk |
| TASK-007 | Documentation | [doc files] | ~Xk |

---

## Dependency Graph

```
TASK-001 ──┬──→ TASK-003 ──┬──→ TASK-005 ──→ TASK-006
           │               │                     ↓
TASK-002 ──┴──→ TASK-004 ──┘              TASK-007
```

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | path/to/new/file.ts | [Description] |
| MODIFY | path/to/existing/file.ts | [What changes] |
| DELETE | path/to/old/file.ts | [Why deleted] |

---

## Quality Gates

- [ ] L1: All specs reviewed
- [ ] L2: Design approved
- [ ] L3: Implementation plan approved
- [ ] L4: Code implemented
- [ ] L5: Tests passing (>80% coverage)
- [ ] L6: Documentation updated

---

## Risks

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Strategy] |
| [Risk 2] | [Strategy] |

---

*Implementation Plan | [Feature Name] | Version 1.0*
```

---

## 5. Task File Templates

### 5.1 Standard Task

```markdown
# TASK-[ID]: [Title]

## Metadata
| Field | Value |
|-------|-------|
| Feature | [Feature Name] |
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Status | todo / in-progress / done |
| Complexity | Low / Medium / High |
| Est. Tokens | ~Xk |

---

## Objective

[1-2 sentences describing what this task accomplishes]

## Context

[Background information needed to complete this task]

## Requirements

From SPEC-XXX:
- FR-X: [Full requirement text]

## Acceptance Criteria

- [ ] AC-1: [Given-When-Then or checkbox item]
- [ ] AC-2: [Given-When-Then or checkbox item]
- [ ] AC-3: [Given-When-Then or checkbox item]

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | path/to/file.ts | [Description] |
| MODIFY | path/to/file.ts | [What to change] |

---

## Implementation Notes

[Any specific guidance for implementation]

## Dependencies

- Depends on: [TASK-XXX] (must be complete)
- Blocks: [TASK-YYY]

---

## Verification

```bash
# Commands to verify task completion
npm test -- --grep "feature"
npm run lint
```

---

*Task File | TASK-[ID] | [Feature Name]*
```

---

## 6. CLAUDE.md Templates

### 6.1 Project CLAUDE.md

```markdown
# CLAUDE.md - [Project Name]

## Project Overview

| Field | Value |
|-------|-------|
| Name | [Project Name] |
| Type | [Web App / API / CLI / Library] |
| Stack | [Main technologies] |

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | TypeScript 5.x |
| Framework | [Framework] |
| Database | [Database] |
| Testing | [Test framework] |

---

## Code Standards

### Naming Conventions
- Files: `kebab-case.ts`
- Components: `PascalCase.tsx`
- Functions: `camelCase`
- Constants: `SCREAMING_SNAKE_CASE`

### Code Style
- [Style rule 1]
- [Style rule 2]
- [Style rule 3]

---

## Directory Structure

```
src/
├── components/     # [Description]
├── lib/            # [Description]
├── services/       # [Description]
└── types/          # [Description]
```

---

## Patterns to Follow

### [Pattern Name]
```typescript
// Example of correct pattern
```

### [Pattern Name]
```typescript
// Example of correct pattern
```

---

## Anti-Patterns to Avoid

- [Anti-pattern 1]: [Why it's bad]
- [Anti-pattern 2]: [Why it's bad]

---

## Testing

| Type | Location | Command |
|------|----------|---------|
| Unit | `__tests__/` | `npm test` |
| Integration | `tests/integration/` | `npm run test:integration` |
| E2E | `tests/e2e/` | `npm run test:e2e` |

---

## Recent Decisions

- [ADR-XXX](link): [Brief description]
- [ADR-YYY](link): [Brief description]

---

## Current Focus

- Working on: [Feature/Task]
- Blocked by: [Blocker or "Nothing"]
- Next up: [Next feature/task]

---

*Last updated: YYYY-MM-DD*
```

---

## 7. Platform Engineering Templates

### 7.1 catalog-info.yaml (Backstage)

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: [service-name]
  description: [Service description]
  annotations:
    github.com/project-slug: '[org]/[repo]'
    backstage.io/techdocs-ref: dir:.
  tags:
    - [language]
    - [framework]
  links:
    - url: [documentation-url]
      title: Documentation
    - url: [dashboard-url]
      title: Grafana Dashboard
spec:
  type: service
  lifecycle: production
  owner: [team-name]
  system: [system-name]
  dependsOn:
    - component:default/[dependency]
  providesApis:
    - [api-name]
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: [api-name]
  description: [API description]
spec:
  type: openapi
  lifecycle: production
  owner: [team-name]
  definition:
    $text: ./openapi.yaml
```

### 7.2 Service Template Skeleton

```yaml
# scaffolder template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: [template-name]
  title: [Template Title]
  description: [Template description]
  tags:
    - [tag1]
    - recommended
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Details
      required:
        - name
        - owner
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z0-9-]+$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker

    - title: Infrastructure Options
      properties:
        includeDatabase:
          title: Include PostgreSQL
          type: boolean
          default: false

  steps:
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}

    - id: create-repo
      name: Create Repository
      action: github:repo:create
      input:
        repoUrl: github.com?owner=[org]&repo=${{ parameters.name }}

    - id: register
      name: Register Component
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.create-repo.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Repository
        url: ${{ steps.create-repo.output.remoteUrl }}
      - title: Open in Catalog
        icon: catalog
        entityRef: ${{ steps.register.output.entityRef }}
```

---

## 8. Observability Templates

### 8.1 OpenTelemetry Configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_mib: 2000
    spike_limit_mib: 400

  attributes:
    actions:
      - key: environment
        value: ${ENVIRONMENT}
        action: insert

exporters:
  otlp:
    endpoint: ${OTLP_ENDPOINT}
    headers:
      Authorization: Bearer ${OTLP_TOKEN}

  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp]

    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp, logging]
```

### 8.2 Structured Logging Configuration

```typescript
// logger.config.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
    bindings: () => ({
      service: process.env.SERVICE_NAME,
      version: process.env.SERVICE_VERSION,
      environment: process.env.NODE_ENV,
    }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: ['password', 'token', 'authorization', '*.password'],
    censor: '[REDACTED]',
  },
});

// Usage
export function createChildLogger(context: Record<string, unknown>) {
  return logger.child(context);
}
```

### 8.3 Metrics Definition

```typescript
// metrics.ts
import { Counter, Histogram, Gauge, Registry } from 'prom-client';

const registry = new Registry();

// Request metrics
export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5],
  registers: [registry],
});

export const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [registry],
});

// Business metrics
export const ordersCreated = new Counter({
  name: 'orders_created_total',
  help: 'Total number of orders created',
  labelNames: ['status', 'payment_method'],
  registers: [registry],
});

export const activeUsers = new Gauge({
  name: 'active_users',
  help: 'Number of currently active users',
  registers: [registry],
});

export { registry };
```

---

## Usage Notes

1. **Copy and customize** - These templates are starting points; adapt to your context
2. **Keep templates updated** - Review quarterly and update based on learnings
3. **Version control templates** - Store in `docs/templates/` or similar
4. **Link templates in process docs** - Make them easy to find

---

## Resources

- [README.md](README.md) - Overview and context
- [checklist.md](checklist.md) - Adoption checklist
- [examples.md](examples.md) - Real-world examples
- [llm-prompts.md](llm-prompts.md) - Effective prompts

---

*Templates Document | SDD Trends Implementation | Version 1.0*
