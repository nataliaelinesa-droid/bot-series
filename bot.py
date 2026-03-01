from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8782801826:AAGZwa4uLmNtfKJ7-XLc0AqH8-9OCkOv5O8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Oi! 🎬 Eu sou seu bot de séries.\nQual gênero você gosta?"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()