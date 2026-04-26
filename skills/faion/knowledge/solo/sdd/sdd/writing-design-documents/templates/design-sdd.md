# {feature-NNN-name}: Design

<!-- SUMMARY: {One sentence describing the technical approach} -->

## Metadata

| Field | Value |
|-------|-------|
| **Feature** | {feature-NNN-name} |
| **Spec** | `.aidocs/{status}/{feature}/spec.md` |
| **Status** | draft / review / approved |
| **Covers FR** | FR-1, FR-2, FR-3 |

## Overview

{2-3 paragraphs: problem → solution approach → scope of this design}

**Not in scope:** {what this design does NOT cover}

## Architecture

### Component Diagram

```
[Client] → [API Layer] → [Service Layer] → [Data Layer]
                ↓               ↓
          [Auth Middleware]  [External API]
```

### Data Flow

1. {Step 1: request enters at X}
2. {Step 2: validated at Y}
3. {Step 3: processed by Z}
4. {Step 4: stored in W}
5. {Step 5: response returned}

## Component Design

### {ComponentName}

**Responsibility:** {one sentence}
**Inputs:** {what it receives}
**Outputs:** {what it produces}
**FR coverage:** FR-{X}

**Key design decisions:** see AD-{X} below.

### {ComponentName}

**Responsibility:** {one sentence}
**Inputs:** {what it receives}
**Outputs:** {what it produces}
**FR coverage:** FR-{Y}

## API Contracts

### {METHOD} {/path}

**Request:**
```json
{
  "field": "type"
}
```

**Response 200:**
```json
{
  "id": "string",
  "status": "string"
}
```

**Errors:** 400 VALIDATION_ERROR | 401 UNAUTHORIZED | 404 NOT_FOUND

## Data Models

### {ModelName}

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | no | Primary key |
| `name` | string(255) | no | {description} |
| `status` | enum | no | active \| inactive |
| `created_at` | timestamp | no | UTC |

## Architecture Decisions

### AD-1: {Decision title}

**Options considered:**
- Option A: {description} — Pros: {X}. Cons: {Y}.
- Option B: {description} — Pros: {X}. Cons: {Y}.

**Decision:** Option {X}

**Rationale:** {Why this option was chosen — 2-3 sentences}

**Trade-offs accepted:** {What we give up}

### AD-2: {Decision title}

**Options considered:**
- Option A: {description}
- Option B: {description}

**Decision:** Option {X}

**Rationale:** {Why}

**Trade-offs accepted:** {Trade-offs}

## Open Questions

| # | Question | Impact | Owner |
|---|----------|--------|-------|
| 1 | {question that blocks implementation} | {which component is blocked} | {person/role} |

## Out of Scope

- {Explicit exclusion — prevents gold-plating}
- {Explicit exclusion}
