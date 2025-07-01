# Импорт для моков и тестирования API
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.conf import settings

# Импортируем модели и утилиты приложения
from app.models import Habit
from app.celery import send_habit_reminder
from app.utils import send_telegram_message


# Тесты регистрации и входа
class AuthTests(APITestCase):

    # Проверка регистрации пользователя
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "testuser@example.com"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Проверка регистрации и входа (получение JWT-токенов)
    def test_user_login(self):
        # Сначала регистрируем
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "testuser@example.com"
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Затем логинимся
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.__dict__))
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


# Тесты для привычек авторизованного пользователя
class UserHabitTests(APITestCase):

    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    # Авторизация через JWT
    def authenticate(self):
        response = self.client.post('/api/token/', {"username": "testuser", "password": "testpass123"})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Тест создания привычки
    def test_create_habit(self):
        self.authenticate()
        data = {
            "user": self.user.id,
            "action": "Drink water",
            "time": "08:00",
            "place": "Kitchen",
            "is_public": False,
            "duration": 30,
        }
        response = self.client.post('/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, str(response.__dict__))

    # Тест получения списка привычек пользователя
    def test_list_user_habits(self):
        self.authenticate()
        Habit.objects.create(user=self.user, action="Read a book", time="18:00", place="Living Room", duration=30)
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # Тест обновления привычки
    def test_update_habit(self):
        self.authenticate()
        habit = Habit.objects.create(user=self.user, action="Jogging", time="06:00", place="Park", duration=30)
        data = {
            "user": self.user.id,
            "action": "Morning Jog",
            "time": "07:00",
            "place": "Park",
            "duration": 30,
        }
        response = self.client.put(f'/habits/{habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, str(response.__dict__))
        self.assertEqual(response.data['action'], 'Morning Jog')

    # Тест удаления привычки
    def test_delete_habit(self):
        self.authenticate()
        habit = Habit.objects.create(user=self.user, action="Meditate", time="07:30", place="Bedroom", duration=30)
        response = self.client.delete(f'/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Тесты публичных привычек (без авторизации)
class PublicHabitTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        # Одна публичная привычка и одна приватная
        Habit.objects.create(user=self.user, action="Yoga", time="06:00", place="Living Room", duration=30, is_public=True)
        Habit.objects.create(user=self.user, action="Read News", time="08:00", place="Balcony", duration=30, is_public=False)

    # Проверка, что отображается только публичная привычка
    def test_list_public_habits(self):
        response = self.client.get('/publichabits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], 'Yoga')

    # Убеждаемся, что нельзя создавать, обновлять или удалять через публичный эндпоинт
    def test_no_create_update_delete_in_public_endpoint(self):
        data = {
            "action": "Exercise",
            "time": "09:00",
            "place": "Gym",
            "is_public": True,
            "duration": 30,
        }
        response = self.client.post('/publichabits/', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        habit = Habit.objects.first()
        response = self.client.put(f'/publichabits/{habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(f'/publichabits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Тесты отправки Telegram-уведомлений
class TelegramNotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.habit = Habit.objects.create(
            user=self.user,
            action="Drink water",
            time="08:00",
            place="Kitchen",
            duration=30,
            is_public=True
        )

    # Проверка успешной отправки сообщения через Telegram
    @patch('telegram.Bot.send_message')
    async def test_send_telegram_message_success(self, mock_send_message):
        mock_send_message.return_value = MagicMock()
        chat_id = settings.TELEGRAM_USER_ID
        message = f"Reminder: {self.habit.action} at {self.habit.time} in {self.habit.place}"

        response = await send_telegram_message(message, chat_id=chat_id)
        mock_send_message.assert_called_once_with(chat_id=chat_id, text=message)
        self.assertIsNone(response)

    # Проверка обработки ошибки при неверном chat_id
    @patch('telegram.Bot.send_message')
    def test_send_telegram_message_invalid_chat_id(self, mock_send_message):
        mock_send_message.side_effect = Exception("Chat not found")

        chat_id = "999"
        message = "Invalid chat test"

        with self.assertRaises(Exception) as context:
            send_telegram_message(message, chat_id=chat_id)
        self.assertEqual(str(context.exception), "Chat not found")

    # Проверка обработки ошибки Telegram API
    @patch('telegram.Bot.send_message')
    async def test_send_telegram_message_api_failure(self, mock_send_message):
        mock_send_message.side_effect = Exception("Telegram API Error")

        chat_id = 123456789
        message = "API failure test"

        with self.assertRaises(Exception) as context:
            await send_telegram_message(message, chat_id=chat_id)
        self.assertEqual(str(context.exception), "Telegram API Error")

    # Проверка корректной работы Celery-задачи send_habit_reminder
    @patch('telegram.Bot.send_message')
    async def test_send_habit_reminder_task(self, mock_send_message):
        mock_send_message.return_value = MagicMock()

        chat_id = 123456789

        # Вызываем задачу
        send_habit_reminder(self.habit.id, chat_id=chat_id)

        message = f"Reminder: {self.habit.action} at {self.habit.time} in {self.habit.place}"
        mock_send_message.assert_called_once_with(chat_id=123456789, text=message)
