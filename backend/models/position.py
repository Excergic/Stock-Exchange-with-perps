from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base
from backend.models.enums import PositionSide


class Position(Base):
    """Per-user, per-instrument, per-side position for perpetuals."""

    __tablename__ = "positions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    instrument_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instruments.id"))

    side: Mapped[PositionSide] = mapped_column(Enum(PositionSide, name="position_side_enum"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    entry_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    leverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    margin_mode: Mapped[str] = mapped_column(String(20))  # CROSS | ISOLATED
    margin_used: Mapped[Decimal] = mapped_column(Numeric(20, 8))  # initial margin locked
    unrealized_pnl: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    liquidation_price: Mapped[Decimal] = mapped_column(Numeric(20, 8))

    # Funding: total paid/received so far; last time we applied funding
    cumulative_funding: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    last_funding_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint("user_id", "instrument_id", "side", name="uq_position_user_instrument_side"),
    )
