"""add_categories_and_transactions

Revision ID: 6f60c2e762b3
Revises: 8f0175943a8a
Create Date: 2026-08-26 09:35:01.322134

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6f60c2e762b3'
down_revision: str | Sequence[str] | None = '8f0175943a8a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("transaction")}

    if "category_id" not in existing_columns:
        op.add_column("transaction", sa.Column("category_id", sa.Integer(), nullable=True))

    if "type" not in existing_columns:
        op.add_column(
            "transaction",
            sa.Column("type", sa.Enum("CREDIT", "DEBIT", name="transactiontype"), nullable=False),
        )

    # SQLite does not support adding foreign key constraints with ALTER TABLE.
    if bind.dialect.name != "sqlite":
        op.create_foreign_key(None, "transaction", "category", ["category_id"], ["id"])

    if "transaction_type" in existing_columns:
        op.drop_column("transaction", "transaction_type")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("transaction")}

    if "transaction_type" not in existing_columns:
        op.add_column("transaction", sa.Column("transaction_type", sa.VARCHAR(length=50), nullable=False))

    if bind.dialect.name != "sqlite":
        op.drop_constraint(None, "transaction", type_="foreignkey")

    if "type" in existing_columns:
        op.drop_column("transaction", "type")

    if "category_id" in existing_columns:
        op.drop_column("transaction", "category_id")
