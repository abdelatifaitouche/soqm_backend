from dataclasses import dataclass
from uuid import UUID, uuid4
from src.features.organizations.enums.employee import EmployeeState, EmployeeLevel
from src.core.exceptions import ValidationError
from src.features.organizations.domain.department import DeptCompact


@dataclass
class Employee:
    id: UUID
    first_name: str
    last_name: str
    department_id: UUID
    job_title: str

    level: str = EmployeeLevel.JUNIOR.value
    status: str = EmployeeState.ACTIVE.value
    user_id: UUID | None = None

    @classmethod
    def add_profile(
        cls,
        first_name: str,
        last_name: str,
        department_id: UUID,
        job_title: str,
        level: str,
        user_id: UUID | None = None,
    ) -> "Employee":

        if not first_name or first_name.strip() == "":
            raise ValidationError(
                message="Invalid first name for employee",
                details={"first_name": first_name},
            )

        if not last_name or last_name.strip() == "":
            raise ValidationError(
                message="Invalid last name for employee",
                details={"last_name": last_name},
            )

        employee = cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            user_id=user_id,
            level=level,
            job_title=job_title,
            status=EmployeeState.ACTIVE.value,
        )
        return employee
