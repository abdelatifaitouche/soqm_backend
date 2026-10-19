from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class PotentialCauses:
    id: UUID
    potential_root_cause: str
    isqm_component: UUID


@dataclass
class RootCauseIndicator:
    id: UUID
    indicator: str
    potential_causes: list[PotentialCauses] = field(default_factory=list)


@dataclass
class RootCauseCategory:
    id: UUID
    category: str
    indicators: list[RootCauseIndicator] = field(default_factory=list)

    @classmethod
    def create(cls, category: str) -> "RootCauseCategory":
        return cls(
            id=uuid4(),
            category=category,
        )

    def add_indicator(
        self, indicator_name: str, potential_root_cause: str, isqm_id: UUID
    ):

        indicator = next(
            (i for i in self.indicators if i.indicator == indicator_name), None
        )

        if not indicator:
            indicator = RootCauseIndicator(id=uuid4(), indicator=indicator_name)

            self.indicators.append(indicator)

        exists = any(
            p.potential_root_cause == potential_root_cause
            and p.isqm_component == isqm_id
            for p in indicator.potential_causes
        )

        if not exists:
            indicator.potential_causes.append(
                PotentialCauses(
                    id=uuid4(),
                    potential_root_cause=potential_root_cause,
                    isqm_component=isqm_id,
                )
            )
