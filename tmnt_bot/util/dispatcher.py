from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from lingua import Language, LanguageDetectorBuilder

from tmnt_bot.middleware.language import detect_language
from tmnt_bot.middleware.text import filter_non_text
from tmnt_bot.middleware.user import filter_non_user
from tmnt_bot.route.text import text_router
from tmnt_bot.util.lifecycle import on_shutdown, on_startup


def add_language_detection(*, dispatcher: Dispatcher) -> Dispatcher:
    dispatcher["language_detector"] = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH,
        Language.RUSSIAN,
    ).build()

    return dispatcher


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())
    dispatcher = add_language_detection(dispatcher=dispatcher)

    dispatcher.include_router(router=text_router)

    text_router.message.middleware(filter_non_user)
    text_router.message.middleware(filter_non_text)
    text_router.message.middleware(detect_language)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher
