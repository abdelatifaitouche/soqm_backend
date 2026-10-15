"""
from src.features.documents.infrastructure.models.document_version import (
    DocumentVersion,
)
from src.features.documents.infrastructure.models.document import Document

from src.features.risks.models.risk_response_association import RiskResponseAssociation
from src.features.risks.models.component_response_seq import ComponentResponseSeq


from src.features.risks.models.risk_objective_association import (
    RiskObjectiveAssociation,
)

from src.features.risks.models.component_risk_seq import ComponentRiskSequence

from src.features.quality_objectives.models.component_objective_seq import (
    ComponentObjectiveSeq,
)
from src.features.risks.models.risk_response import RiskResponse

from src.features.risks.models.risk import Risk




from src.features.quality_objectives.models.quality_objective import QualityObjective
"""

from src.features.findings.infra.models import *
from src.features.soqm_engine.infra.models import *
from src.features.organizations.infra.models import *
from src.infra.db.base import Base
from src.features.auth.models.user import User
from src.features.auth.models.role import Role
from src.features.auth.models.role_permissions import RolePermissions
from src.features.auth.models.user_roles import UserRoles
from src.features.risks.models.risk_audit_log import RiskAuditLog

print("Risk registered:", "Risk" in Base.registry._class_registry)
print("Registered models:", list(Base.registry._class_registry.keys()))
