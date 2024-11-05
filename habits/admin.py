from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place', 'time', 'is_public')
    list_filter = ('is_public', 'user', 'time')
    search_fields = ('action', 'place', 'user__username')

    fieldsets = (
        (None, {
            'fields': ('user', 'action', 'place', 'time', 'is_public')
        }),
        ('Details', {
            'fields': ('is_pleasant', 'related_habit', 'reward', 'completion_time', 'frequency')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Переопределение сохранения для валидации привычки:
        - Исключает одновременное заполнение полей `related_habit` и `reward`.
        - Проверяет, что время выполнения не превышает 120 секунд.
        - Проверяет, что связанная привычка является приятной привычкой.
        """
        if obj.related_habit and obj.reward:
            raise ValueError("Нельзя одновременно указать вознаграждение и связанную привычку.")

        if obj.completion_time > 120:
            raise ValueError("Время выполнения привычки не должно превышать 120 секунд.")

        if obj.related_habit and not obj.related_habit.is_pleasant:
            raise ValueError("Связанная привычка должна быть отмечена как приятная.")

        super().save_model(request, obj, form, change)
