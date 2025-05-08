from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from flask import Flask
from threading import Thread
from datetime import datetime

# Configuración inicial
TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"Z2013b", "X1314e", "F240e", "H876x", "Y389w", "J791s", "L184e", "T678v"}
ADMIN_ID = 5616748906

# Mini servidor Flask para UptimeRobot
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    """Endpoint de salud para UptimeRobot"""
    if dentro_de_horario():
        return "OK", 200
    return "Fuera de horario ⏰", 503

def dentro_de_horario():
    """Verifica si está dentro del horario activo"""
    hora_actual = datetime.now().hour
    return (8 <= hora_actual < 12) or (14 <= hora_actual < 18) or (20 <= hora_actual < 1)

def run_flask():
    """Inicia el servidor Flask en segundo plano"""
    flask_app.run(host='0.0.0.0', port=8080)

# Funciones del bot
async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        mensaje = update.message.text
        reporte = (
            f"📩 Mensaje de < {user.full_name} >\n\n"
            f"📝 {mensaje}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=reporte)
    except Exception as e:
        print(f"Error en notificación: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    await notificar_admin(update, context)
    await update.message.reply_text("¡Hola!  ¿Quieres un regalo?  🎁  ¡Ingresa una clave! >")
    context.user_data.clear()
    context.user_data['estado'] = 'esperando_clave'

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    horarios = (
        "Ey, hola, este bot funciona en los siguientes horarios (Funciona cuando le da la gana ):\n\n"
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
        await update.message.reply_text("El bot esta en reparación, espera a la otra semana, \n\nJorge necesita tiempo 🛠️😴😴")
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

if __name__ == "__main__":
    # Inicia el servidor Flask en un hilo separado
    Thread(target=run_flask).start()
    
    # Inicia el bot de Telegram
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot en ejecución...")
    app.run_polling()
