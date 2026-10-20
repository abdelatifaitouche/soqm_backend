from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from src.core.exceptions import ValidationError
from src.features.organizations.enums.employee import EmployeeLevel, EmployeeState


@dataclass
class Employee:
    id: UUID
    first_name: str
    last_name: str
    department_id: UUID
    job_title: str
    created_at: datetime
    updated_at: datetime

    level: str = EmployeeLevel.JUNIOR.value
    status: str = EmployeeState.ACTIVE.value
    user_id: UUID | None = None

    @classmethod
    def create(
        cls,
        *,
        first_name: str,
        last_name: str,
        department_id: UUID,
        job_title: str,
        level: str,
        user_id: UUID | None = None,
    ) -> "Employee":

        cls._validate(first_name, last_name, job_title)

        employee = cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            user_id=user_id,
            level=level,
            job_title=job_title,
            status=EmployeeState.ACTIVE.value,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return employee

    @staticmethod
    def _validate(first_name: str, last_name: str, job_title: str) -> None:
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
        if not job_title or job_title.strip() == "":
            raise ValidationError(
                message="Invalid job title for employee",
                details={"job title": job_title},
            )

    def update(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        job_title: str | None = None,
    ):

        if first_name and first_name.strip() != "":
            self.first_name = first_name

        if last_name and last_name.strip() != "":
            self.last_name = last_name

        if job_title:
            self.job_title = job_title

        self.updated_at = datetime.now()

    def change_department(self, dept_id: UUID):
        if dept_id != self.department_id:
            self.department_id = dept_id
            self.updated_at = datetime.now()

    def deactivate(self):
        if self.status != EmployeeState.IN_ACTIVE.value:
            self.status = EmployeeState.IN_ACTIVE.value
            self.updated_at = datetime.now()

    def activate(self):
        if self.status != EmployeeState.ACTIVE.value:
            self.status = EmployeeState.ACTIVE.value
            self.updated_at = datetime.now()
