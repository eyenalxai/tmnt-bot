from aiogram import Router
from aiogram.types import Message
from lingua import Language

text_router = Router(name="text router")


@text_router.message()
async def text_handler(
    message: Message,
    language: Language | None,
    message_text: str,
) -> None:
    ...
