from rest_framework import serializers
from .models import Habit, CustomUser


# Сериализатор для модели Habit
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'  # Включает все поля модели Habit

    # Валидация уровня сериализатора, в соответствии с тз
    def validate(self, data):
        if data.get('linked_habit') and data.get('reward'):
            raise serializers.ValidationError("Cannot set both linked habit and reward.")
        return data


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
