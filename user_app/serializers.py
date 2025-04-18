from rest_framework import serializers
from .models import CustomUser

# Сериализатор для регистрации пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'telegram_chat_id')
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль не отображается в ответе
            'email': {'required': True}
        }

    def create(self, validated_data):
        # Используем create_user, чтобы пароль автоматически хешировался
        user = CustomUser.objects.create_user(**validated_data)
        return user