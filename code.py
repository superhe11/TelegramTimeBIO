import asyncio

import logging

import pytz

from datetime import datetime

from telethon import TelegramClient, functions, errors

from tzlocal import get_localzone



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def read_config(file_path):

    config = {}

    with open(file_path, 'r') as file:

        for line in file:

            line = line.strip()

            if line and '=' in line:

                key, value = line.split('=', 1)

                config[key] = value

    return config



config = read_config('config.txt')

api_id = int(config['api_id'])

api_hash = config['api_hash']

phone = config['phone']

language = config['language']



client = TelegramClient('session_name', api_id, api_hash)



async def update_bio():

    tz = get_localzone()

    current_time = datetime.now(tz).strftime('%H:%M')

    if language == 'en':

        new_bio = f'The current time is {current_time}'

    elif language == 'ru':

        new_bio = f'Сейчас {current_time}'

    else:

        new_bio = f'The current time is {current_time}'

    try:

        await client(functions.account.UpdateProfileRequest(about=new_bio))

        logging.info("Bio updated successfully.")

    except errors.RPCError as e:

        logging.error(f"Failed to update bio: {e}")



async def main():

    try:

        await client.start(phone)

        logging.info("Client started successfully.")

    except Exception as e:

        logging.error(f"Failed to start client: {e}")

        return

    tz = get_localzone()

    last_minute = datetime.now(tz).minute

    while True:

        current_minute = datetime.now(tz).minute

        if current_minute != last_minute:

            await update_bio()

            last_minute = current_minute

        await asyncio.sleep(1)



if __name__ == "__main__":

    with client:

        try:

            client.loop.run_until_complete(main())

        except OSError as e:

            logging.error(f"Network error: {e}")
