from typing import Literal, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    telegram_token: str

    poll_type: Literal["WEBHOOK", "POLLING"]
    port: int | None = None
    domain: str | None = None
    host: str = Field(default="0.0.0.0")
    main_bot_path: str = "/webhook/main/tmnt-bot"

    @property
    def webhook_url(self: Self) -> str:
        return "{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    @model_validator(mode="after")  # type: ignore
    def validate_frontend_urls(self: Self) -> None:
        errors = []
        if self.poll_type == "WEBHOOK":
            if self.port is None:
                errors.append("PORT is required for WEBHOOK mode")

            if self.domain is None:
                errors.append("DOMAIN is required for WEBHOOK mode")

        if len(errors) > 0:
            errors_str = "\n".join(errors)
            raise ValueError(f"\n\nInvalid settings: \n{errors_str}\n\n")


bot_settings = BotSettings()  # type: ignore
