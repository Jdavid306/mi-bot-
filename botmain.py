from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from flask import Flask
from threading import Thread
from datetime import datetime
import logging
import asyncio

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuración inicial
TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"Z2013b", "X1314e", "F240e", "H876x", "Y389w", "J791s", "L184e", "T678v"}
ADMIN_ID = 5616748906

# Servidor Flask optimizado
flask_app = Flask(__name__)
PORT = int(os.environ.get('PORT', 8080))

@flask_app.route('/')
def health_check():
    hora_actual = datetime.now().hour
    status = 200 if (8 <= hora_actual < 12) or (14 <= hora_actual < 18) or (20 <= hora_actual < 1) else 503
    return f"Bot Status: {'OK' if status == 200 else 'Fuera de horario'}", status

@flask_app.route('/ping')
def ping():
    return "pong", 200

def run_flask():
    from waitress import serve
    serve(flask_app, host="0.0.0.0", port=PORT)

# Funciones del bot
async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        mensaje = update.message.text
        reporte = f"📩 Mensaje de <{user.full_name}>\n\n📝 {mensaje}"
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
    
    horarios = (
        "Horarios de funcionamiento:\n\n"
        "• 8:30 AM - 12:00 PM\n"
        "• 2:00 PM - 6:00 PM\n"
        "• 8:00 PM - 1:00 AM"
    )
    await update.message.reply_text(horarios)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    await notificar_admin(update, context)
    texto_original = update.message.text.strip()
    estado = context.user_data.get('estado', 'esperando_clave')

    if context.user_data.get('tarea_finalizada'):
        await update.message.reply_text("El bot está en mantenimiento 🛠️")
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

async def reset_telegram_connection():
    """Reinicia la conexión con Telegram"""
    bot = Bot(token=TOKEN)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.close()
        logger.info("Conexión con Telegram reiniciada correctamente")
    except Exception as e:
        logger.error(f"Error reiniciando conexión: {e}")

async def run_bot():
    """Función principal con autoreconexión"""
    while True:
        try:
            await reset_telegram_connection()
            
            app = Application.builder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("info", info))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            logger.info("Iniciando bot...")
            await app.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error en el bot: {e}. Reconectando en 10 segundos...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    # Inicia servidor Flask
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"Servidor Flask iniciado en puerto {PORT}")
    
    # Inicia el bot con autoreconexión
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente")
