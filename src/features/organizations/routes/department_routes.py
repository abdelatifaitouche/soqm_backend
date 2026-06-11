from fastapi import APIRouter, Depends
from uuid import UUID
from src.infra.db.uow import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.organizations.repositories.department_repository import (
    DepartmentRepository,
)
from src.features.organizations.services.department_service import DepartmentService
from src.features.organizations.schemas.department import Department, CreateDepartment
from src.features.organizations.mappers.DepartmentMapper import DepartmentMapper
from src.features.organizations.domain.department import Department as Entity

router = APIRouter(prefix="/organization")


def get_service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    repo: DepartmentRepository = DepartmentRepository(db)
    return DepartmentService(repo)


@router.get("/departments")
async def list_depts(
    service: DepartmentService = Depends(get_service),
):
    depts: list[Entity] = await service.list()
    return [Department.model_validate(dept) for dept in depts]


@router.post("/departments/")
async def create(
    data: CreateDepartment,
    service: DepartmentService = Depends(get_service),
):
    dept: Entity = await service.create(DepartmentMapper.from_create(data))
    return Department.model_validate(dept)


@router.get("/departments/{department_id}")
async def get_by_id(
    department_id: str,
    service: DepartmentService = Depends(get_service),
):
    dept: Entity | None = await service.get_by_id(UUID(department_id))
    return Department.model_validate(dept)


@router.delete("/departments/{department_id}/")
async def delete():
    return
