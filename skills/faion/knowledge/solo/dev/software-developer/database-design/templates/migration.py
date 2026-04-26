"""Alembic migration example: expand-contract pattern for adding NOT NULL column.

Step 1 (this migration): add as nullable
Step 2 (separate migration): backfill in batches
Step 3 (separate migration): add NOT NULL constraint

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # Step 1 of expand-contract: add NULLABLE — no table rewrite, no lock
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('language', sa.String(5), default='en'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_prefs_user', 'user_preferences', ['user_id'])

    # To add NOT NULL to existing big table — use expand-contract:
    # op.add_column('orders', sa.Column('currency', sa.String(3), nullable=True))
    # Then in a separate migration after backfill:
    # op.alter_column('orders', 'currency', nullable=False)


def downgrade():
    op.drop_index('idx_user_prefs_user', table_name='user_preferences')
    op.drop_table('user_preferences')
