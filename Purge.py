__version__ = (1, 0, 2)

import asyncio
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class Purge(loader.Module):
    """Удаляет все сообщения в чате очень быстро"""
    strings = {"name": "Purge"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def purgecmd(self, message: Message):
        """Полностью очистить чат"""
        chat = await message.get_chat()
        count = 0
        msg_ids = []

        async for msg in self.client.iter_messages(chat, reverse=True):
            msg_ids.append(msg.id)
            if len(msg_ids) >= 100: 
                await self.client.delete_messages(chat, msg_ids)
                count += len(msg_ids)
                msg_ids = []

                if count % 500 == 0:
                    await message.edit(f"🚮 Удалено: {count}")

        if msg_ids:
            await self.client.delete_messages(chat, msg_ids)
            count += len(msg_ids)

        await message.delete()
        await self.client.send_message(chat, f"✅ Успешно удалено {count} сообщений")
