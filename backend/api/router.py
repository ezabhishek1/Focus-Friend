"""
Focus Friend - API V1 Router Aggregator.
Aggregates all version 1 endpoints under the /api/v1 prefix.
"""

from fastapi import APIRouter
from backend.api.endpoints.extraction import router as extraction_router
from backend.api.endpoints.health import router as health_router
from backend.api.endpoints.models import router as models_router
from backend.api.endpoints.presets import router as presets_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(extraction_router)
api_router.include_router(health_router)
api_router.include_router(models_router)
api_router.include_router(presets_router)
