from pydantic import BaseModel, field_validator


class CreateComponentRequest(BaseModel):
    name: str
    description: str
    isqm_reference: str
    display_order: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if value.strip() == "" or len(value) == 0:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("display_order")
    @classmethod
    def validate_display_order(cls, value: int) -> int:
        if value <= 0 or value > 8:
            raise ValueError("Display Order must but bound between 1-8")
        return value

    @field_validator("isqm_reference")
    @classmethod
    def validate_isqm_ref(cls, value: str) -> str:
        if value.strip() == "" or len(value) == 0:
            raise ValueError("ISQM reference cannot be empty")
        return value


class UpdateComponentRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    isqm_reference: str | None = None
    display_order: int | None = None
