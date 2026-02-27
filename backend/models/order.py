from decimal import Decimal
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base
from backend.models.enums import MarginMode, OrderSide, OrderStatus, OrderType


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    instrument_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instruments.id"))

    side: Mapped[OrderSide] = mapped_column(Enum(OrderSide, name="order_side_enum"))
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType, name="order_type_enum"))
    price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    filled_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status_enum"), default=OrderStatus.OPEN
    )
    leverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    margin_mode: Mapped[MarginMode] = mapped_column(Enum(MarginMode, name="margin_mode_enum"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        Index("idx_orders_user_id", "user_id"),
        Index("idx_orders_instrument_status", "instrument_id", "status"),
    )
