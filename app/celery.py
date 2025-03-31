import asyncio
import os
from asgiref.sync import sync_to_async
from celery import Celery, shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_task.settings')

app = Celery('final_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task
async def send_habit_reminder(habit_id, chat_id):
    try:
        habit = await sync_to_async(Habit.objects.get)(id=habit_id)
        message = f"Reminder: {habit.action} at {habit.time} in {habit.place}"
    except Habit.DoesNotExist:
        return f"Habit with ID {habit_id} does not exist."
    await send_telegram_message(message, chat_id=chat_id)
