from pydantic import BaseModel


class ComponentFilters(BaseModel):
    is_active: bool | None = None
