import requests
import logging
from HabitTracker.settings import TELEGRAM_URL, TELEGRAM_BOT_TOKEN


def send_telegram_message(chat_id, message):
    logger = logging.getLogger(__name__)
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.get(url=f'{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage', params=params)

    if response.status_code != 200:
        logger.error(f"Ошибка отправки сообщения: {response.status_code} - {response.text}")
    else:
        logger.info("Сообщение отправлено успешно!")