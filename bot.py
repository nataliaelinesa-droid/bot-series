from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

# Lista de gêneros
generos = [["Ação", "Romance"], ["Comédia", "Terror"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = ReplyKeyboardMarkup(generos, resize_keyboard=True)
    await update.message.reply_text(
        "Oi! 🎬 Eu sou seu bot de séries.\nEscolha um gênero:",
        reply_markup=teclado
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genero = update.message.text

    if genero == "Ação":
        resposta = "🔥 Recomendo: Breaking Bad"
    elif genero == "Romance":
        resposta = "❤️ Recomendo: Bridgerton"
    elif genero == "Comédia":
        resposta = "😂 Recomendo: Brooklyn 99"
    elif genero == "Terror":
        resposta = "👻 Recomendo: The Haunting of Hill House"
    else:
        resposta = "Escolha um gênero pelos botões 😉"

    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

app.run_polling()
