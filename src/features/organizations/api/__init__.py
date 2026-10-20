from fastapi import APIRouter

from .routes.department_routes import router as dept_router
from .routes.employee_routes import router as emp_router

router = APIRouter(prefix="/org")

router.include_router(dept_router)
router.include_router(emp_router)
