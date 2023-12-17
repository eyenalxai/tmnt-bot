from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from tmnt_bot.config.log import logger
from tmnt_bot.util.health_check import health_check_endpoint
from tmnt_bot.util.settings import bot_settings


async def on_startup(bot: Bot) -> None:
    if bot_settings.poll_type == "WEBHOOK":
        await bot.set_webhook(bot_settings.webhook_url)
        logger.info(f"Webhook set to: {bot_settings.webhook_url}")


async def on_shutdown() -> None:
    logger.info("Shutting down...")


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
