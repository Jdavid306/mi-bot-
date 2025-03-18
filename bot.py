import os
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text('¡Hola! Soy tu bot en GitHub Actions 🚀')

TOKEN = os.environ["TELEGRAM_TOKEN"]  # Token desde variables de entorno

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
updater.idle()  # Mantiene el bot en ejecución
