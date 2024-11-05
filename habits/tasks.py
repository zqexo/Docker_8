from datetime import datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message

import logging


@shared_task
def send_notifications_to_telegram():
    now = datetime.now()
    logger = logging.getLogger(__name__)
    habits = Habit.objects.filter(time__hour=now.hour)
    for habit in habits:
        message = f"Напоминание: {habit.action} в {habit.place}!"
        send_telegram_message(habit.user.tg_chat_id, message)
        logger.info(f"Сообщение для {habit.user.tg_chat_id} отправлено: {message}")
