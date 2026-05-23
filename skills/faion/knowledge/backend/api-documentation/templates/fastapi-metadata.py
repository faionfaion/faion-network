# purpose: Template helper for API Documentation (fastapi-metadata.py).
# consumes: see content/02-output-contract.xml inputs for api-documentation
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
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
