import os
import telegram
from dotenv import load_dotenv
from utils.logging_config import configure_logging, logging

load_dotenv()
configure_logging()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')


async def send_message(msg: str):
    """Send message to Telegram bot (if configured). Otherwise write to log."""
    if BOT_TOKEN and CHAT_ID:
        bot = telegram.Bot(BOT_TOKEN)
        async with bot:
            await bot.send_message(text=msg, chat_id=CHAT_ID)
    else:
        logging.error('Telegram bot is not configured properly! Check your `.env`...')
        logging.debug('Bot was trying to send message: {}'.format(msg))
