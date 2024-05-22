from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')
channel_username = 'mr_trump_poems' 



client = TelegramClient('poems', api_id, api_hash)


async def main():

    await client.start()
    #if not await client.is_user_authorized():
     #   await client.send_code_request(phone)
      #  await client.sign_in(phone, input('Enter the code: '))

    entity = await client.get_entity(channel_username)

    with open ('poem_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['id', 'message', 'date'])

        async for message in client.iter_messages(entity, limit =2000):
            writer.writerow([message.id, message.message, message.date])


with client:
    client.loop.run_until_complete(main())
