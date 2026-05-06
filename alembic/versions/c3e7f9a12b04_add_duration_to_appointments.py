"""Agregar columna duration a appointments

Revision ID: c3e7f9a12b04
Revises: f61f03471ba9
Create Date: 2026-05-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3e7f9a12b04'
down_revision: Union[str, Sequence[str], None] = 'f61f03471ba9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'appointments',
        sa.Column('duration', sa.Integer(), nullable=False, server_default='0'),
    )
    op.alter_column('appointments', 'duration', server_default=None)


def downgrade() -> None:
    op.drop_column('appointments', 'duration')
