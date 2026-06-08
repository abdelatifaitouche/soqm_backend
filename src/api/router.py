from fastapi import APIRouter
from src.features.auth.routes.auth_routes import router as auth_router
from src.features.soqm_components.routes.routes import router as component_router

router = APIRouter(prefix="/api/v1")


router.include_router(auth_router)
router.include_router(component_router)
