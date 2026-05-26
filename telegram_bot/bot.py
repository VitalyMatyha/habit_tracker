import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str) -> None:
    """Отправка сообщения пользователю в Telegram."""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    response = requests.post(url, data=data)
    return response.json()