import time
import pytz
from datetime import datetime
from telethon.sync import TelegramClient, functions

# Функция для чтения конфигурационного файла
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Чтение конфигурации
config = read_config('config.txt')

# Извлечение параметров из конфигурации
api_id = config['api_id']
api_hash = config['api_hash']
phone = config['phone']
update_interval = int(config['update_interval'])
language = config['language']
timezone = config['timezone']

# Создаём клиента
client = TelegramClient('session_name', api_id, api_hash)

async def update_bio():
    # Получение текущего времени в заданном часовом поясе
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz).strftime('%H:%M')
    
    if language == 'en':
        new_bio = f'The current time is {current_time}'
    elif language == 'ru':
        new_bio = f'Сейчас {current_time}'
    else:
        new_bio = f'The current time is {current_time}'  # Значение по умолчанию

    # Обновление BIO профиля
    await client(functions.account.UpdateProfileRequest(about=new_bio))

async def main():
    # Авторизация
    await client.start(phone)
    
    # Получение текущего времени в заданном часовом поясе для ожидания первого изменения времени
    tz = pytz.timezone(timezone)
    last_minute = datetime.now(tz).minute
    
    while True:
        current_minute = datetime.now(tz).minute
        if current_minute != last_minute:
            await update_bio()
            last_minute = current_minute
            time.sleep(update_interval)

# Запуск клиента
with client:
    client.loop.run_until_complete(main())
