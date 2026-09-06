from fastapi import APIRouter

from src.features.soqm_engine.api import soqm_engine_router

router = APIRouter(prefix="/api/v1")


router.include_router(soqm_engine_router)
