from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests

TOKEN = os.getenv("TOKEN")
TMDB_KEY = os.getenv("TMDB_KEY")

# 🎬 IDs oficiais corretos do TMDB para TV
GENRES = {
    "Ação": 10759,        # Action & Adventure
    "Comédia": 35,
    "Terror": 9648,       # Mystery (terror real para TV quase não existe separado)
    "Romance": 10749
}

def buscar_series_por_genero(genre_id):
    url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_KEY}&with_genres={genre_id}&language=pt-BR&sort_by=popularity.desc"

    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            return "Erro ao conectar com a API 😢"

        data = response.json()
        series = data.get("results", [])

        if not series:
            return "Não encontrei séries 😢"

        resultado = ""
        for s in series[:3]:
            nome = s.get("name", "Sem nome")
            resultado += f"📺 {nome}\n"

        return resultado

    except Exception as e:
        return "Erro inesperado 😢"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        ["Ação", "Romance"],
        ["Comédia", "Terror"]
    ]

    reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    await update.message.reply_text(
        "Oi! 🎬 Eu sou seu bot de séries.\nEscolha um gênero:",
        reply_markup=reply_markup
    )

async def responder_genero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genero = update.message.text

    if genero in GENRES:
        recomendacoes = buscar_series_por_genero(GENRES[genero])
        await update.message.reply_text(
            f"🎬 Recomendações de {genero}:\n\n{recomendacoes}"
        )
    else:
        await update.message.reply_text("Escolha um gênero usando os botões 😉")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_genero))

app.run_polling()
