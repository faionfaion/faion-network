<!--

purpose: API specification skeleton — base URLs, auth, rate limits, endpoints, error codes
consumes: endpoint inventory + auth decision + rate-limit policy
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-900 tokens when loaded as context
-->


# <api_name> API Specification

## Overview
[Brief description of what this API does]

## Base URL
- Production: <prod_base_url>
- Staging: <staging_base_url>

## Authentication
<auth_method>

## Rate Limits

| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | <free_tier_rpm> | <free> |
| Pro | <pro_tier_rpm> | <pro> |

## Endpoints

### <method> /path/to/endpoint

**Description:** [What this endpoint does]

**Request:**
```json
{
  "field1": "string",
  "field2": 123
}
```

**Responses:**

200 OK:
```json
{
  "id": "abc123",
  "created_at": "2026-01-20T10:00:00Z"
}
```

400 Bad Request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field 'field1' is required"
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

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| RATE_LIMITED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |
