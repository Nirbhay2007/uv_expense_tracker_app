"""add expense category

Revision ID: 73159613d6fe
Revises: d1e2f3a4b5c6
Create Date: 2026-06-11 22:32:31.356040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73159613d6fe'
down_revision: Union[str, Sequence[str], None] = 'd1e2f3a4b5c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add expense category enum and column."""
    # Create the PostgreSQL Enum type
    expense_category = sa.Enum(
        'FOOD', 'TRAVEL', 'SHOPPING', 'BILLS',
        'ENTERTAINMENT', 'OTHER',
        name='expensecategory',
    )
    expense_category.create(op.get_bind())

    # Add the category column to expenses table
    op.add_column(
        'expenses',
        sa.Column(
            'category',
            expense_category,
            nullable=False,
            server_default='OTHER',
        ),
    )


def downgrade() -> None:
    """Remove expense category column and enum."""
    # Drop the category column
    op.drop_column('expenses', 'category')

    # Drop the PostgreSQL Enum type
    expense_category = sa.Enum(name='expensecategory')
    expense_category.drop(op.get_bind())
