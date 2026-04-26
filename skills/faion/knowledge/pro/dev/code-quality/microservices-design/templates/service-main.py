"""FastAPI microservice entrypoint with lifespan, health check, and versioned API router."""
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI

health_router = APIRouter()


@health_router.get("/health")
async def health():
    # Extend to check DB/broker connectivity
    return {"status": "ok"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # await init_db()
    # await init_message_bus()
    yield
    # Shutdown
    # await close_message_bus()
    # await close_db()


app = FastAPI(
    title="<Service Name>",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router, tags=["health"])
# app.include_router(router, prefix="/api/v1", tags=["<domain>"])
