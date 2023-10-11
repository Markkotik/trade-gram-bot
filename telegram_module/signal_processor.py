from telethon.tl.custom import Message
from typing import Optional

from database.models import TradeSignal, ActionType


class SignalProcessor:
    class Signal:
        def __init__(self, message: str):
            self.message = message

        def __str__(self) -> str:
            return f"Message: {self.message}"

    def create_signal(self, message: Message) -> Optional["SignalProcessor.Signal"]:
        trade_signal = self.parse_message(message.message)
        if trade_signal:
            return self.Signal(str(trade_signal))
        else:
            return None

    @staticmethod
    def is_signal(message: Message) -> bool:
        if message.media:
            return message.message is not None and message.message.startswith("🚀 Binance Alert:")

    @staticmethod
    def parse_message(message: str) -> Optional[TradeSignal]:
        # Поиск сигналов торговли в сообщении
        if "🚀 Binance Alert:" in message:
            try:
                lines = message.split('\n')
                symbol = lines[0].split('#')[-1].strip()  # Удаляем пробелы по краям
                action_line = lines[1].lower()  # Преобразуем строку в нижний регистр для упрощения поиска

                if "buy" in action_line:
                    action = ActionType.BUY
                elif "sell" in action_line:
                    action = ActionType.SELL
                else:
                    raise ValueError("Unknown action type")

                price = float(action_line.split(' ')[-1])
                stop_price = float(lines[2].split(': ')[-1])
                targets = [float(line.split(': ')[-1]) for line in lines[3:6]]

                return TradeSignal(
                    symbol=symbol,
                    action=action,
                    price=price,
                    stop_price=stop_price,
                    targets=targets
                )
            except Exception as e:
                print(f"Error parsing message: {e}")
                return None
        else:
            return None
