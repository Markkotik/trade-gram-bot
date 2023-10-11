from telethon import TelegramClient, events
from decouple import config
from telegram_module.signal_processor import SignalProcessor


class TelegramListener:
    def __init__(self, signal_callback):
        # Загрузка учетных данных из файла .env
        self.api_id = config('TELEGRAM_API_ID')
        self.api_hash = config('TELEGRAM_API_HASH')
        self.entity_username = config('TELEGRAM_USER_ID')

        # Создание клиента
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)

        # Создаем экземпляр обработчика сигналов
        self.signal_processor = SignalProcessor()

        # Сохраняем функцию обратного вызова
        self.signal_callback = signal_callback

        # Регистрация обработчика событий
        @self.client.on(events.NewMessage(chats=self.entity_username))
        async def new_message_handler(event):
            message = event.message

            if self.signal_processor.is_signal(message):
                signal = self.signal_processor.create_signal(message)
                print(f"Received a new signal: {signal}")
                # Теперь мы используем функцию обратного вызова, вместо возврата значения
                await self.signal_callback(signal)
            else:
                print("Received message does not meet signal criteria")

    async def start(self):
        print(f"Listening to entity: {self.entity_username}...")
        await self.client.start()
        await self.client.run_until_disconnected()
