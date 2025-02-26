__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import asyncio
import logging
from telethon import events

logger = logging.getLogger(__name__)

@loader.tds
class AudioToTextMod(loader.Module):
    """Расшифровка аудио/видео"""

    strings = {
        "name": "звук в текст",
        "processing": "🔮 <b>Обработка...</b>",
        "no_reply": "🚫 <b>Ответьте на голосовое или видеосообщение!</b>",
        "result": "📜 <b>Результат:</b>\n\n{}",
        "error": "❌ <b>Ошибка при обработке сообщения.</b>",
        "timeout": "⏱ <b>Превышено время ожидания ответа от бота.</b>",
        "waiting": "⏳ <b>Ожидание ответа от бота...</b>"
    }
    
    def __init__(self):
        self.bot_username = "@smartspeech_sber_bot"
        self.name = self.strings["name"]
    
    async def _send_to_bot(self, message):
        try:
            bot_msg = await self._client.send_message(self.bot_username, file=message.media)
            
           
            await asyncio.sleep(1)
            
            start_time = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_time < 120:
                
                async for msg in self._client.iter_messages(self.bot_username, limit=5):
                   
                    if msg.from_id and msg.id != bot_msg.id:
                       
                        if msg.text and not msg.text.startswith("/"):
                            return msg.text
                
                await asyncio.sleep(2)
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка в _send_to_bot: {e}", exc_info=True)
            return None

    async def _delete_bot_chat(self):
        try:
            async for message in self._client.iter_messages(self.bot_username, limit=50):
                await self._client.delete_messages(self.bot_username, message.id)
                await asyncio.sleep(0.3)
        except Exception as e:
            logger.error(f"Ошибка в _delete_bot_chat: {e}", exc_info=True)

    @loader.command()
    async def atxt(self, message):
        """Использование: ответьте на голосовое сообщение или видеозаметку командой .atxt"""
        reply = await message.get_reply_message()

        if not reply or not hasattr(reply, 'media') or not (
            hasattr(reply.media, 'document') and 
            (getattr(reply.media.document, 'attributes', None) and 
             any(getattr(attr, 'CONSTRUCTOR_ID', None) in (1989037971, 1923290508) 
                 for attr in reply.media.document.attributes))
            or reply.voice or reply.video_note
        ):
            return await utils.answer(message, self.strings["no_reply"])

        msg = await utils.answer(message, self.strings["processing"])
        
        await utils.answer(msg, self.strings["waiting"])
        
        result = await self._send_to_bot(reply)
        
        if result:
            await utils.answer(msg, self.strings["result"].format(result))
        else:
            await utils.answer(msg, self.strings["timeout"])
        
        await self._delete_bot_chat()