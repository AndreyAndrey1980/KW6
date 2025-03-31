from django.conf import settings
from telegram import Bot


TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID
bot = Bot(token=TELEGRAM_TOKEN)


async def send_telegram_message(message, chat_id=TELEGRAM_USER_ID):
    await bot.send_message(chat_id=chat_id, text=message)