from aiogram import Bot

from tmnt_bot.util.dispatcher import initialize_dispatcher
from tmnt_bot.util.lifecycle import start_bot
from tmnt_bot.util.settings import bot_settings


def main() -> None:
    bot = Bot(bot_settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
