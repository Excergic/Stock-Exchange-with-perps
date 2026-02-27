"""perps funding margin wallet_tx

Revision ID: c4f5a6b7d8e9
Revises: 1b3e415de881
Create Date: 2026-02-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4f5a6b7d8e9"
down_revision: Union[str, Sequence[str], None] = "1b3e415de881"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE wallet_transaction_type_enum AS ENUM ('DEPOSIT', 'WITHDRAW')")

    op.add_column(
        "instruments",
        sa.Column("funding_rate", sa.Numeric(precision=12, scale=8), server_default=sa.text("0"), nullable=False),
    )
    op.add_column(
        "instruments",
        sa.Column("funding_interval_seconds", sa.Integer(), server_default=sa.text("28800"), nullable=False),
    )
    op.add_column("instruments", sa.Column("next_funding_at", sa.DateTime(), nullable=True))

    op.add_column(
        "positions",
        sa.Column("margin_mode", sa.String(20), server_default=sa.text("'CROSS'"), nullable=False),
    )
    op.add_column(
        "positions",
        sa.Column("margin_used", sa.Numeric(20, 8), server_default=sa.text("0"), nullable=False),
    )
    op.add_column(
        "positions",
        sa.Column("cumulative_funding", sa.Numeric(20, 8), server_default=sa.text("0"), nullable=False),
    )
    op.add_column("positions", sa.Column("last_funding_at", sa.DateTime(), nullable=True))

    op.add_column(
        "wallets",
        sa.Column("margin_locked", sa.Numeric(20, 8), server_default=sa.text("0"), nullable=False),
    )

    op.create_table(
        "wallet_transactions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("wallet_id", sa.UUID(), nullable=False),
        sa.Column("type", sa.Enum("DEPOSIT", "WITHDRAW", name="wallet_transaction_type_enum"), nullable=False),
        sa.Column("amount", sa.Numeric(20, 8), nullable=False),
        sa.Column("balance_after", sa.Numeric(20, 8), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["wallet_id"], ["wallets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("wallet_transactions")
    op.drop_column("wallets", "margin_locked")
    op.drop_column("positions", "last_funding_at")
    op.drop_column("positions", "cumulative_funding")
    op.drop_column("positions", "margin_used")
    op.drop_column("positions", "margin_mode")
    op.drop_column("instruments", "next_funding_at")
    op.drop_column("instruments", "funding_interval_seconds")
    op.drop_column("instruments", "funding_rate")
    op.execute("DROP TYPE IF EXISTS wallet_transaction_type_enum CASCADE")
