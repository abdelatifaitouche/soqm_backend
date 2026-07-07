import pytest
from src.core.ordering import apply_ordering, OrderDirection, OrderBy
from sqlalchemy import select, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class TestModel(Base):
    __tablename__ = "test_model"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[str] = mapped_column(String)
    created_at: Mapped[int] = mapped_column(Integer, default=1)


@pytest.fixture
def stmt():
    return select(TestModel.score)


@pytest.fixture
def order():
    return OrderBy(column="score")


class TestOrderingMethod:
    def test_basic_output(self, stmt, order):
        stmt = apply_ordering(TestModel, stmt, order)
        logger.info(stmt)
