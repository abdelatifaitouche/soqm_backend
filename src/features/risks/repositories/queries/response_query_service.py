from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select, func
from sqlalchemy.orm import joinedload
from typing import Any
from src.features.risks.models.risk_response import (
    RiskResponse as ResponseDB,
    RESPONSE_ORDER_FIELDS,
)
from src.features.risks.filters.response_filters import ResponseFilters
from src.core.pagination import Pagination
from src.infra.db.pagination import apply_pagination
from src.core.ordering import OrderBy, apply_ordering, resolve_order_column
from src.features.organizations.models.employee import Employee as EmployeeDB
from src.features.risks.services.response_dto import (
    ResponseList,
    ResponseOwner,
    PaginatedResponse,
    ResponseDetails,
)
from uuid import UUID


class ResponseQueryService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def apply_filters(self, stmt: Select[Any], filters: ResponseFilters) -> Select[Any]:

        if filters.status:
            stmt = stmt.where(ResponseDB.status == filters.status)

        if filters.created_by:
            stmt = stmt.where(ResponseDB.created_by == filters.created_by)

        if filters.assigned_employee:
            stmt = stmt.where(ResponseDB.owner == filters.assigned_employee)

        if filters.frequency:
            stmt = stmt.where(ResponseDB.frequency == filters.frequency)

        if filters.execution_type:
            stmt = stmt.where(ResponseDB.execution_type == filters.execution_type)

        return stmt

    async def list(
        self, pagination: Pagination, filters: ResponseFilters, order: OrderBy
    ) -> PaginatedResponse:

        total_query = select(func.count()).select_from(ResponseDB)
        total: int | None = await self.db.scalar(total_query)

        if not total:
            return PaginatedResponse(
                total=0,
                page=0,
                size=0,
                items=[],
            )

        stmt = select(
            ResponseDB.id,
            ResponseDB.response_name,
            ResponseDB.response_ref,
            ResponseDB.status,
            ResponseDB.response_type,
            ResponseDB.frequency,
            ResponseDB.execution_type,
            EmployeeDB.first_name,
            EmployeeDB.last_name,
        ).join(ResponseDB.assigned_employee)
        stmt = self.apply_filters(stmt, filters)

        column = resolve_order_column(
            ResponseDB,
            order.column,
            RESPONSE_ORDER_FIELDS,
        )

        stmt = apply_ordering(stmt, column, direction=order.direction)

        stmt = apply_pagination(stmt, pagination)

        results = (await self.db.execute(stmt)).mappings().all()

        responses: list[ResponseList] = [
            ResponseList(
                id=resp["id"],
                response_name=resp["response_name"],
                response_ref=resp["response_ref"],
                status=resp["status"],
                response_type=resp["response_type"],
                frequency=resp["frequency"],
                execution_type=resp["execution_type"],
                owner=ResponseOwner(
                    first_name=resp["first_name"],
                    last_name=resp["last_name"],
                ),
            )
            for resp in results
        ]

        return PaginatedResponse(
            total=total,
            page=pagination.page,
            size=pagination.limit,
            items=responses,
        )

    async def get_response_details(self, response_id: UUID):
        from src.features.soqm_components.models.soqm_component import SOQMComponent
        from src.features.organizations.models.employee import Employee

        stmt = (
            select(
                ResponseDB,
                SOQMComponent.id,
                SOQMComponent.name,
                SOQMComponent.description,
                SOQMComponent.display_order,
            )
            .options(
                joinedload(ResponseDB.assigned_employee).joinedload(Employee.department)
            )
            .join(
                SOQMComponent,
                SOQMComponent.id == ResponseDB.component_id,
            )
            .where(
                ResponseDB.id == response_id,
            )
        )
        result = (await self.db.execute(stmt)).mappings().one()

        return result
