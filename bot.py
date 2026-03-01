import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
TMDB_KEY = os.getenv("TMDB_API_KEY")

print("TMDB_KEY carregada:", TMDB_KEY)

GENRES = {
    "Ação": 10759,
    "Comédia": 35,
    "Terror": 9648,
    "Romance": 10749,
}

# 🔎 Função que busca séries + temporadas + episódios
def buscar_series_por_genero(genre_id):
    try:
        url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_KEY}&with_genres={genre_id}&language=pt-BR&sort_by=popularity.desc"
        
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Erro ao conectar com a API 😢"

        data = response.json()
        series = data.get("results", [])[:3]

        if not series:
            return "Não encontrei séries 😢"

        resultado = ""

        for s in series:
            try:
                serie_id = s.get("id")
                nome = s.get("name", "Sem nome")

                detalhes_url = f"https://api.themoviedb.org/3/tv/{serie_id}?api_key={TMDB_KEY}&language=pt-BR"
                detalhes_resp = requests.get(detalhes_url, timeout=10)

                if detalhes_resp.status_code == 200:
                    detalhes = detalhes_resp.json()
                    temporadas = detalhes.get("number_of_seasons", "?")
                    episodios = detalhes.get("number_of_episodes", "?")

                    resultado += (
                        f"📺 {nome}\n"
                        f"📀 {temporadas} temporadas\n"
                        f"🎬 {episodios} episódios\n\n"
                    )
                else:
                    resultado += f"📺 {nome}\n\n"

            except Exception:
                resultado += f"📺 {nome}\n\n"

        return resultado

    except Exception:
        return "Erro ao conectar com a API 😢"


# 🚀 Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Ação", "Romance"], ["Comédia", "Terror"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Oi! 🎬 Eu sou seu bot de séries.\nEscolha um gênero:",
        reply_markup=reply_markup
    )


# 🎯 Quando usuário escolhe gênero
async def responder_genero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genero = update.message.text

    if genero in GENRES:
        genre_id = GENRES[genero]
        resultado = buscar_series_por_genero(genre_id)

        await update.message.reply_text(
            f"🎬 Recomendações de {genero}:\n\n{resultado}"
        )


# 🔧 Inicialização
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_genero))

app.run_polling()



