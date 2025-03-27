from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"D122v", "P278v", "L341m"}
ADMIN_ID = 5616748906

async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('modulo_activo'):
        return
    
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
    await update.message.reply_text("¡Hola!  ¿Quieres un regalo?  🎁  ¡Ingresa una clave!")
    context.user_data.clear()
    context.user_data['estado'] = 'esperando_clave'

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    horarios = (
        "Ey, hola, este bot funciona en los siguientes horarios (hora de Cuba):\n\n"
        "• 8:00 AM - 12:00 PM\n"
        "• 2:00 PM - 6:00 PM\n"
        "• 8:00 PM - 1:00 AM"
    )
    await update.message.reply_text(horarios)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    texto_original = update.message.text.strip()
    estado = context.user_data.get('estado', 'esperando_clave')

    if estado == 'esperando_clave':
        if texto_original in CLAVES_VALIDAS:
            context.user_data.clear()
            context.user_data.update({
                'estado': 'modulo_activo',
                'modulo_activo': True,
                'modulo_actual': 'regalo1'
            })
            context.bot_data['ADMIN_ID'] = ADMIN_ID
            
            import regalo1
            await regalo1.iniciar_flujo(update, context)
        else:
            await update.message.reply_text("❌ Clave incorrecta")
    else:
        if 'modulo_actual' in context.user_data:
            import regalo1
            await regalo1.manejar_flujo(update, context)

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot en ejecución...")
    app.run_polling()
