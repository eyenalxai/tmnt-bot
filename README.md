## Usage

This application can be configured using the following environment variables:

- `TELEGRAM_TOKEN`: Your Telegram bot token.
- `POLL_TYPE`: Set to either `WEBHOOK` or `POLLING`.
- `PORT`: (Required if `POLL_TYPE` is set to `WEBHOOK`) The port number for the webhook server.
- `DOMAIN`: (Required if `POLL_TYPE` is set to `WEBHOOK`) The domain on which the webhook is set.
- `HOST`: (Default `0.0.0.0`) The host address for the server.
- `MAIN_BOT_PATH`: (Default `/webhook/main/tmnt-bot`) The path to the main Telegram bot's webhook endpoint.

