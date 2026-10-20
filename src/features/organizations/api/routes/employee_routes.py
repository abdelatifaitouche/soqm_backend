from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from src.features.organizations.api.dependencies import get_emp_uc, get_emp_queries
from src.features.organizations.application.dtos import CreateEmployee, UpdateEmployee
from src.features.organizations.api.commands.writes.employee_writes import (
    CreateEmployeeRequest,
    UpdateEmployeeRequest,
)
from src.features.organizations.api.commands.reads import (
    EmployeeCreatedResponse,
    EmployeeReadResponse,
)
from src.features.organizations.application.usecases import EmployeeUC
from src.features.organizations.infra.queries import EmployeeQueryService
from src.features.organizations.application.filters import EmployeeFilters
from src.core.pagination import Pagination

router = APIRouter(prefix="/employee")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeCreatedResponse,
)
async def create_employee(
    data: CreateEmployeeRequest,
    uc: EmployeeUC = Depends(get_emp_uc),
):
    emp_id = await uc.create(
        CreateEmployee(
            first_name=data.first_name,
            last_name=data.last_name,
            department_id=data.department_id,
            job_title=data.job_title,
            level=data.level,
            user_id=data.user_id,
        )
    )

    return EmployeeCreatedResponse(id=emp_id)


@router.patch("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee(
    employee_id: UUID,
    data: UpdateEmployeeRequest,
    uc: EmployeeUC = Depends(get_emp_uc),
):
    return await uc.update(
        emp_id=employee_id,
        update_data=UpdateEmployee(
            first_name=data.first_name,
            last_name=data.last_name,
            job_title=data.job_title,
        ),
    )


@router.post("/{employee_id}/block", status_code=status.HTTP_204_NO_CONTENT)
async def block_employee(
    employee_id: UUID,
    uc: EmployeeUC = Depends(get_emp_uc),
):
    return await uc.block(employee_id)


@router.post("/{employee_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_employee(
    employee_id: UUID,
    uc: EmployeeUC = Depends(get_emp_uc),
):
    return await uc.activate(employee_id)


@router.get(
    "/{employee_id}",
    response_model=EmployeeReadResponse,
    status_code=status.HTTP_200_OK,
)
async def get_employee_details(
    employee_id: UUID, queries: EmployeeQueryService = Depends(get_emp_queries)
):
    emp = await queries.get_employee_details(employee_id)

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": "Employee Not Found",
            },
        )

    return EmployeeReadResponse.model_validate(emp)


@router.get("")
async def list_employees(
    pagination: Pagination = Depends(),
    filters: EmployeeFilters = Depends(),
    queries: EmployeeQueryService = Depends(get_emp_queries),
):
    return await queries.list(pagination, filters)


@router.get("/employees/options")
async def list_options(
    queries: EmployeeQueryService = Depends(
        get_emp_queries,
    ),
):
    """this endpoint needs to be fixed its f***** ugly"""
    return await queries.list_options()
