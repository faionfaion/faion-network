# purpose: Legacy template for the database-design methodology.
# consumes: inputs declared in database-design/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
"""Add user_preferences table

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
Create Date: 2025-01-01 00:00:00.000000

Usage: alembic upgrade head / alembic downgrade -1
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "a1b2c3d4e5f6"
down_revision = "9z8y7x6w5v4u"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("theme", sa.String(20), nullable=False, server_default="light"),
        sa.Column("notifications_enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("language", sa.String(5), nullable=False, server_default="en"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_user_preferences_user_id"),
    )
    # CREATE INDEX CONCURRENTLY must run outside a transaction.
    # Use a separate migration step or execute_if needed.
    op.create_index("idx_user_prefs_user", "user_preferences", ["user_id"])


def downgrade() -> None:
    op.drop_index("idx_user_prefs_user", table_name="user_preferences")
    op.drop_table("user_preferences")
