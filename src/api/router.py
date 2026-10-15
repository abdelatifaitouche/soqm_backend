from fastapi import APIRouter

from src.features.auth.routes.auth_routes import router as auth_router
from src.features.findings.api import finding_router
from src.features.organizations.routes.department_routes import router as dept_router
from src.features.organizations.routes.employee_routes import router as emp_router
from src.features.soqm_engine.api import soqm_engine_router

router = APIRouter(prefix="/api/v1")

ROUTER_REGISTRY = {
    "engine_router": soqm_engine_router,
    "finding_router": finding_router,
    "auth_router": auth_router,
    "org_router": dept_router,
    "employee_router": emp_router,
}


for feature_router in ROUTER_REGISTRY.values():
    router.include_router(feature_router)
