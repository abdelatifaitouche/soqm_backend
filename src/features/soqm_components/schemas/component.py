from pydantic import BaseModel
from uuid import UUID


class BaseComponent(BaseModel):
    id: UUID
    name: str
    isqm_reference: str

    model_config = {"from_attributes": True}
