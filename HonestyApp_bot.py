from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Configuración
import os
TOKEN = os.getenv("TOKEN")

WEB_APP_URL = "www.honestylearningapp"
MINIJUEGO_1_URL = "https://www.honestylearningapp/minijuego1"
MINIJUEGO_2_URL = "https://www.honestylearningapp/minijuego2"
COMPRA_TOKEN_URL = "https://pancakeswap.finance/?outputCurrency=0xAcd641A8ce3a373Cd0305d6212358227Ef2829E0"

# Función de inicio
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    mensaje = f"Hola {user.first_name}! 🎮 Bienvenido al bot de nuestra comunidad."

    keyboard = [
        [InlineKeyboardButton("🌐 Acceder a la Web", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("🎮 Jugar Minijuego 1", web_app=WebAppInfo(url=MINIJUEGO_1_URL))],
        [InlineKeyboardButton("🎮 Jugar Minijuego 2", web_app=WebAppInfo(url=MINIJUEGO_2_URL))],
        [InlineKeyboardButton("💰 Comprar Token", web_app=WebAppInfo(url=COMPRA_TOKEN_URL))],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(mensaje, reply_markup=reply_markup)

# Función de ayuda
def help_command(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.reply_text(
        "📌 Instrucciones:\n\n1️⃣ Usa el botón '🌐 Acceder a la Web' para entrar a la plataforma.\n"
        "2️⃣ Usa '🎮 Jugar Minijuego 1/2' para jugar los minijuegos.\n"
        "3️⃣ Usa '💰 Comprar Token' para adquirir tokens.\n"
        "4️⃣ Si necesitas más ayuda, contáctanos."
    )

# Configuración del bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(help_command, pattern='help'))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
