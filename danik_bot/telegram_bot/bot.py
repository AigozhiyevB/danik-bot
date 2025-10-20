import json
import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import logging
from langchain_rag.bedrock_rag import DanikBotBedrockPipeline

pipeline = DanikBotBedrockPipeline()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name or 'товарищ'}! Я твой друг Даник-путеводитель по ресторанам Алматы"
        "Чем могу помочь?"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    await update.message.reply_text(
        "Вот мои команды:\n"
        "/start - Запустить меня\n"
        "/help - Помощь\n"
        "Перейдем к выбору места?"
    )


# --- Message Handler ---
async def ask_rag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo back any text message."""
    user_text = update.message.text
    answer = pipeline.process_query(user_text)
    await update.message.reply_text(answer.content)


# --- Error Handler ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


class TelegramBotApp:
    def __init__(self, token: str):
        self.token = token
        self.app = ApplicationBuilder().token(self.token).build()

        # Register handlers
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(CommandHandler("help", help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rag))

        # Error handler
        self.app.add_error_handler(error_handler)

    def run(self):
        """Start the bot."""
        logger.info("🚀 Bot is running...")
        self.app.run_polling()


def lambda_handler(event, context):
    """AWS Lambda handler."""
    # Extract the Telegram webhook payload
    tmp = event if isinstance(event, dict) else json.loads(event)
    body = json.loads(tmp['body'])
    update = Update.de_json(body)

    # Set up the ApplicationBuilder with the Telegram token
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_rag))

    # Process the incoming update
    asyncio.run(app.initialize())
    asyncio.run(app.process_update(update))

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Success'})
    }
