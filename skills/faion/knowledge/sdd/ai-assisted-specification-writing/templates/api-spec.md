# [API_NAME] API Specification

## Overview
[Brief description of what this API does]

## Base URL
- Production: https://api.example.com/v1
- Staging: https://api-staging.example.com/v1

## Authentication
[Bearer token / API key / OAuth — describe method]

## Rate Limits
| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 60 | 1,000 |
| Pro | 600 | 50,000 |

## Endpoints

### [METHOD] /path/to/endpoint

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
