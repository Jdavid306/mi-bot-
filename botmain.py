import os
import sys
import signal
import time
import logging
from threading import Thread
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# --- Configuración Básica ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"Z2013b", "X1314e", "F240e", "H876x", "Y389w", "J791s", "L184e", "T678v"}
ADMIN_ID = 5616748906

# --- Configuración de Logs Mejorada ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_runtime.log')
    ]
)
logger = logging.getLogger(__name__)

# --- Estado Global del Bot ---
class BotState:
    active = False
    restarting = False

# --- Manejadores de Señales ---
def handle_sigterm(signum, frame):
    """Maneja el cierre limpio del servicio"""
    logger.info("Recibida señal de terminación, cerrando limpiamente...")
    BotState.active = False
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

# --- Función de Reinicio Completo ---
def full_restart():
    """Reinicia completamente el proceso Python"""
    logger.warning("Iniciando reinicio completo...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# --- Core del Bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /start"""
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    if not BotState.active:
        await update.message.reply_text("🔄 El bot se está iniciando, por favor espera...")
        return
    
    await update.message.reply_text("¡Bot activado correctamente! 🚀")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador principal de mensajes"""
    if not BotState.active:
        await update.message.reply_text("⏳ El bot está en proceso de activación...")
        return
        
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return

    # --- Tu lógica original aquí ---
    texto_original = update.message.text.strip()
    estado = context.user_data.get('estado', 'esperando_clave')

    if context.user_data.get('tarea_finalizada'):
        await update.message.reply_text("🔧 Bot en mantenimiento, vuelve pronto")
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

# --- Sistema de Autoreparación ---
def health_monitor():
    """Hilo que monitorea y repara el bot automáticamente"""
    while True:
        time.sleep(30)
        
        if not BotState.active and not BotState.restarting:
            logger.error("Bot inactivo detectado - Forzando reinicio...")
            BotState.restarting = True
            full_restart()

def run_bot():
    """Inicia y mantiene el bot en ejecución"""
    retries = 0
    max_retries = 3
    
    while retries < max_retries:
        try:
            # Configuración de la aplicación
            app = Application.builder().token(TOKEN).build()
            
            # Registro de handlers
            app.add_handler(CommandHandler("start", start))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            # Inicio del bot
            logger.info("🚀 Iniciando bot de Telegram...")
            BotState.active = True
            BotState.restarting = False
            app.run_polling()
            
        except Exception as e:
            logger.error(f"Error crítico: {str(e)}")
            BotState.active = False
            retries += 1
            time.sleep(10 if retries < max_retries else 30)
    
    # Si supera los reintentos, reinicio completo
    full_restart()

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    # Iniciar monitor de salud
    Thread(target=health_monitor, daemon=True).start()
    
    # Iniciar bot principal
    run_bot()
