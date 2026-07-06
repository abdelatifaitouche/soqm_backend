from pydantic import BaseModel, field_validator
from uuid import UUID


class ComponentOption(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class BaseComponent(BaseModel):
    id: UUID
    name: str
    isqm_reference: str
    status: str
    display_order: int
    model_config = {"from_attributes": True}


class Component(BaseComponent):
    description: str
    status: str

    model_config = {"from_attributes": True}


class CreateComponent(BaseModel):
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


class ReadComponent(BaseModel):
    pass


class UpdateComponent(BaseModel):
    name: str | None = None
    description: str | None = None
    isqm_reference: str | None = None
    display_order: int | None = None
