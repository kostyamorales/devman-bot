# devman-bot

## Получаем уведомления о проверке работ на курсе программистов [dvmn.org.](https://dvmn.org/)

Проект использует `long polling` [API DEVMAN](https://dvmn.org/api/docs/), чтобы получать результаты проверки работ студентов. Результаты отправляет `telegram bot`, а постоянную работу программы поддерживает платформа [Heroku.](https://dashboard.heroku.com)

## Подготовка к работе.
1. Создайте два `telegram bot`. Для этого отправьте пользователю `@BotFather` в `Telegram` команды `/start` и затем `/newbot`. Вы получите API токен для доступа к боту. В дальнейшем токен первого бота запишете в переменную `TELEGRAM_BOT_TOKEN`, на него будут приходить результаты проверки. Токен второго запишете в `TELEGRAM_LOGGING_BOT_TOKEN` на него будут приходить логи в случае неисправностей. 
Получите ID чата. Для этого отправьте `@userinfobot` в `Telegram` команду `/start`. В ответ он пришлет `Id`. Его в дальнем вы запишете в переменную `TELEGRAM_CHAT_ID`.

2. Зарегистрируйтесь на сайте [dvmn.org.](https://dvmn.org/) и получите [API токен](https://dvmn.org/api/docs/), его нужно будет записать в переменную `DVMN_API_TOKEN`.

## Для запуска на локальной машине.
1. Создайте файл `.env` в головном каталоге. Внутри файла напишите 
```
DVMN_API_TOKEN=значение
TELEGRAM_BOT_TOKEN=значение
TELEGRAM_LOGGING_BOT_TOKEN=значение
TELEGRAM_CHAT_ID=значение

```
2. Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
3. Запустите программу командой
```
python bot.py
```
## Для запуска на платформе Heroku.

1. Сделайте `Fork` данного репозитория.
2. Зарегистрируйтесь на платформе [Heroku](https://signup.heroku.com/login). На [странице приложений](https://dashboard.heroku.com/apps) создайте новое. Затем во вкладке `Deploy` в пункте `Deployment method` выберите `GitHub`. Привяжите к`Heroku` ваш аккаунт `GitHub` и укажите путь к репозиторию.  Сделайте `Deploy`. Затем зайдите во вкладку `Settings` на странице приложения, найдите `Config Vars` и заполните переменные окружения по образцу:

имя переменной | значение |
--- | --- |
DVMN_API_TOKEN |	|
TELEGRAM_BOT_TOKEN |	|	
TELEGRAM_LOGGING_BOT_TOKEN | |	
TELEGRAM_CHAT_ID | |

3. На странице приложения зайдите во вкладку `Resourses`.
Там вы увидете строку
```
 bot python3 bot.py 
```
Справа от нее есть значок, при наведении подсветится `Edit dyno formation`. Зайдите и запустите программу.

## Цель проекта

 Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/)
