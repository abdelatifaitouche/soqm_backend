from src.features.auth.permissions.auth_permissions import AuthPermissions
from src.features.risks.permissions.risk_permissions import RiskPermissions
from src.features.soqm_components.permissions.components_permissions import (
    ComponentPermissions,
)


class Permissions:
    Auth = AuthPermissions
    Component = ComponentPermissions
    Risk = RiskPermissions
