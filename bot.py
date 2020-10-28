from os import environ
import requests
from time import sleep
import telegram
import logging

logger = logging.getLogger()


class MyLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = telegram.Bot(bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)


def get_checklist(token, chat_id):
    while True:
        params = {}
        headers = {
            'Authorization': f'Token {token}'
        }
        url = f'https://dvmn.org/api/long_polling/'
        try:
            response = requests.get(url, headers=headers, params=params, timeout=90)
            response.raise_for_status()
            answer = response.json()
            if answer['status'] == 'timeout':
                params['timestamp'] = answer['timestamp_to_request']
            elif answer['status'] == 'found':
                params['timestamp'] = answer['last_attempt_timestamp']
                new_attempt = answer['new_attempts'][0]
                name_work = new_attempt['lesson_title']
                lesson_url = new_attempt['lesson_url']
                work_is_negative = new_attempt['is_negative']
                message = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                if work_is_negative:
                    message = "К сожалению в работе нашлись ошибки"
                bot.send_message(chat_id,
                                 f'Преподаватель проверил работу: "{name_work}" https://dvmn.org{lesson_url} {message}')
        except requests.exceptions.ReadTimeout as error:
            continue
        except ConnectionError as error:
            logger.info(error)
            sleep(30)


if __name__ == '__main__':
    telegram_bot_token = environ['TELEGRAM_BOT_TOKEN']
    telegram_chat_id = environ['TELEGRAM_CHAT_ID']
    dvmn_token = environ['DVMN_API_TOKEN']
    telegram_logging_bot_token = environ['TELEGRAM_LOGGING_BOT_TOKEN']

    logging.basicConfig(level='INFO', format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
    my_handler = MyLogsHandler(telegram_logging_bot_token, telegram_chat_id)
    logger.addHandler(my_handler)
    template_fmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    my_handler.setFormatter(template_fmt)
    bot = telegram.Bot(telegram_bot_token)
    logger.info('Бот запущен')
    while True:
        try:
            get_checklist(dvmn_token, telegram_chat_id)
        except Exception as error:
            logger.info(f'Бот упал с ошибкой: {error}')
