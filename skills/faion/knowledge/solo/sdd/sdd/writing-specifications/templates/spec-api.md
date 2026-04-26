# {api-name} API: Specification

<!-- SUMMARY: {One sentence describing what this API enables} -->

## Overview

**Base path:** `{/api/v1/resource}`
**Auth:** {Bearer token / API key / None}
**Format:** JSON request + response

## Endpoints

### {METHOD} {/path}

**Purpose:** {what this endpoint does}

**Request:**
```json
{
  "field_name": "string",
  "count": 0,
  "optional_field?": "string"
}
```

**Response 200:**
```json
{
  "id": "string",
  "result": "string",
  "created_at": "ISO-8601"
}
```

**Error responses:**

| Status | Code | Condition |
|--------|------|-----------|
| 400 | VALIDATION_ERROR | Missing required fields |
| 401 | UNAUTHORIZED | Invalid or missing auth token |
| 404 | NOT_FOUND | Resource does not exist |
| 422 | UNPROCESSABLE | Field validation failed |
| 500 | INTERNAL_ERROR | Unexpected server error |

**Acceptance Criteria:**
- Given: valid request with required fields
- When: POST {/path}
- Then: 200 with response body containing id

**Error AC:**
- Given: request with missing required field
- When: POST {/path}
- Then: 400 with VALIDATION_ERROR and field-level error details

---

### {METHOD} {/path/:id}

**Purpose:** {what this endpoint does}

**Path params:**
- `id` (string, required) — {description}

**Response 200:**
```json
{
  "id": "string",
  "status": "active | inactive"
}
```

## Rate Limits

| Tier | Requests/minute | Burst |
|------|-----------------|-------|
| Free | 60 | 10 |
| Pro | 600 | 100 |

## Non-Functional Requirements

- p99 latency: < {X}ms
- Availability: {X}%
- Max payload size: {X}MB
