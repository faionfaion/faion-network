# __faion_header_v1__
# purpose: FastAPI v1/v2 router scaffold with frozen v1 module
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#frozen-v1-module
# token-budget-impact: ~230 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"FastAPI v1/v2 router scaffold with frozen v1 module","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#frozen-v1-module","token_budget_impact":"~230 tokens when loaded as context"}}
from fastapi import APIRouter, FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

DEPRECATED_AT = "Wed, 01 Jan 2026 00:00:00 GMT"
SUNSET_AT = "Wed, 01 Jul 2026 00:00:00 GMT"  # >= 90 days after DEPRECATED_AT

app = FastAPI()
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")


class V1DeprecationMiddleware(BaseHTTPMiddleware):
    """Inject RFC 8594 deprecation headers on every /api/v1/* response."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if request.url.path.startswith("/api/v1/"):
            response.headers["Deprecation"] = DEPRECATED_AT
            response.headers["Sunset"] = SUNSET_AT
            response.headers["Link"] = '</api/v2>; rel="successor-version"'
        return response


@v1_router.get("/users", tags=["Users v1"])
async def get_users_v1():
    return {"format": "v1", "users": []}


@v2_router.get("/users", tags=["Users v2"])
async def get_users_v2():
    return {"data": {"users": []}, "meta": {}}


app.add_middleware(V1DeprecationMiddleware)
app.include_router(v1_router)
app.include_router(v2_router)
