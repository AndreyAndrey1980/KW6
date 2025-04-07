from rest_framework import viewsets, status, generics, mixins  # Классы представлений DRF
from rest_framework.permissions import AllowAny, IsAuthenticated  # Права доступа

from .pagination import HabitPagination  # Кастомная пагинация
from .serializers import UserSerializer, HabitSerializer  # Сериализаторы
from .models import CustomUser,Habit  # Модель привычек
from .celery import send_habit_reminder


# Представление для регистрации нового пользователя
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer  # Используется кастомный сериализатор, создающий пользователя с хешированием пароля


# ViewSet для работы с привычками текущего пользователя
class UserHabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
    pagination_class = HabitPagination  # Подключена кастомная пагинация

    # Возвращаем только привычки текущего пользователя
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    # При создании новой привычки автоматически привязываем её к текущему пользователю
    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)

        # Получаем telegram_chat_id из профиля
        chat_id = self.request.user.telegram_chat_id
        if chat_id:
            send_habit_reminder.delay(habit.id, chat_id)


# ViewSet только для чтения публичных привычек
class PublicHabitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [AllowAny]  # Доступ открыт для всех (в том числе анонимных пользователей)

    # Возвращаем только те привычки, которые являются публичными
    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
