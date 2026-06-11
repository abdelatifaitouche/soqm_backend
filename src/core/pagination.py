from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    page: int = 1

    @property
    def offset(self):
        return self.limit * (self.page - 1)
