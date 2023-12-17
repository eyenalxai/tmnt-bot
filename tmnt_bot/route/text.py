from aiogram import Router
from aiogram.types import Message
from lingua import Language as LinguaLanguage
from spacy import Language as SpacyLanguage

from tmnt_bot.config.log import logger

text_router = Router(name="text router")


@text_router.message()
async def text_handler(
    message: Message,
    language: LinguaLanguage | None,
    nlp_en: SpacyLanguage,
    nlp_ru: SpacyLanguage,
    message_text: str,
) -> None:
    if language is None:
        logger.warning(f"No language detected for message text: {message_text}")
        return
