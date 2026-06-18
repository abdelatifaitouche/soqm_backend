from dataclasses import dataclass
import uuid
from src.core.exceptions import ValidationError


@dataclass
class RiskAuditLog:
    id: uuid.UUID
    risk_id: uuid.UUID
    field_changed: str
    old_value: str
    new_value: str
    change_comment: str
    changed_by: uuid.UUID

    @staticmethod
    def create(
        risk_id: uuid.UUID,
        field_changed: str,
        old_value: str,
        new_value: str,
        change_comment: str,
        changed_by: uuid.UUID,
    ) -> "RiskAuditLog":
        """Factory method for creating the risk audit log object"""

        if field_changed.strip() == "":
            raise ValidationError(
                message="field changed cannot be empty",
            )

        if old_value.strip() == "":
            raise ValidationError(
                message="Empty Old Value",
                details={
                    "old_value": old_value,
                },
            )

        if new_value.strip() == "":
            raise ValidationError(
                message="Empty New Value",
                details={
                    "new_value": new_value,
                },
            )

        if old_value.strip().lower() == new_value.strip().lower():
            raise ValidationError(
                message="new value is the same as the old value",
                details={
                    "new_value": new_value,
                    "old_value": old_value,
                },
            )

        return RiskAuditLog(
            id=uuid.uuid4(),
            risk_id=risk_id,
            field_changed=field_changed,
            old_value=old_value,
            new_value=new_value,
            change_comment=change_comment,
            changed_by=changed_by,
        )
