from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ActionType(Enum):
    """Enum representing possible trading actions."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """Enum representing possible order types."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


@dataclass
class TradeSignal:
    """
    A class representing a trading signal.

    Attributes:
        - symbol: The trading pair, e.g., "BTCUSDT".
        - action: The trading action to take, either BUY or SELL.
        - order_type: The type of the order, either MARKET or LIMIT.
        - price: The execution price for the LIMIT order type.
        - targets: A list of target prices for closing the position.
        - stop_price: The stop-loss price.
        - quantity: The amount to buy/sell.
        - quote_order_qty: The amount of quote currency to spend.
        - timestamp: The time the signal was received.
    """

    symbol: str
    action: ActionType
    order_type: OrderType = OrderType.MARKET
    price: Optional[float] = None
    targets: List[float] = None
    stop_price: Optional[float] = None
    quantity: Optional[float] = None
    quote_order_qty: Optional[float] = None
    timestamp: Optional[float] = None
