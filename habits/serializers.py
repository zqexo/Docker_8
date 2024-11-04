from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Укажите либо вознаграждение, либо связанную привычку, но не оба сразу.")
        if data.get('completion_time') and data['completion_time'] > 120:
            raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд.")
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждения или связанной привычки.")
        return data

