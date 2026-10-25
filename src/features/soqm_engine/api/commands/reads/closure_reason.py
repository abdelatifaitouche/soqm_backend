from pydantic import BaseModel


class ClosureReasonResponse(BaseModel):
    code: str
    context: str
    display_text: str

    model_config = {"from_attributes": True}
