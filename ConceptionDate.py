__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
from telethon import types
import datetime

class ConceptionDate(loader.Module):
    """Определяет примерную дату зачатия по дате рождения. Используйте: .зачали [год] [месяц] [день]"""
    
    strings = {
        "name": "ConceptionDate",
        "no_args": "❌ <b>Формат:</b> <code>.зачали [год] [месяц] [день]</code>",
        "invalid_date": "❌ <b>Неверная дата. Используйте:</b> <code>.зачали [год] [месяц] [день]</code>",
        "future_date": "❌ <b>Дата рождения не может быть в будущем!</b>",
        "result": "🔍 <b>Примерная дата зачатия:</b> <code>{}</code>"
    }
    
    async def зачалиcmd(self, message: types.Message):
        """Рассчитывает примерную дату зачатия по дате рождения."""
        args = utils.get_args(message)
        if len(args) != 3:
            return await utils.answer(message, self.strings["no_args"])
        
        try:
            date = datetime.date(int(args[0]), int(args[1]), int(args[2]))
            if date > datetime.date.today():
                return await utils.answer(message, self.strings["future_date"])
            conception_date = date - datetime.timedelta(days=266)
            await utils.answer(message, self.strings["result"].format(conception_date.strftime("%d.%m.%Y")))
        except:
            await utils.answer(message, self.strings["invalid_date"])
