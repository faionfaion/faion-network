# purpose: FastAPI app entry — lifespan, router includes, error handler.
# consumes: settings (pydantic-settings), routers, lifespan deps.
# produces: app = FastAPI(...) importable as `app.main:app`.
# depends-on: fastapi, pydantic-settings.
# token-budget-impact: ~40 lines.
"""
FastAPI application entry point.
Adjust imports, router includes, and middleware to your project structure.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, close_db
from app.routers import users  # add more routers here


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, release on shutdown."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production API",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}
