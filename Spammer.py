__version__ = (1, 7, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import asyncio

@loader.tds
class LightSpamMod(loader.Module):
    """Автоматический отправщик сообщений"""
    
    strings = {
        "name": "Spammer",
        "cfg_err": "<b>❌ Формат: .spam [чат]|[текст]|[задержка]</b>",
        "started": "<b>✅ Отправка запущена</b>",
        "stopped": "<b>🛑 Отправка остановлена</b>",
        "not_cfg": "<b>❌ Сначала настройте командой .spam</b>"
    }

    def __init__(self):
        self.active = False
        self.chat = None
        self.text = None
        self.delay = None
        self.task = None

    @loader.command()
    async def ls(self, message):
        """Настройка: .spam [чат]|[текст]|[задержка]"""
        args = utils.get_args_raw(message).split("|")
        
        if len(args) != 3:
            return await message.edit(self.strings["cfg_err"])
            
        try:
            self.chat = int(args[0])
            self.text = args[1]
            self.delay = float(args[2])
            await message.edit("<b>✅ Настроено! Используйте .ls для запуска</b>")
            
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка:</b> {str(e)}")

    @loader.command()
    async def ls(self, message):
        """Запустить отправку"""
        if not self.chat:
            return await message.edit(self.strings["not_cfg"])
            
        self.active = True
        self.task = asyncio.create_task(self.sender())
        await message.edit(self.strings["started"])

    @loader.command()
    async def ls(self, message):
        """Остановить отправку"""
        self.active = False
        if self.task:
            self.task.cancel()
        await message.edit(self.strings["stopped"])

    async def sender(self):
        while self.active:
            try:
                await self.client.send_message(self.chat, f"<b>{self.text}</b>")
                await asyncio.sleep(self.delay)
            except Exception:
                break
