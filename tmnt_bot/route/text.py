from aiogram import Router
from aiogram.types import Message
from lingua import Language as LinguaLanguage
from result import Err
from spacy import Language as SpacyLanguage

from tmnt_bot.config.log import logger
from tmnt_bot.util.pyphen import get_pyphen_by_language
from tmnt_bot.util.spacy import get_spacy_model_by_language
from tmnt_bot.util.syllables import count_syllables
from tmnt_bot.util.words import extract_words_only

text_router = Router(name="text router")


@text_router.message()
async def text_handler(
    message: Message,
    language: LinguaLanguage | None,
    nlp_en: SpacyLanguage,
    nlp_ru: SpacyLanguage,
    cmudict_dict: dict,
    message_text: str,
) -> None:
    if len(message_text) > 80:
        return

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

    pyphen_result = get_pyphen_by_language(language=language)

    if isinstance(pyphen_result, Err):
        logger.error(
            f"Could not get pyphen thing for language {pyphen_result.err_value}"
        )
        return

    words = extract_words_only(nlp=spacy_model_result.ok_value, text=message_text)

    if len("".join(words)) > 60:
        return

    syllables_count_result = count_syllables(
        language=language,
        pyphen=pyphen_result.ok_value,
        cmudict_dict=cmudict_dict,
        words=words,
    )

    if isinstance(syllables_count_result, Err):
        logger.error(
            f"Could not count syllables for language {syllables_count_result.err_value}"
        )
        return

    if syllables_count_result.ok_value == 8:
        await message.reply("TMNT")
