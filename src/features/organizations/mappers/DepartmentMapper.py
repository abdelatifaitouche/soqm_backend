from src.features.organizations.domain.department import Department as Entity
from src.features.organizations.schemas.department import Department, CreateDepartment


class DepartmentMapper:
    @staticmethod
    def from_create(data: CreateDepartment) -> Entity:
        return Entity(
            name=data.name,
            parent_dept=data.parent_dept,
        )
