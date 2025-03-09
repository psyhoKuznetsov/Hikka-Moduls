__version__ = (1, 7, 1)

from .. import loader, utils
import asyncio

@loader.tds
class Spammer(loader.Module):
    """Спамер для чатов"""

    strings = {
        "name": "Spammer",
        "cfg_err": "<b>❌ Формат: .spam [текст]|[задержка]</b>",
        "started": "<b>✅ Отправка запущена в текущий чат</b>",
        "stopped": "<b>🛑 Отправка остановлена</b>",
        "not_cfg": "<b>❌ Сначала настройте командой .spam</b>",
        "configured": "<b>✅ Настроено! Используйте .start для запуска</b>",
        "id": "<b>🆔 ID:</b> <code>{}</code>"
    }

    def __init__(self):
        self.active = False
        self.text = None
        self.delay = None
        self.task = None

    @loader.command()
    async def spam(self, message):
        """Настройка: .spam [текст]|[задержка]"""
        args = utils.get_args_raw(message).split("|")
        
        if len(args) != 2:
            return await message.edit(self.strings["cfg_err"])
            
        try:
            self.text = args[0]
            self.delay = float(args[1])
            await message.edit(self.strings["configured"])
            
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка:</b> {str(e)}")

    @loader.command()
    async def start(self, message):
        """Запустить отправку в текущий чат"""
        if not self.text or not self.delay:
            return await message.edit(self.strings["not_cfg"])
            
        self.active = True
        self.task = asyncio.create_task(self.sender(message.chat_id))
        await message.edit(self.strings["started"])

    @loader.command()
    async def stop(self, message):
        """Остановить отправку"""
        self.active = False
        if self.task:
            self.task.cancel()
        await message.edit(self.strings["stopped"])

    async def sender(self, chat_id):
        """Функция отправки сообщений"""
        while self.active:
            try:
                await self.client.send_message(chat_id, self.text)
                await asyncio.sleep(self.delay)
            except Exception as e:
                await self.client.send_message(chat_id, f"<b>❌ Ошибка при отправке:</b> {str(e)}")
                break

    @loader.command()
    async def getid(self, message):
        """Получить ID чата или пользователя"""
        reply = await message.get_reply_message()
        if reply:
            user_id = reply.sender_id
            return await message.edit(self.strings["id"].format(user_id))
        else:
            chat_id = message.chat_id
            return await message.edit(self.strings["id"].format(chat_id))
