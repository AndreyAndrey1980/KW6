from django.db import models  # Модуль моделей Django
from django.core.exceptions import ValidationError  # Для генерации ошибок валидации
from user_app.models import CustomUser


# Модель Habit описывает привычку пользователя
class Habit(models.Model):
    # Привязка привычки к пользователю
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits')

    # Место выполнения привычки
    place = models.CharField(max_length=255)

    # Время выполнения привычки
    time = models.TimeField()

    # Действие, описывающее привычку
    action = models.CharField(max_length=255)

    # Является ли привычка приятной (без дополнительной мотивации)
    is_pleasant = models.BooleanField(default=False)

    # Связанная привычка (например, привычка-награда за выполнение другой привычки)
    linked_habit = models.ForeignKey(
        'self',  # Связь на саму себя
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Периодичность выполнения привычки в днях (от 1 до 7)
    periodicity = models.PositiveIntegerField()

    # Награда за выполнение привычки (если не связана с другой привычкой)
    reward = models.CharField(max_length=255, null=True, blank=True)

    # Продолжительность привычки в секундах
    duration = models.PositiveIntegerField()

    # Публичная ли привычка (можно ли делиться ею с другими)
    is_public = models.BooleanField(default=False)


    # Кастомная валидация модели
    def clean(self):
        # Ограничение по максимальной продолжительности
        if self.duration > 120:
            raise ValidationError('Duration cannot exceed 120 seconds.')

        # Нельзя одновременно указать связанную привычку и награду
        if self.linked_habit and self.reward:
            raise ValidationError('Cannot set both linked habit and reward.')

        # Связанная привычка должна быть "приятной"
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError('Linked habit must be a pleasant habit.')

        # Приятные привычки не могут иметь награды или быть связаны с другими
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Pleasant habits cannot have rewards or linked habits.')

        # Периодичность должна быть в пределах от 1 до 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError('Periodicity must be between 1 and 7 days.')

    # Представление привычки в виде строки
    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.time} in {self.place}"
