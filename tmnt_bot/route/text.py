from aiogram import Router
from aiogram.types import Message
from lingua import Language as LinguaLanguage
from result import Err
from spacy import Language as SpacyLanguage

from tmnt_bot.config.log import logger
from tmnt_bot.util.spacy import get_spacy_model_by_language
from tmnt_bot.util.words import extract_words_only

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

    spacy_model_result = get_spacy_model_by_language(
        language=language,
        nlp_en=nlp_en,
        nlp_ru=nlp_ru,
    )

    if isinstance(spacy_model_result, Err):
        logger.error(
            f"Could not get spacy thing for language {spacy_model_result.err_value}"
        )
        return

    words = extract_words_only(nlp=spacy_model_result.ok_value, text=message_text)
    await message.answer(text=f"Words: {words}")
