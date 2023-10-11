import asyncio
import logging
from telegram_module.telegram_listener import TelegramListener

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def handle_new_signal(signal):
    """
    Callback function to handle new signals.

    :param signal: The signal data to be processed.
    """
    logging.info(f"Processing signal: {signal}")


async def main():
    """
    Main function to initialize the TelegramListener and start listening.
    """
    try:
        listener = TelegramListener(signal_callback=handle_new_signal)
        await listener.start()
    except Exception as e:
        logging.exception("An error occurred while running the listener: %s", e)


if __name__ == "__main__":
    # Running the main function in the asyncio event loop
    asyncio.run(main())
