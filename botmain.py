from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from flask import Flask
from threading import Thread
from datetime import datetime
import logging
import asyncio
import time

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
    logger.info(f"Iniciando servidor Flask en puerto {PORT}")
    serve(flask_app, host="0.0.0.0", port=PORT)

# Funciones del bot (manteniendo tu lógica original)
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

async def run_bot():
    """Función principal mejorada para manejo de conexiones"""
    while True:
        try:
            # Configuración inicial limpia
            application = Application.builder().token(TOKEN).build()
            
            # Registro de handlers
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("info", info))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            # Limpieza inicial
            bot = Bot(TOKEN)
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.close()
            
            logger.info("Iniciando bot de Telegram...")
            await application.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error en el bot: {str(e)}")
            logger.info("Reintentando en 30 segundos...")
            time.sleep(30)  # Espera más larga para evitar flood control

def main():
    # Inicia Flask en un hilo separado
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Inicia el bot en el hilo principal
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente")
    except Exception as e:
        logger.error(f"Error fatal: {str(e)}")

if __name__ == "__main__":
    main()
