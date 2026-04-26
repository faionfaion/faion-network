# [API Name]

## Overview

Brief description: what the API does and who it is for.

## Authentication

```
Authorization: Bearer <token>
```

How to obtain a token: [link or steps].

Rate limits: Free tier — N req/hour. Pro tier — N req/hour.
Headers returned: `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Quick Start

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/users
```

## Endpoints

### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| POST | /users | Create user |
| GET | /users/{id} | Get user by ID |
| PATCH | /users/{id} | Update user fields |
| DELETE | /users/{id} | Delete user |

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 400 | Bad Request | Check request body against schema |
| 401 | Unauthorized | Verify your API key |
| 403 | Forbidden | Check required permissions |
| 404 | Not Found | Verify resource ID |
| 409 | Conflict | Resource already exists |
| 429 | Rate Limited | Back off and retry after X-RateLimit-Reset |
| 500 | Server Error | Contact support with the traceId |

## SDKs

- Python: `pip install example-api`
- JavaScript: `npm install @example/api-client`

## Changelog

### v1.1.0 (YYYY-MM-DD)

- Added user search endpoint
- Fixed pagination cursor bug

### v1.0.0 (YYYY-MM-DD)

- Initial release
