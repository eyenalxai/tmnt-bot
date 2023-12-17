from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from tmnt_bot.config.log import logger


async def filter_non_user(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("Message is not a Message, somehow")

    if not message.from_user:
        logger.info("No user in message")
        return None

    return await handler(message, data)
