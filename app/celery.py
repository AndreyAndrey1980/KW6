# Импорт необходимых модулей
import os  # Для взаимодействия с переменными окружения
from asgiref.sync import sync_to_async  # Для вызова синхронных Django ORM функций в асинхронном коде
from celery import Celery, shared_task  # Celery — система распределённого выполнения задач

# Установка переменной окружения для конфигурации Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_task.settings')

# Создание экземпляра приложения Celery
app = Celery('final_task')

# Загрузка настроек Celery из Django-конфигурации
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматический импорт задач из всех приложений Django
app.autodiscover_tasks()


# Асинхронная задача Celery для отправки напоминания о привычке
@shared_task
async def send_habit_reminder(habit_id, chat_id):
    try:
        # Получение объекта Habit по ID через асинхронную обёртку sync_to_async
        habit = await sync_to_async(Habit.objects.get)(id=habit_id)

        # Формирование текстового сообщения
        message = f"Reminder: {habit.action} at {habit.time} in {habit.place}"

    except Habit.DoesNotExist:
        # Если привычка с указанным ID не найдена, возвращается сообщение об ошибке
        return f"Habit with ID {habit_id} does not exist."

    # Отправка сообщения в Telegram (предполагается, что send_telegram_message — это асинхронная функция)
    await send_telegram_message(message, chat_id=chat_id)

    from celery import current_app
    countdown = habit.periodicity * 86400
    current_app.send_task(
        'app.celery.send_habit_reminder',
        args=[habit_id, chat_id],
        countdown=countdown
    )

