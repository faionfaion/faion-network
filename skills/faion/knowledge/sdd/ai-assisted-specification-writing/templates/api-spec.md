<!--
purpose: API specification skeleton — base URLs, auth, rate limits, endpoints, error codes
consumes: endpoint inventory + auth decision + rate-limit policy
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-900 tokens when loaded as context
variables:
  - name: api_name
    type: string
    required: true
    description: The API's name as callers will refer to it in support threads and in their own code. Match the SDK package name if one exists; two names for one API doubles your search surface.
  - name: prod_base_url
    type: string
    required: true
    description: Production base URL including the version segment. Version in the path, not only in a header - the first thing an integrator copies is this line, and it has to still work next year.
  - name: staging_base_url
    type: string
    required: true
    description: Staging base URL. If there is no staging environment, say so here explicitly rather than omitting the line - integrators will otherwise test against production, and you will find out how.
  - name: auth_method
    type: text
    required: true
    description: How a caller authenticates, in one or two sentences - the scheme, where the credential goes, and how long it lives. Expiry is the detail people leave out and then get paged about.
  - name: free_tier_rpm
    type: integer
    required: true
    description: Requests per minute allowed on the free tier. A real number - limits described as "reasonable" get discovered by being hit, in production, at somebody else's peak hour.
  - name: pro_tier_rpm
    type: integer
    required: true
    description: Requests per minute on the paid tier. The gap between this and the free number is the upgrade argument, so make sure it is one you would actually make out loud.
-->
# {{api_name}} API Specification

## Overview
[Brief description of what this API does]

## Base URL
- Production: {{prod_base_url}}
- Staging: {{staging_base_url}}

## Authentication
{{auth_method}}

## Rate Limits

| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | {{free_tier_rpm}} | [N] |
| Pro | {{pro_tier_rpm}} | [N] |

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
