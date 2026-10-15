from uuid import UUID

from pydantic import BaseModel


class ReadComponentDetails(BaseModel):
    id: UUID
    name: str
    isqm_reference: str
    status: str
    display_order: int

    description: str
    status: str

    model_config = {"from_attributes": True}
