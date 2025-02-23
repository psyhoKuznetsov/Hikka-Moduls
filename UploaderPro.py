__version__ = (1, 1, 1)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
from telethon.tl.types import Message
import requests
import logging
from io import BytesIO
import random
import json

logger = logging.getLogger(__name__)

@loader.tds
class Uploader(loader.Module):
    """Универсальный модуль для загрузки файлов на различные сервисы."""
    strings = {
        "name": "UploaderPro",
        "description": "📤 Загружает файлы на различные сервисы (Catbox, Envs.sh, 0x0.st и др.).",
        "uploading": "🔄 <b>Загрузка файла...</b>",
        "no_reply": "❌ <b>Ответьте на медиа (фото, видео, файл) для загрузки.</b>",
        "success": "✅ <b>Файл успешно загружен!</b>\n🔗 <b>Ссылка:</b> <code>{}</code>",
        "error": "❌ <b>Ошибка при загрузке:</b> <code>{}</code>",
        "file_too_big": "❌ <b>Файл слишком большой для загрузки.</b>",
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def _get_file(self, message: Message):
        """Получает файл из сообщения."""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings["no_reply"])
            return None

        file = BytesIO()
        file.name = reply.file.name or f"file_{random.randint(1000, 9999)}.{reply.file.ext}"
        await self._client.download_media(reply.media, file)
        file.seek(0)
        return file

    async def _upload_to_service(self, file, service_url, field_name="file", extra_data=None):
        """Загружает файл на указанный сервис."""
        try:
            data = extra_data or {}
            files = {field_name: file}
            response = requests.post(service_url, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip()
            else:
                return None
        except Exception as e:
            logger.error(f"Ошибка при загрузке: {e}")
            return None

    async def _parse_json_response(self, response_text):
        """Парсит JSON-ответ и извлекает ссылку."""
        try:
            data = json.loads(response_text)
            if isinstance(data, dict) and data.get("success", False):
                if "files" in data and isinstance(data["files"], list):
                    return data["files"][0].get("url")
            elif "url" in data:
                return data["url"]
        except json.JSONDecodeError:
            return response_text  # Если ответ не JSON, возвращаем как есть
        return None

    @loader.unrestricted
    async def catboxcmd(self, message: Message):
        """Загружает файл на Catbox.moe. Используй: .catbox (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        link = await self._upload_to_service(
            file,
            "https://catbox.moe/user/api.php",
            field_name="fileToUpload",
            extra_data={"reqtype": "fileupload"}
        )
        if link:
            await utils.answer(message, self.strings["success"].format(link))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def envscmd(self, message: Message):
        """Загружает файл на Envs.sh. Используй: .envs (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        link = await self._upload_to_service(
            file,
            "https://envs.sh",
            field_name="file"
        )
        if link:
            await utils.answer(message, self.strings["success"].format(link))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def oxocmd(self, message: Message):
        """Загружает файл на 0x0.st. Используй: .oxo (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        link = await self._upload_to_service(
            file,
            "https://0x0.st",
            field_name="file"
        )
        if link:
            await utils.answer(message, self.strings["success"].format(link))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def x0cmd(self, message: Message):
        """Загружает файл на x0.at. Используй: .x0 (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        link = await self._upload_to_service(
            file,
            "https://x0.at",
            field_name="file"
        )
        if link:
            await utils.answer(message, self.strings["success"].format(link))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def tmpfilescmd(self, message: Message):
        """Загружает файл на tmpfiles.org. Используй: .tmpfiles (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        link = await self._upload_to_service(
            file,
            "https://tmpfiles.org/api/v1/upload",
            field_name="file"
        )
        if link:
            await utils.answer(message, self.strings["success"].format(link))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def pomfcmd(self, message: Message):
        """Загружает файл на pomf.lain.la. Используй: .pomf (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        response_text = await self._upload_to_service(
            file,
            "https://pomf.lain.la/upload.php",
            field_name="files[]"
        )
        if response_text:
            link = await self._parse_json_response(response_text)
            if link:
                await utils.answer(message, self.strings["success"].format(link))
            else:
                await utils.answer(message, self.strings["error"].format("Не удалось извлечь ссылку"))
        else:
            await utils.answer(message, self.strings["error"].format("Ошибка сервера"))

    @loader.unrestricted
    async def bashcmd(self, message: Message):
        """Загружает файл на bashupload.com. Используй: .bash (ответ на медиа)."""
        file = await self._get_file(message)
        if not file:
            return

        await utils.answer(message, self.strings["uploading"])
        try:
            response = requests.put(
                "https://bashupload.com",
                data=file.read()
            )
            if response.ok:
                urls = [line for line in response.text.split("\n") if "wget" in line]
                if urls:
                    url = urls[0].split()[-1]
                    await utils.answer(message, self.strings["success"].format(url))
                else:
                    await utils.answer(message, self.strings["error"].format("Не удалось найти ссылку"))
            else:
                await utils.answer(message, self.strings["error"].format(response.status_code))
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
