from telegram_bot import TelegramBotApp
import pydotenv

if __name__ == "__main__":
    env = pydotenv.Environment()
    TELEGRAM_TOKEN = env.get("TELEGRAM_TOKEN")

    bot = TelegramBotApp(TELEGRAM_TOKEN)
    bot.run()
