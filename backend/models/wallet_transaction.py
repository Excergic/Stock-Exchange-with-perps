"""Demo add fund / send money – one row per deposit or withdrawal."""

from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base
from backend.models.enums import WalletTransactionType


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"))
    type: Mapped[WalletTransactionType] = mapped_column(
        Enum(WalletTransactionType, name="wallet_transaction_type_enum")
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 8))  # positive = credit, negative = debit
    balance_after: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)  # snapshot after tx
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
