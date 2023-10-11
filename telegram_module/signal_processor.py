import logging
from typing import Optional

from telethon.tl.custom import Message

from database.models import TradeSignal, ActionType

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s')


class Signal:
    """
    Represents a parsed signal from a message.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"Message: {self.message}"


class SignalProcessor:
    """
    Processes Telegram messages to parse trading signals.
    """

    @staticmethod
    def create_signal(message: Message) -> Optional[Signal]:
        """
        Creates a Signal object if message contains a valid trade signal.
        """
        trade_signal = SignalProcessor.parse_message(message.message)
        if trade_signal:
            return Signal(str(trade_signal))
        else:
            return None

    @staticmethod
    def is_signal(message: Message) -> bool:
        """
        Checks if the message contains a trading signal.
        """
        return bool(message.media and message.message and message.message.startswith("🚀 Binance Alert:"))

    @staticmethod
    def parse_message(message: str) -> Optional[TradeSignal]:
        """
        Parses the message to extract trading signal information.
        """
        if "🚀 Binance Alert:" not in message:
            return None

        try:
            lines = message.split('\n')
            symbol = lines[0].split('#')[-1].strip()
            action = ActionType.BUY if "buy" in lines[1].lower() else ActionType.SELL
            price = float(lines[1].split(' ')[-1])
            stop_price = float(lines[2].split(': ')[-1])
            targets = [float(line.split(': ')[-1]) for line in lines[3:6]]

            return TradeSignal(
                symbol=symbol,
                action=action,
                price=price,
                stop_price=stop_price,
                targets=targets
            )
        except (ValueError, IndexError) as e:
            logging.error(f"Error parsing message: {e}")
            return None
