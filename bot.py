import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo desde GitHub Actions 🏖 siuuu")

if __name__ == "__main__":
    # Configuración correcta para v20.x
    application = Application.builder().token(TOKEN).build()
    
    # Añadir handlers
    application.add_handler(CommandHandler("start", start))
    
    # Iniciar el bot
    application.run_polling()
