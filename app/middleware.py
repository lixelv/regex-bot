from typing import Callable, Dict, Any, Awaitable
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram import BaseMiddleware
from app.database import AsyncDB


class CheckDB(BaseMiddleware):
    def __init__(self, db: AsyncDB):
        super().__init__()
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type != ChatType.PRIVATE:
            return await handler(event, data)

        if not await self.db.user_exists(event.from_user.id):
            await self.db.add_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.language_code,
                event.date,
            )
        result = await handler(event, data)

        return result
