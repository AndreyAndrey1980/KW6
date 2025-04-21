from django.db import models  # Модуль моделей Django
from django.contrib.auth.models import AbstractUser  # Для получения пользовательской модели

# Получаем модель пользователя (переопределённую, если указана в settings.AUTH_USER_MODEL)
class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    