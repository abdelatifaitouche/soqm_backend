from fastapi import APIRouter
from .routes.component_routes import router as component_router
from .routes.risk_routes import router as risk_router
from .routes.response_routes import router as response_router
from .routes.objective_routes import router as objective_router


soqm_engine_router = APIRouter(prefix="/soqm", tags=["Isqm engine"])

soqm_engine_router.include_router(component_router)
soqm_engine_router.include_router(risk_router)
soqm_engine_router.include_router(response_router)
soqm_engine_router.include_router(objective_router)
