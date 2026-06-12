from src.features.soqm_components.schemas.component import (
    CreateComponent,
    UpdateComponent,
)
from src.features.soqm_components.domain.component import (
    CreateComponent as CreateComponentEntity,
    UpdateComponent as UpdateEntity,
)


class ComponentMapper:
    @staticmethod
    def from_create(data: CreateComponent) -> CreateComponentEntity:
        return CreateComponentEntity(
            name=data.name,
            description=data.description,
            isqm_reference=data.isqm_reference,
            display_order=data.display_order,
        )

    @staticmethod
    def from_update(data: UpdateComponent) -> UpdateEntity:
        return UpdateEntity(
            name=data.name,
            status=data.status,
            isqm_reference=data.isqm_reference,
            description=data.description,
        )
