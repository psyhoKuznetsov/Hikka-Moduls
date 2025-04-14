__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import logging
from datetime import datetime
from typing import Optional
from telethon.tl.types import Message, PeerChannel
from telethon.errors import ChatIdInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from .. import loader, utils
import asyncio

@loader.tds
class DeleteChatMessagesModule(loader.Module):
    """Модуль для массового удаления сообщений в чате"""
    
    strings = {
        "name": "DeleteMessages",
        "description": "Модуль для удаления всех ваших сообщений в указанном чате.",
        "deleting": "<b>🗑 Удаление сообщений... ({count} найдено)</b>",
        "deleted": "<b>✅ Удалено {count} сообщений!</b>",
        "error": "<b>❌ Ошибка:</b> {error}",
        "no_messages": "<b>ℹ️ Сообщения не найдены</b>",
        "no_access": "<b>❌ Нет доступа к чату</b>"
    }

    def __init__(self):
        self._client = None
        self._db = None
        self._me = None
        self._batch_size = 100

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        seif._me = await client.get_me()
        try:
            await client(JoinChannelRequest("@psyhomodules"))
        except:
            pass

    async def _delete_batch(self, chat, messages: list) -> int:
        """Удаление сообщений пакетами"""
        try:
            await self._client.delete_messages(
                entity=chat,
                message_ids=[msg.id for msg in messages],
                revoke=True
            )
            return len(messages)
        except Exception as e:
            logging.error(f"Ошибка при пакетном удалении: {str(e)}")
            return 0

    async def delchatmecmd(self, message: Message):
        """Удалить все ваши сообщения в чате.
        Использование: <code>.delchatme [ID чата]</code>
        Если ID чата не указан, удаление происходит в текущем чате."""
        
        args = utils.get_args_raw(message)
        chat = await self._resolve_chat(args, message)
        if chat is None:
            return

        # Отправляем новое сообщение вместо редактирования исходного
        status_msg = await self._client.send_message(
            message.chat_id,
            self.strings["deleting"].format(count=0)
        )

        try:
            messages = []
            total_count = 0

            async for msg in self._client.iter_messages(
                chat,
                from_user=self._me.id,
                reverse=True,
                limit=None
            ):
                messages.append(msg)
                total_count += 1
                
                if total_count % 50 == 0:
                    try:
                        await status_msg.edit(self.strings["deleting"].format(count=total_count))
                    except Exception:
                        # Если редактирование не удалось, создаем новое сообщение
                        await status_msg.delete()
                        status_msg = await self._client.send_message(
                            message.chat_id,
                            self.strings["deleting"].format(count=total_count)
                        )
                
                if len(messages) >= self._batch_size:
                    deleted = await self._delete_batch(chat, messages)
                    total_count -= (len(messages) - deleted)
                    messages.clear()

            if messages:
                deleted = await self._delete_batch(chat, messages)
                total_count -= (len(messages) - deleted)

            final_text = (self.strings["deleted"].format(count=total_count) 
                         if total_count > 0 else self.strings["no_messages"])
            try:
                await status_msg.edit(final_text)
            except Exception:
                await status_msg.delete()
                await self._client.send_message(message.chat_id, final_text)
            
            await asyncio.sleep(2)
            await status_msg.delete()

        except ChatIdInvalidError:
            await self._client.send_message(
                message.chat_id,
                self.strings["error"].format(error="Недействительный ID чата")
            )
        except Exception as e:
            error_text = self.strings["error"].format(error=str(e))
            try:
                await status_msg.edit(error_text)
            except Exception:
                await status_msg.delete()
                await self._client.send_message(message.chat_id, error_text)
            logging.exception(f"Ошибка в delchatmecmd: {str(e)}")
        finally:
            # Убеждаемся, что статусное сообщение удаляется даже при ошибке
            try:
                await status_msg.delete()
            except Exception:
                pass

    async def _resolve_chat(self, args: str, message: Message) -> Optional[any]:
        """Получение объекта чата по ID или текущего чата"""
        try:
            if not args:
                return message.chat_id
            
            chat_id = int(args)
            if chat_id < 0:
                if chat_id <= -1000000000000:
                    chat_id = -1000000000000 + (chat_id % 1000000000000)
                chat = await self._client.get_entity(PeerChannel(chat_id))
            else:
                chat = await self._client.get_entity(chat_id)
            
            return chat
        except ValueError:
            await self._client.send_message(
                message.chat_id,
                self.strings["error"].format(error="Неверный формат ID чата")
            )
        except Exception as e:
            if "access" in str(e).lower():
                await self._client.send_message(message.chat_id, self.strings["no_access"])
            else:
                await self._client.send_message(
                    message.chat_id,
                    self.strings["error"].format(error="Чат не найден")
                )
            logging.exception(f"Ошибка при получении чата: {str(e)}")
        return None