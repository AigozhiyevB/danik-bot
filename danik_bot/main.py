from telegram_bot import TelegramBotApp, lambda_handler
import os
import pydotenv

if __name__ == "__main__":
    try:
        env = pydotenv.Environment(check_file_exists=True)
    except OSError:
        env = os.environ
    TELEGRAM_TOKEN = env.get("TELEGRAM_TOKEN")

    bot = TelegramBotApp(TELEGRAM_TOKEN)
    bot.run()
