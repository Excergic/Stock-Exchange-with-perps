from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base
from backend.models.enums import ContractType


class Instrument(Base):
    """
    Perp instrument: symbol, tick size, leverage limits, margin rules, funding.
    Used for: what can be traded, funding rate, and margin params.
    """

    __tablename__ = "instruments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(50), unique=True)
    contract_type: Mapped[ContractType] = mapped_column(Enum(ContractType, name="contract_type_enum"))
    tick_size: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    max_leverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    maintenance_margin_rate: Mapped[Decimal] = mapped_column(Numeric(10, 8))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Funding (perps): rate applied every funding_interval_seconds
    funding_rate: Mapped[Decimal] = mapped_column(Numeric(12, 8), default=Decimal("0"))
    funding_interval_seconds: Mapped[int] = mapped_column(Integer, default=28800)  # 8h
    next_funding_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
