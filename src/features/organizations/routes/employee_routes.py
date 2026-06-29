from fastapi import APIRouter, Depends
from src.features.organizations.employee_dependencies import get_service
from src.features.organizations.schemas.employee import CreateEmployee
from src.features.organizations.services.employee_service import EmployeeService
from src.features.organizations.schemas.employee import (
    Employee,
    EmployeeList,
    EmployeeOption,
    EmployeeProfile,
)
from src.features.auth.security.dependencies import require_auth
from src.features.organizations.filters.employee_filters import EmployeeFilters
from src.core.pagination import Pagination

router = APIRouter(prefix="/employee")


@router.post("/")
async def create_employee(
    data: CreateEmployee,
    service: EmployeeService = Depends(get_service),
):

    employee = await service.create_employee(data)
    return Employee.model_validate(employee)


@router.get("")
async def list_employees(
    pagination: Pagination = Depends(),
    filters: EmployeeFilters = Depends(),
    service: EmployeeService = Depends(get_service),
):
    employees = await service.list_employees(pagination, filters)
    return (
        [EmployeeList.model_validate(emp) for emp in employees] if employees else None
    )


@router.get("/options")
async def list_options(
    service: EmployeeService = Depends(get_service),
):
    options = await service.list_options()
    return [EmployeeOption.model_validate(opt) for opt in options]


@router.get("/profile/me")
async def get_my_profile(
    creds=Depends(require_auth),
    service: EmployeeService = Depends(get_service),
):
    profile = await service.get_user_profile(creds.get("sub"))
    return EmployeeProfile.model_validate(profile)


@router.get("/{employee_id}")
async def get_employee():
    return


@router.patch("/{employee_id}/")
async def update():
    return
