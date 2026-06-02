from src.core.permissions import Permissions
import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.features.auth.models.permission import Permission


def get_all_permissions() -> list[tuple[str, str]]:
    all_perms = []

    for feature_class in vars(Permissions).values():
        if inspect.isclass(feature_class):
            for val in vars(feature_class).values():
                if isinstance(val, tuple) and len(val) == 2:
                    all_perms.append(val)

    return all_perms


async def seed_permissions(session: AsyncSession):

    all_perms = get_all_permissions()

    data_to_insert = [{"resource": r, "action": a} for r, a in all_perms]

    result = await session.execute(
        pg_insert(Permission).values(data_to_insert).on_conflict_do_nothing()
    )

    return result
