# FastAPI app with full metadata: title, description, version, auth docs, Swagger/Redoc URLs.
from fastapi import FastAPI

app = FastAPI(
    title="User Management API",
    description="""
## Overview
User management capabilities including creation, retrieval, update, and deletion.

## Authentication
All endpoints require Bearer token authentication.
```
Authorization: Bearer <your-token>
```

Obtain a token via `POST /auth/token`.

## Rate Limits
| Plan | Requests/hour |
|------|---------------|
| Free | 100           |
| Pro  | 10,000        |

## Errors
All errors follow [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807).
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "users", "description": "User management endpoints"},
        {"name": "auth", "description": "Authentication endpoints"},
    ],
)
