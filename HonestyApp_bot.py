from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuración
import os
TOKEN = os.getenv("TOKEN")
WEB_APP_URL = "https://honestylearningapp.com"
MINIJUEGO_1_URL = "https://honestylearningapp.com/minijuego1"
MINIJUEGO_2_URL = "https://honestylearningapp.com/minijuego2"
COMPRA_TOKEN_URL = "https://pancakeswap.finance/?outputCurrency=0xAcd641A8ce3a373Cd0305d6212358227Ef2829E0"

# Base de datos simple para almacenar puntos de usuarios
usuarios_puntos = {}

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in usuarios_puntos:
        usuarios_puntos[user_id] = 0

    mensaje = f"Hola {user.first_name}! 🎮 Bienvenido al bot de nuestra comunidad.\n"
    mensaje += f"Tienes {usuarios_puntos[user_id]} puntos. 🎯"

    keyboard = [
        [InlineKeyboardButton("🌐 Acceder a la Web", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🎮 Jugar Minijuego 1", callback_data='jugar1')],
        [InlineKeyboardButton("🎮 Jugar Minijuego 2", callback_data='jugar2')],
        [InlineKeyboardButton("💰 Comprar Token", web_app=WebAppInfo(url=COMPRA_TOKEN_URL))],
        [InlineKeyboardButton("🎁 Canjear Recompensas", callback_data='recompensas')],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(mensaje, reply_markup=reply_markup)

# Función para asignar puntos al jugar
async def jugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    usuarios_puntos[user_id] += 10
    await query.answer(f"¡Has ganado 10 puntos! Ahora tienes {usuarios_puntos[user_id]} puntos.")
    await query.message.reply_text(f"🎉 ¡Felicidades! Ahora tienes {usuarios_puntos[user_id]} puntos.")

# Función para canjear recompensas
async def canjear_recompensas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if usuarios_puntos[user_id] >= 50:
        usuarios_puntos[user_id] -= 50
        await query.answer("🎁 Has canjeado 50 puntos por 1 token!")
        await query.message.reply_text(f"✅ Canje exitoso. Te quedan {usuarios_puntos[user_id]} puntos.")
    else:
        await query.answer("❌ No tienes suficientes puntos para canjear.")
        await query.message.reply_text("❌ Necesitas al menos 50 puntos para canjear un token.")

# Función de ayuda
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📌 Instrucciones:\n\n1️⃣ Usa '🎮 Jugar Minijuego 1/2' para ganar puntos.\n"
        "2️⃣ Acumula puntos y canjéalos en '🎁 Canjear Recompensas'.\n"
        "3️⃣ Usa '💰 Comprar Token' para adquirir más tokens.\n"
        "4️⃣ Si necesitas más ayuda, contáctanos."
    )

# Configuración del bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(jugar, pattern='jugar1|jugar2'))
    application.add_handler(CallbackQueryHandler(canjear_recompensas, pattern='recompensas'))
    application.add_handler(CallbackQueryHandler(help_command, pattern='help'))

    application.run_polling()

if __name__ == "__main__":
    main()
