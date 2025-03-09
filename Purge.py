__version__ = (1, 0, 1)

import asyncio
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class Purge(loader.Module):
    strings = {"name": "Purge"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    async def purgecmd(self, message: Message):
        chat = await message.get_chat()
        count = 0
        
        async for msg in self.client.iter_messages(chat):
            try:
                await msg.delete()
                count += 1
                if count % 500 == 0:
                    await message.edit(f"🚮 Удалено: {count}")
            except Exception:
                pass

        await message.delete()
        await self.client.send_message(chat, f"✅ Успешно удалено {count} сообщений")
