from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.features.organizations.api.commands.writes import CreateDepartmentRequest
from src.features.organizations.api.dependencies import get_dept_queries, get_dept_uc
from src.features.organizations.application.dtos import CreateDepartment
from src.features.organizations.application.usecases import DepartmentUC
from src.features.organizations.infra.queries import DepartmentQueryService

router = APIRouter(prefix="/departments")


@router.get("")
async def list_depts(queries: DepartmentQueryService = Depends(get_dept_queries)):
    return await queries.list()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_department(
    department_data: CreateDepartmentRequest,
    uc: DepartmentUC = Depends(get_dept_uc),
):
    return await uc.create(
        data=CreateDepartment(
            name=department_data.name,
            parent_id=department_data.parent_id,
        ),
    )


@router.get("/{department_id}")
async def get_department_details(
    department_id: UUID,
    queries: DepartmentQueryService = Depends(
        get_dept_queries,
    ),
):
    return await queries.get_department_details(department_id)
