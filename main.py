from telegram_module.telegram_listener import TelegramListener


async def handle_new_signal(signal):
    print(f"Обработка сигнала: {signal}")


async def main():
    listener = TelegramListener(signal_callback=handle_new_signal)
    await listener.start()


# Запуск главной асинхронной функции
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
