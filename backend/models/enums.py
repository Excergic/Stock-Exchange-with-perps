"""PostgreSQL-backed enums for exchange schema. Prevents invalid data."""

import enum


class OrderSide(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, enum.Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


class OrderStatus(str, enum.Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class MarginMode(str, enum.Enum):
    CROSS = "CROSS"
    ISOLATED = "ISOLATED"


class PositionSide(str, enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class TakerSide(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class ContractType(str, enum.Enum):
    PERPETUAL = "PERPETUAL"
    FUTURES = "FUTURES"


class WalletTransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"   # add fund (demo)
    WITHDRAW = "WITHDRAW"  # send money (demo)
