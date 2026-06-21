from fastapi import APIRouter
from src.features.auth.routes.auth_routes import router as auth_router
from src.features.soqm_components.routes.routes import router as component_router
from src.features.organizations.routes.department_routes import router as dept_router
from src.features.quality_objectives.routes.routes import router as objective_router
from src.features.risks.routes.routes import router as risk_router
from src.features.risks.routes.response_routes import router as response_router

router = APIRouter(prefix="/api/v1")


router.include_router(auth_router)
router.include_router(component_router)
router.include_router(dept_router)
router.include_router(objective_router)
router.include_router(risk_router)
router.include_router(response_router)
