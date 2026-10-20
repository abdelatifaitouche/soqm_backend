from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.features.organizations.api.commands.writes import (
    CreateDepartmentRequest,
    UpdateDepartmentParentRequest,
    UpdateDepartmentRequest,
)
from src.features.organizations.api.dependencies import get_dept_queries, get_dept_uc
from src.features.organizations.application.dtos import (
    CreateDepartment,
    UpdateDepartment,
    UpdateDepartmentParent,
)
from src.features.organizations.application.usecases import DepartmentUC
from src.features.organizations.infra.queries import DepartmentQueryService

router = APIRouter(prefix="/departments")


@router.get("", status_code=status.HTTP_200_OK)
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


@router.get("/{department_id}", status_code=status.HTTP_200_OK)
async def get_department_details(
    department_id: UUID,
    queries: DepartmentQueryService = Depends(
        get_dept_queries,
    ),
):
    return await queries.get_department_details(department_id)


@router.patch("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_department(
    department_id: UUID,
    data: UpdateDepartmentRequest,
    uc: DepartmentUC = Depends(get_dept_uc),
):
    return await uc.update(
        dept_id=department_id,
        update_data=UpdateDepartment(name=data.name),
    )


@router.post("/{department_id}/change_parent", status_code=status.HTTP_204_NO_CONTENT)
async def change_dept_parent(
    department_id: UUID,
    data: UpdateDepartmentParentRequest,
    uc: DepartmentUC = Depends(get_dept_uc),
):
    return await uc.change_parent_dept(
        department_id,
        UpdateDepartmentParent(
            parent_id=data.parent_id,
        ),
    )


@router.delete("/{department_id}")
async def delete_department():
    return
