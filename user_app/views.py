from rest_framework import generics  # Классы представлений DRF
from .serializers import UserSerializer  # Сериализаторы
from .models import CustomUser

# Представление для регистрации нового пользователя
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer  # Используется кастомный сериализатор, создающий пользователя с хешированием пароля
