"""Add created_at to expenses

Revision ID: b3f1a2c5d7e9
Revises: 94aad27cc4eb
Create Date: 2026-06-11 16:50:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b3f1a2c5d7e9'
down_revision: Union[str, Sequence[str], None] = '94aad27cc4eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'expenses',
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('expenses', 'created_at')
