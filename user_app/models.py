from django.contrib.auth.models import AbstractUser  # Для получения пользовательской модели

# Получаем модель пользователя (переопределённую, если указана в settings.AUTH_USER_MODEL)
class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)