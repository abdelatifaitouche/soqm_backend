from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.features.soqm_components.models.soqm_component import SOQMComponent
from sqlalchemy import select, delete


async def check_db_state(session: AsyncSession) -> bool:
    stmt = select(SOQMComponent)

    result = await session.execute(stmt)

    count = result.scalars() or 0

    return count == 8


def check_data_validity(components: list[dict]):

    if len(components) != 8:
        raise ValueError(f"Expected 8 components, got {len(components)}")

    ids = set()
    names = set()
    display_orders = set()
    for component in components:
        order = component.get("display_order")

        if not order or not isinstance(order, int) or order not in range(1, 9):
            raise ValueError("Display order must be an integer and with range(1-8)")

        if not component.get("name"):
            raise ValueError("Each component must have a name")

        if order in display_orders:
            raise ValueError("Display Orders must be unique and withing the range(1-8)")

        if component.get("name") in names:
            raise ValueError("Component names must be unique")

        display_orders.add(order)
        names.add(component.get("name"))

    return True


async def seed_components(data: list[dict], session: AsyncSession, force: bool = False):

    try:
        check_data_validity(data)
    except ValueError as e:
        return {
            "success": False,
            "message": f"seed data validation failed: {e}",
            "created": 0,
            "skipped": 0,
        }

    exists = await check_db_state(session)

    if exists and not force:
        return {
            "success": True,
            "message": "Components already seeded (skipping)",
            "created": 0,
            "skipped": 8,
        }

    if exists and force:
        await session.execute(delete(SOQMComponent))
        await session.commit()

    try:
        result = await session.execute(
            pg_insert(SOQMComponent).values(data).on_conflict_do_nothing()
        )
        await session.commit()

        created = result.rowcount
        skipped = 8 - created

        return {
            "success": True,
            "message": f"Seeding completed : {created} created , {skipped} Skipped",
            "created": created,
            "skipped": skipped,
        }
    except Exception as e:
        await session.rollback()
        raise e
