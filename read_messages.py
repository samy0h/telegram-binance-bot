import asyncio
from telethon import TelegramClient

api_id = 22874799       # ← استبدل هذا بالـ API ID الخاص بك
api_hash = '1173f8b66f57f86cbdf61fb7526a7c80'

channel_id = -1002339729195  # ← ID القناة المستهدفة

async def main():
    async with TelegramClient('my_session', api_id, api_hash) as client:
        print("✅ تم تسجيل الدخول إلى تيليجرام.")
        channel = await client.get_entity(channel_id)
        
        print("📥 آخر 5 رسائل من القناة:")
        async for message in client.iter_messages(channel, limit=5):
            print("🔹", message.text)
            print("=" * 50)

asyncio.run(main())
