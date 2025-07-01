from django.urls import include, path  # Подключение систем маршрутизации Django
from rest_framework.routers import DefaultRouter  # Автоматическая маршрутизация для ViewSet-ов
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT views

# Импорт представлений
from .views import UserHabitViewSet, PublicHabitViewSet

# Создаём роутер и регистрируем в нём viewsets
router = DefaultRouter()

# ViewSet для работы с привычками, принадлежащими текущему пользователю (требует авторизации)
router.register(r'habits', UserHabitViewSet, basename='habit')

# ViewSet для публичных привычек (можно просматривать без авторизации)
router.register(r'publichabits', PublicHabitViewSet, basename='public-habit')

# Основной список URL-паттернов
urlpatterns = [
    # Включение маршрутов из роутера (автоматически сгенерированные маршруты для ViewSet-ов)
    path('', include(router.urls)),
]
