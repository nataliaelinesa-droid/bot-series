import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# 👑 @natflixx_bot (para enviar alertas)
ADMIN_ID = 123456789  # troque pelo seu ID

# 🔔 Lista de usuários que ativaram alertas
usuarios_alerta = set()

# 🔥 LISTAS BOOKTOK
BOOKTOK_BR = [
    {"titulo": "O Acordo Perfeito", "autor": "Autora Brasileira", "nota": "4.7 ⭐", "link": "https://linkafiliado.com"},
    {"titulo": "Sombras da Meia-Noite", "autor": "Autora Nacional", "nota": "4.6 ⭐", "link": "https://linkafiliado.com"},
]

BOOKTOK_INT = [
    {"titulo": "Twisted Love", "autor": "Ana Huang", "nota": "4.1 ⭐", "link": "https://linkafiliado.com"},
    {"titulo": "Haunting Adeline", "autor": "H.D. Carlton", "nota": "4.2 ⭐", "link": "https://linkafiliado.com"},
]

TOP_SEMANA = [
    "🥇 Twisted Love",
    "🥈 O Acordo Perfeito",
    "🥉 Haunting Adeline",
]

# 🚀 MENU INICIAL
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        ["🔥 Bombando no BookTok"],
        ["🇧🇷 Destaques Nacionais", "🌍 Internacionais"],
        ["📈 Top da Semana"],
        ["🚨 Lançamentos"],
        ["🔔 Ativar Alertas"],
        ["💎 Área VIP"]
    ]

    reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    await update.message.reply_text(
        "📚 Radar BookTok BR & Internacional\n\nEscolha uma opção:",
        reply_markup=reply_markup
    )

# 📚 FUNÇÃO PARA MOSTRAR LISTAS
async def mostrar_lista(update: Update, lista):
    resposta = ""
    for livro in lista:
        resposta += (
            f"📖 {livro['titulo']}\n"
            f"✍️ {livro['autor']}\n"
            f"⭐ {livro['nota']}\n"
            f"🛒 Comprar: {livro['link']}\n\n"
        )
    await update.message.reply_text(resposta)

# 🎯 RESPOSTAS
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    user_id = update.message.from_user.id

    if texto == "🔥 Bombando no BookTok":
        await mostrar_lista(update, BOOKTOK_BR + BOOKTOK_INT)

    elif texto == "🇧🇷 Destaques Nacionais":
        await mostrar_lista(update, BOOKTOK_BR)

    elif texto == "🌍 Internacionais":
        await mostrar_lista(update, BOOKTOK_INT)

    elif texto == "📈 Top da Semana":
        await update.message.reply_text("\n".join(TOP_SEMANA))

    elif texto == "🚨 Lançamentos":
        await update.message.reply_text(
            "🚨 Último lançamento:\n\n📖 Novo Dark Romance Internacional\n📅 Lançado esta semana!"
        )

    elif texto == "🔔 Ativar Alertas":
        usuarios_alerta.add(user_id)
        await update.message.reply_text("🔔 Alertas ativados! Você receberá novidades.")

    elif texto == "💎 Área VIP":
        await update.message.reply_text(
            "💎 Área VIP:\n\nRanking antecipado + lista secreta.\nEm breve sistema de assinatura."
        )

# 📢 COMANDO ADMIN PARA ENVIAR ALERTA
async def novo_lancamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    mensagem = "🚨 NOVO LANÇAMENTO BOOKTOK!\n\n📖 Título\n✍️ Autor\n⭐ Nota\n🛒 Link"

    for user_id in usuarios_alerta:
        try:
            await context.bot.send_message(chat_id=user_id, text=mensagem)
        except:
            pass

    await update.message.reply_text("✅ Alerta enviado!")

# 🔧 INICIALIZAÇÃO
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("novo", novo_lancamento))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

app.run_polling()
