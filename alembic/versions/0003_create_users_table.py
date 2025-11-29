"""create users table for authentication

Revision ID: 0003_create_users_table
Revises: 0002_add_items_status_and_fields
Create Date: 2025-11-29
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_create_users_table'
down_revision = '0002_add_items_status_and_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=128), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('users')

