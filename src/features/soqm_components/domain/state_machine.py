from src.features.soqm_components.enums.soqm_component import ComponentState
from src.core.exceptions import InvalidStateTransition

ALLOWED_TRANSITIONS = {
    ComponentState.ACTIVE.value: {
        ComponentState.ARCHIVED.value,
        ComponentState.IN_ACTIVE.value,
    },
    ComponentState.IN_ACTIVE.value: {
        ComponentState.ARCHIVED.value,
        ComponentState.ACTIVE.value,
    },
    ComponentState.ARCHIVED.value: {},
}


def _can_transition(from_state: str, to_state: str) -> bool:
    return to_state in ALLOWED_TRANSITIONS[from_state]


def transition(from_state: str, to_state: str) -> str:

    if not _can_transition(from_state, to_state):
        raise InvalidStateTransition(
            message=f"Invalid transition from {from_state} --> {to_state}",
        )

    return to_state
