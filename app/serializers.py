from rest_framework import serializers
from .models import Habit


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
