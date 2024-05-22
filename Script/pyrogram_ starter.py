from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "telegram_api_id": int(os.getenv("TG_API_ID")),
    "telegram_hash": os.getenv("TG_API_HASH"),
}

app = Client("my_account",CONFIG["telegram_api_id"],CONFIG["telegram_hash"])


with app:
    app.send_message("me", "Hello from pyrogram")
    app = Client("my_account",CONFIG["telegram_api_id"],CONFIG["telegram_hash"])

chat_id = -1001130580549

async def main():
    async with app:
        async for message in app.get_chat_history(chat_id):
            print(message)

app.run(main())







