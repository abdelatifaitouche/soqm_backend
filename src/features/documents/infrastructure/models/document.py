from src.infra.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Document(Base):
    __tablename__ = "documents"

    name

    file_name
