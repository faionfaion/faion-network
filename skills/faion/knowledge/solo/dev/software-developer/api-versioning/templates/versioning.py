# versioning.py — FastAPI multi-version router with deprecation middleware
# Mount both routers on the FastAPI app:
#   app.include_router(v1)
#   app.include_router(v2)

from fastapi import APIRouter, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

DEPRECATED_AT = "Wed, 01 Jan 2026 00:00:00 GMT"
SUNSET_AT     = "Wed, 01 Jul 2026 00:00:00 GMT"

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")


class V1DeprecationMiddleware(BaseHTTPMiddleware):
    """Inject deprecation headers on all /api/v1/* responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if request.url.path.startswith("/api/v1/"):
            response.headers["Deprecation"] = DEPRECATED_AT
            response.headers["Sunset"] = SUNSET_AT
            response.headers["Link"] = '</api/v2>; rel="successor-version"'
        return response


# Shared service (one source of truth — both versions call this)
def _get_user_from_db(user_id: str) -> dict:
    """Fetch user. Replace with real service/repo call."""
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}


@v1.get("/users/{user_id}")
async def get_user_v1(user_id: str):
    """V1 flat response shape."""
    user = _get_user_from_db(user_id)
    return {"id": user["id"], "name": user["name"]}


@v2.get("/users/{user_id}")
async def get_user_v2(user_id: str):
    """V2 enveloped response shape with meta."""
    user = _get_user_from_db(user_id)
    return {"data": user, "meta": {"version": 2}}
