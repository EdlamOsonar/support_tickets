"""create items table

Revision ID: 0001_create_items
Revises: 
Create Date: 2025-11-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_items'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, index=False),
        sa.Column('description', sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('items')
