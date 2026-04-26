"""
FastAPI versioned router setup.
v1 routes are FROZEN — do not modify response shape.
v2 lives in a separate module; v1 is read-only once published.
"""
from fastapi import FastAPI, APIRouter

app = FastAPI()

# v1 router — frozen after publication
v1_router = APIRouter(prefix="/api/v1")

# v2 router — new structure
v2_router = APIRouter(prefix="/api/v2")


@v1_router.get("/users", tags=["Users v1"])
async def get_users_v1():
    """v1 response shape — never change this once consumers depend on it."""
    return {
        "format": "v1",
        "users": [],
        "_warnings": [
            {
                "code": "DEPRECATED_API",
                "message": "v1 API deprecated. Migrate to /api/v2/users by 2026-07-01.",
                "documentation": "https://api.example.com/docs/migration/v1-to-v2",
            }
        ],
    }


@v2_router.get("/users", tags=["Users v2"])
async def get_users_v2():
    """v2 response shape — envelope changed, richer metadata."""
    return {
        "data": {"users": []},
        "meta": {"total": 0, "page": 1},
    }


app.include_router(v1_router)
app.include_router(v2_router)
