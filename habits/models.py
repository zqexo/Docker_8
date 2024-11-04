from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь"
    )
    place = models.CharField("Место", max_length=255)
    time = models.TimeField("Время выполнения")
    action = models.CharField("Действие", max_length=255)
    is_pleasant = models.BooleanField("Приятная привычка", default=False)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True},
        related_name="main_habits",
        verbose_name="Связанная привычка"
    )
    frequency = models.CharField(
        "Периодичность",
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily'
    )
    reward = models.CharField("Вознаграждение", max_length=255, blank=True, null=True)
    completion_time = models.PositiveIntegerField("Время на выполнение (в секундах)")
    is_public = models.BooleanField("Публичная привычка", default=False)

    def clean(self):
        # Проверка на одновременное указание связанной привычки и вознаграждения
        if self.reward and self.related_habit:
            raise ValidationError(
                _("Укажите либо вознаграждение, либо связанную привычку, но не оба сразу.")
            )

        # Время на выполнение не должно превышать 120 секунд
        if self.completion_time > 120:
            raise ValidationError(
                _("Время выполнения должно быть не больше 120 секунд.")
            )

        # Приятная привычка не может иметь связанной привычки или вознаграждения
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                _("Приятная привычка не может иметь вознаграждения или связанной привычки.")
            )

        # Периодичность выполнения должна быть не реже 1 раза в неделю
        if self.frequency == 'weekly' and self.completion_time > 7 * 86400:
            raise ValidationError(
                _("Периодичность выполнения привычки должна быть не реже 1 раза в неделю.")
            )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.action} ({self.get_frequency_display()}) в {self.place} в {self.time}"
