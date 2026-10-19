from fastapi import APIRouter

from .routes.department_routes import router as dept_router

router = APIRouter(prefix="/org")

router.include_router(dept_router)
