"""Drop category and created_at from expenses

Revision ID: d1e2f3a4b5c6
Revises: ada74739fae7
Create Date: 2026-06-11 21:58:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, Sequence[str], None] = 'ada74739fae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop category and created_at columns added by removed features."""
    op.drop_column('expenses', 'category')
    op.drop_column('expenses', 'created_at')

    # Drop the PostgreSQL Enum type that was created for category
    expense_category = sa.Enum(name='expensecategory')
    expense_category.drop(op.get_bind())


def downgrade() -> None:
    """Re-add category and created_at columns."""
    expense_category = sa.Enum(
        'FOOD', 'TRAVEL', 'SHOPPING', 'BILLS',
        'ENTERTAINMENT', 'OTHER',
        name='expensecategory',
    )
    expense_category.create(op.get_bind())

    op.add_column(
        'expenses',
        sa.Column('category', expense_category, nullable=False),
    )
    op.add_column(
        'expenses',
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
