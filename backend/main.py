"""
Focus Friend - Main FastAPI Application Server.
Provides the scalable REST API and serves the modular Neo-Brutalist frontend.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.api.router import api_router
from backend.middleware.timing_middleware import TimingMiddleware
from backend.middleware.error_handler import register_exception_handlers
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle management."""
    logger.info("==================================================")
    logger.info(f"⚡ {settings.app_name.upper()}: LOCAL-FIRST EXECUTIVE ASSISTANT")
    logger.info("🎨 Aesthetic Neo-Brutalism UI & Scalable API v1")
    logger.info(f"🚀 Running locally at: http://{settings.host}:{settings.port}")
    logger.info(f"📚 OpenAPI Interactive Docs at: http://{settings.host}:{settings.port}/docs")
    logger.info(f"🔒 100% Private - Zero Cloud Telemetry")
    logger.info("==================================================")
    yield
    logger.info(f"Shutting down {settings.app_name} server.")


tags_metadata = [
    {
        "name": "Distillation",
        "description": "Core Signal extraction endpoints that distill walls of text into Tone, Timeline, and Task."
    },
    {
        "name": "Health & Status",
        "description": "Liveness probes, daemon connectivity verification, and engine state."
    },
    {
        "name": "Models",
        "description": "Enumeration of local open-weight model weights installed on the machine."
    },
    {
        "name": "Presets",
        "description": "Standardized communication overload scenarios for ADHD testing and quick evaluation."
    }
]

app = FastAPI(
    title=settings.app_name,
    description=(
        "A minimalist, local-first executive function assistant that distills walls of text "
        "into Tone, Timeline, and Task. Built for ADHD and neurodivergent professionals."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Global Timing & Request Logging Middleware
app.add_middleware(TimingMiddleware)

# Global Error Handlers
register_exception_handlers(app)

# CORS Configuration
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount REST API (v1)
app.include_router(api_router)

# Mount Modular Frontend
if settings.frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(settings.frontend_dir), html=True), name="frontend")
