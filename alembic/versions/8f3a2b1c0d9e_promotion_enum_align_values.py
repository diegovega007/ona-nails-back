"""Alinear promotiontype con valores del Enum (discount, …), igual que Field(status).

Si el tipo quedó con etiquetas en mayúsculas (DISCOUNT, …), las renombra a los
valores de PromotionType para coincidir con SQLModel sin PG_ENUM explícito.

Revision ID: 8f3a2b1c0d9e
Revises: d2c4a26638c9
Create Date: 2026-05-04

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8f3a2b1c0d9e"
down_revision: Union[str, Sequence[str], None] = "d2c4a26638c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _enum_has_label(typname: str, label: str) -> bool:
    conn = op.get_bind()
    return bool(
        conn.execute(
            sa.text(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = :typname AND e.enumlabel = :label
                )
                """
            ),
            {"typname": typname, "label": label},
        ).scalar()
    )


def upgrade() -> None:
    if _enum_has_label("promotiontype", "DISCOUNT"):
        op.execute(
            sa.text("ALTER TYPE promotiontype RENAME VALUE 'DISCOUNT' TO 'discount'")
        )
        op.execute(
            sa.text(
                "ALTER TYPE promotiontype RENAME VALUE 'SERVICE_FREE' TO 'service_free'"
            )
        )
        op.execute(
            sa.text(
                "ALTER TYPE promotiontype RENAME VALUE 'NO_PROMOTION' TO 'no_promotion'"
            )
        )


def downgrade() -> None:
    if _enum_has_label("promotiontype", "discount"):
        op.execute(
            sa.text("ALTER TYPE promotiontype RENAME VALUE 'discount' TO 'DISCOUNT'")
        )
        op.execute(
            sa.text(
                "ALTER TYPE promotiontype RENAME VALUE 'service_free' TO 'SERVICE_FREE'"
            )
        )
        op.execute(
            sa.text(
                "ALTER TYPE promotiontype RENAME VALUE 'no_promotion' TO 'NO_PROMOTION'"
            )
        )
