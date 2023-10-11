import logging
from telethon import TelegramClient, events
from decouple import config
from telegram_module.signal_processor import SignalProcessor
from typing import Callable, Awaitable, Any

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s')


class TelegramListener:
    """
    Listens to Telegram messages and processes signals.
    """

    def __init__(self, signal_callback: Callable[[Any], Awaitable[None]]) -> None:
        """
        Initializes the listener with the provided callback.
        """
        self._load_config()
        self.client: TelegramClient = TelegramClient('session_name', self.api_id, self.api_hash)
        self.signal_processor: SignalProcessor = SignalProcessor()
        self.signal_callback: Callable[[Any], Awaitable[None]] = signal_callback
        self._register_event_handlers()

    def _load_config(self) -> None:
        """
        Loads configuration from the environment.
        """
        self.api_id: int = config('TELEGRAM_API_ID')
        self.api_hash: str = config('TELEGRAM_API_HASH')
        self.entity_username: str = config('TELEGRAM_USER_ID')

    def _register_event_handlers(self) -> None:
        """
        Registers event handlers for the client.
        """

        @self.client.on(events.NewMessage(chats=self.entity_username))
        async def new_message_handler(event: events.NewMessage.Event) -> None:
            """
            Handles new message events.
            """
            message = event.message

            if self.signal_processor.is_signal(message):
                signal = self.signal_processor.create_signal(message)
                logging.info(f"Received a new signal: {signal}")
                await self.signal_callback(signal)
            else:
                logging.info("Received message does not meet signal criteria")

    async def start(self) -> None:
        """
        Starts the Telegram client.
        """
        logging.info(f"Listening to entity: {self.entity_username}...")
        await self.client.start()
        await self.client.run_until_disconnected()
