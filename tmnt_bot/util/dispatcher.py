import nltk  # type: ignore
import spacy
from aiogram import Dispatcher
from lingua import Language as LinguaLanguage
from lingua import LanguageDetectorBuilder
from nltk.corpus import cmudict  # type: ignore
from spacy import Language as SpacyLanguage

from tmnt_bot.config.log import logger
from tmnt_bot.middleware.language import detect_language
from tmnt_bot.middleware.text import filter_non_text
from tmnt_bot.middleware.user import filter_non_user
from tmnt_bot.route.text import text_router
from tmnt_bot.util.lifecycle import on_shutdown, on_startup


def add_language_detection(*, dispatcher: Dispatcher) -> Dispatcher:
    dispatcher["language_detector"] = LanguageDetectorBuilder.from_languages(
        LinguaLanguage.ENGLISH,
        LinguaLanguage.RUSSIAN,
    ).build()

    return dispatcher


def add_spacy_models(*, dispatcher: Dispatcher) -> Dispatcher:
    logger.info("Loading spacy models...")

    nlp_en: SpacyLanguage = spacy.load("en_core_web_sm")
    dispatcher["nlp_en"] = nlp_en
    logger.info("Loaded spacy model: en_core_web_sm")

    nlp_ru: SpacyLanguage = spacy.load("ru_core_news_sm")
    dispatcher["nlp_ru"] = nlp_ru
    logger.info("Loaded spacy model: ru_core_news_sm")

    return dispatcher


def add_cmudict(*, dispatcher: Dispatcher) -> Dispatcher:
    logger.info("Downloading cmudict for nltk")
    nltk.download(info_or_id="cmudict", raise_on_error=True)
    logger.info("Downloaded cmudict for nltk")

    dispatcher["cmudict_dict"] = cmudict.dict()
    return dispatcher


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher = add_language_detection(dispatcher=dispatcher)
    dispatcher = add_spacy_models(dispatcher=dispatcher)
    dispatcher = add_cmudict(dispatcher=dispatcher)

    dispatcher.include_router(router=text_router)

    text_router.message.middleware(filter_non_user)
    text_router.message.middleware(filter_non_text)
    text_router.message.middleware(detect_language)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher
