"""add items_status table and new fields to items

Revision ID: 0002_add_items_status_and_fields
Revises: 0001_create_items
Create Date: 2025-11-15
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_items_status_and_fields'
down_revision = '0001_create_items'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create items_status table
    op.create_table(
        'items_status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('status', sa.String(length=50), nullable=False, unique=True, index=True),
    )
    
    # Insert default statuses
    op.execute("INSERT INTO items_status (status) VALUES ('IN_PROGRESS')")
    op.execute("INSERT INTO items_status (status) VALUES ('RESOLVED')")
    
    # Add new columns to items table
    op.add_column('items', sa.Column('ticket_url', sa.String(length=255), nullable=True))
    op.add_column('items', sa.Column('publication_url', sa.String(length=255), nullable=True))
    op.add_column('items', sa.Column('reported_user', sa.String(length=128), nullable=True))
    op.add_column('items', sa.Column('creation_date', sa.DateTime, nullable=False, server_default=sa.func.now()))
    op.add_column('items', sa.Column('status_id', sa.Integer, nullable=False, server_default='1'))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_items_status_id',
        'items', 'items_status',
        ['status_id'], ['id']
    )


def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint('fk_items_status_id', 'items')
    
    # Remove columns from items table
    op.drop_column('items', 'status_id')
    op.drop_column('items', 'creation_date')
    op.drop_column('items', 'reported_user')
    op.drop_column('items', 'publication_url')
    op.drop_column('items', 'ticket_url')
    
    # Drop items_status table
    op.drop_table('items_status')
