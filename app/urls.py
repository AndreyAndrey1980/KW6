from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserHabitViewSet, PublicHabitViewSet, RegisterView

router = DefaultRouter()
router.register(r'habits', UserHabitViewSet, basename='habit')
router.register(r'publichabits', PublicHabitViewSet, basename='public-habit')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls))
]