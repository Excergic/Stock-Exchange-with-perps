from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    asset: Mapped[str] = mapped_column(String(20))  # e.g. USDT (demo settlement)
    balance: Mapped[Decimal] = mapped_column(Numeric(20, 8))  # total (add fund / send money)
    margin_locked: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))  # in open positions
    available_balance: Mapped[Decimal] = mapped_column(Numeric(20, 8))  # balance - margin_locked (for orders)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("Users", back_populates="wallets")

