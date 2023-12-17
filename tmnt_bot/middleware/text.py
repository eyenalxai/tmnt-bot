from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from tmnt_bot.config.log import logger


async def filter_non_text(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("Message is not a Message, somehow")

    if message.text is not None:
        data["message_text"] = message.text
        return await handler(message, data)

    if message.caption is not None:
        data["message_text"] = message.caption
        return await handler(message, data)

    logger.error(f"No text in message?! Message: {message}")
    return None
