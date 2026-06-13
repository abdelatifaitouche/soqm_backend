from pydantic import BaseModel


class ComponentFilters(BaseModel):
    status: str | None = None
