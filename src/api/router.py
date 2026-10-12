from fastapi import APIRouter

from src.features.soqm_engine.api import soqm_engine_router
from src.features.findings.api import finding_router
from src.features.auth.routes.auth_routes import router as auth_router


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(soqm_engine_router)
router.include_router(finding_router)
