from rest_framework import serializers
from .models import CustomUser

# Сериализатор для регистрации пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('password', 'email', 'telegram_chat_id')
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль не отображается в ответе
            'email': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user