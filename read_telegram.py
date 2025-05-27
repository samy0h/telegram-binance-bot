from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import asyncio

api_id = 22874799      # <-- استبدله بـ api_id الخاص بك
api_hash = '1173f8b66f57f86cbdf61fb7526a7c80'
                  # <-- استبدله بـ api_hash الخاص بك
async def main():
    async with TelegramClient('my_session', api_id, api_hash) as client:
        print("📡 القنوات التي أنت مشترك بها:")

        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.is_channel:
                print(f"- {dialog.name} | ID: {dialog.id}")

asyncio.run(main())