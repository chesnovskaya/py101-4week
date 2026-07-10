import os
import sys
import logging

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_FROM_NUMBER",
]


def get_config():
    """Считывает и проверяет обязательные переменные окружения."""
    config = {var: os.getenv(var) for var in REQUIRED_ENV_VARS}
    missing = [k for k, v in config.items() if not v]
    if missing:
        raise EnvironmentError(f"Не заданы переменные окружения: {', '.join(missing)}")
    return config


def send_sms(to_number: str, body: str) -> str:
    """Отправляет SMS через Twilio и возвращает SID сообщения."""
    config = get_config()
    client = Client(config["TWILIO_ACCOUNT_SID"], config["TWILIO_AUTH_TOKEN"])

    try:
        message = client.messages.create(
            body=body,
            from_=config["TWILIO_FROM_NUMBER"],
            to=to_number,
        )
    except TwilioRestException as exc:
        logger.error("Ошибка при отправке SMS: %s", exc)
        raise

    logger.info("Сообщение отправлено, SID: %s", message.sid)
    return message.sid


def main():
    if len(sys.argv) < 2:
        print("Использование: python send_sms.py <номер_получателя> [текст сообщения]")
        sys.exit(1)

    to_number = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else "Привет!"

    send_sms(to_number, body)


if __name__ == "__main__":
    main()
