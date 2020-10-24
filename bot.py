from dotenv import load_dotenv
from os import getenv
import requests
from time import sleep
import telegram


def get_checklist(token, chat_id):
    while True:
        params = {}
        headers = {
            'Authorization': f'Token {token}'
        }
        url = f'https://dvmn.org/api/long_polling/'
        try:
            response = requests.get(url, headers=headers, params=params, timeout=91)
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
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError:
            sleep(30)


if __name__ == '__main__':
    load_dotenv()
    telegram_api_key = getenv('TELEGRAM_API_KEY')
    telegram_chat_id = getenv('TELEGRAM_CHAT_ID')
    devman_token = getenv('DEVMAN_API_TOKEN')
    bot = telegram.Bot(telegram_api_key)
    get_checklist(devman_token, telegram_chat_id)
