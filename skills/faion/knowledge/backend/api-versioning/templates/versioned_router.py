# __faion_header_v1__
# purpose: FastAPI v1/v2 router scaffold with frozen v1 module
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#additive-first
# faion_header_json: {"__faion_header__":{"purpose":"FastAPI v1/v2 router scaffold with frozen v1 module","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#additive-first","token_budget_impact":"~150 tokens when loaded"}}
from fastapi import FastAPI, APIRouter

app = FastAPI()
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")


@v1_router.get("/users", tags=["Users v1"])
async def get_users_v1():
    return {"format": "v1", "users": []}


@v2_router.get("/users", tags=["Users v2"])
async def get_users_v2():
    return {"data": {"users": []}, "meta": {}}


app.include_router(v1_router)
app.include_router(v2_router)
