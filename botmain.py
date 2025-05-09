from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from flask import Flask
from threading import Thread
import time
import logging
import sys

# Configuración básica
TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"Z2013b", "X1314e", "F240e", "H876x", "Y389w", "J791s", "L184e", "T678v"}
ADMIN_ID = 5616748906

# Configuración de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Servidor Flask mínimo
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    """Endpoint básico para mantener el servicio activo"""
    return "OK", 200

def run_flask():
    """Inicia Flask en segundo plano"""
    flask_app.run(host='0.0.0.0', port=8080)

# Función para reiniciar el bot
def reiniciar_bot():
    """Reinicia el proceso actual"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Handlers originales (sin cambios)
async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        mensaje = update.message.text
        reporte = f"📩 Mensaje de < {user.full_name} >\n\n📝 {mensaje}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=reporte)
    except Exception as e:
        logger.error(f"Error en notificación: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    await notificar_admin(update, context)
    await update.message.reply_text("¡Hola! ¿Quieres un regalo? 🎁 ¡Ingresa una clave! >")
    context.user_data.clear()
    context.user_data['estado'] = 'esperando_clave'

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    horarios = "Ey, hola, este bot funciona en los siguientes horarios:\n\n• 8:30 AM - 12:00 PM\n• 2:00 PM - 6:00 PM\n• 8:00 PM - 1:00 AM"
    await update.message.reply_text(horarios)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    await notificar_admin(update, context)
    
    texto_original = update.message.text.strip()
    estado = context.user_data.get('estado', 'esperando_clave')

    if context.user_data.get('tarea_finalizada'):
        await update.message.reply_text("El bot está en reparación, espera a la otra semana.\n\nJorge necesita tiempo 🛠️😴😴")
        return

    if estado == 'esperando_clave':
        if texto_original in CLAVES_VALIDAS:
            context.user_data.clear()
            import regalo2
            await regalo2.iniciar_flujo(update, context)
        else:
            await update.message.reply_text("❌ Clave incorrecta")
    else:
        import regalo2
        await regalo2.manejar_flujo(update, context)

def main():
    """Función principal con autoreconexión mejorada"""
    while True:
        try:
            # Inicia Flask en segundo plano
            flask_thread = Thread(target=run_flask)
            flask_thread.daemon = True
            flask_thread.start()

            # Inicia el bot de Telegram
            app = Application.builder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("info", info))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            logger.info("Bot iniciado correctamente")
            app.run_polling()
            
        except Exception as e:
            logger.error(f"Error crítico: {e}. Reiniciando en 30 segundos...")
            time.sleep(30)
            reiniciar_bot()

if __name__ == "__main__":
    main()
