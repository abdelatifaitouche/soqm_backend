"""seed_closure_termination_reasons

Revision ID: 665641be1e94
Revises: 831b2fe24341
Create Date: 2026-10-22 02:34:45.154518

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from uuid import uuid4

# revision identifiers, used by Alembic.
revision: str = "665641be1e94"
down_revision: Union[str, Sequence[str], None] = "831b2fe24341"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    reason_categories_table = sa.table(
        "reason_categories",
        sa.column("id", sa.UUID),
        sa.column("code", sa.String),
        sa.column("context", sa.String),
        sa.column("display_text", sa.String),
        sa.column("is_active", sa.Boolean),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )

    raw_data = [
        {
            "code": "ERR_DUPLICATE",
            "context": "RISK_CLOSE",
            "display_text": "Duplicate Record",
        },
        {
            "code": "ERR_DATA_ENTRY",
            "context": "RISK_CLOSE",
            "display_text": "Entered in Error / Typo",
        },
        {
            "code": "PROC_OBSOLETE",
            "context": "RISK_CLOSE",
            "display_text": "Process / Asset Decommissioned",
        },
        {
            "code": "RISK_ACCEPTED",
            "context": "RISK_CLOSE",
            "display_text": "Risk Accepted by Management",
        },
        {
            "code": "FORCE_MAJEURE",
            "context": "RISK_CLOSE",
            "display_text": "External Factor Shift",
        },
    ]

    now = datetime.now()
    rows_to_insert = []

    for row in raw_data:
        rows_to_insert.append(
            {
                "id": uuid4(),
                "created_at": now,
                "updated_at": now,
                "context": row["context"],
                "code": row["code"],
                "display_text": row["display_text"],
                "is_active": True,
            }
        )

    target_codes = [r["code"] for r in rows_to_insert]
    op.execute(
        sa.text("DELETE FROM reason_categories WHERE code IN :codes").bindparams(
            sa.bindparam("codes", value=target_codes, expanding=True)
        ),
    )

    # 5. Bulk insert the fully enriched records natively via Alembic
    op.bulk_insert(reason_categories_table, rows_to_insert)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DELETE FROM reason_categories 
            WHERE code IN ('ERR_DUPLICATE', 'ERR_DATA_ENTRY', 'PROC_OBSOLETE', 'RISK_ACCEPTED', 'FORCE_MAJEURE');
            """
        )
    )
