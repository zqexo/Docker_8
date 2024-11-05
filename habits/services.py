import requests

from HabitTracker.settings import TELEGRAM_URL, TELEGRAM_BOT_TOKEN


def send_telegram_message(chat_id, message):
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    requests.get(url=f'{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
