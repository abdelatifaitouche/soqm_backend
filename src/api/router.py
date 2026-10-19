from fastapi import APIRouter

from src.features.auth.routes.auth_routes import router as auth_router
from src.features.findings.api import finding_router, rca_router, action_router
from src.features.organizations.api import router as org_router
from src.features.soqm_engine.api import soqm_engine_router

router = APIRouter(prefix="/api/v1")

ROUTER_REGISTRY = {
    "engine_router": soqm_engine_router,
    "finding_router": finding_router,
    "rca_router": rca_router,
    "auth_router": auth_router,
    "action_router": action_router,
    "org": org_router,
}


for feature_router in ROUTER_REGISTRY.values():
    router.include_router(feature_router)
