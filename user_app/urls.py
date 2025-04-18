from django.urls import include, path  # Подключение систем маршрутизации Django
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT views

# Импорт представлений
from .views import RegisterView

# Основной список URL-паттернов
urlpatterns = [
    # JWT: получение пары access/refresh токенов
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT: обновление access токена по refresh токену
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Регистрация нового пользователя
    path('api/register/', RegisterView.as_view(), name='register'),
]
