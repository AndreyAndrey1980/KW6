from django.conf import settings  # Для доступа к переменным конфигурации Django
from telegram import Bot  # Telegram Bot API из библиотеки python-telegram-bot


# Получаем токен бота и ID пользователя из настроек Django
TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

# Создаём экземпляр Telegram-бота
bot = Bot(token=TELEGRAM_TOKEN)


# Асинхронная функция для отправки сообщения в Telegram
async def send_telegram_message(message, chat_id):
    await bot.send_message(chat_id=chat_id, text=message)
