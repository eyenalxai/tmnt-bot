from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from lingua import Language, LanguageDetectorBuilder

from tmnt_bot.config.log import logger
from tmnt_bot.settings import bot_settings
from tmnt_bot.util.health_check import health_check_endpoint


async def on_startup(bot: Bot) -> None:
    if bot_settings.poll_type == "WEBHOOK":
        await bot.set_webhook(bot_settings.webhook_url)
        logger.info(f"Webhook set to: {bot_settings.webhook_url}")


async def on_shutdown() -> None:
    logger.info("Shutting down...")


def add_language_detection(*, dispatcher: Dispatcher) -> Dispatcher:
    dispatcher["language_detector"] = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH,
        Language.RUSSIAN,
    ).build()

    return dispatcher


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())
    dispatcher = add_language_detection(dispatcher=dispatcher)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher


def start_bot(*, dispatcher: Dispatcher, bot: Bot) -> None:
    if bot_settings.poll_type == "WEBHOOK":
        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app,
            path=bot_settings.main_bot_path,
        )
        setup_application(app, dispatcher, bot=bot)
        app.add_routes([web.get("/health", health_check_endpoint)])
        web.run_app(app, host=bot_settings.host, port=bot_settings.port)

    if bot_settings.poll_type == "POLLING":
        dispatcher.run_polling(bot, skip_updates=True)


def main() -> None:
    bot = Bot(bot_settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
