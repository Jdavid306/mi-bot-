from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
CLAVES_VALIDAS = {"Z2013b", "X1314e", "F240e", "H876x", "Y389w", "J791s", "L184e", "T678v"}
ADMIN_ID = 5616748906

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
    await update.message.reply_text("¡Hola!  ¿Quieres un regalo?  🎁  ¡Ingresa una clave! 3")
    context.user_data.clear()
    context.user_data['estado'] = 'esperando_clave'

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    horarios = (
        "Ey, hola, este bot funciona Manual (Funciona cuando le da la gana ):\n\n"
    )
    await update.message.reply_text(horarios)

async def pista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    await update.message.reply_text("🔍 La clave está debajo de tu cama, a veces sobre la cama, a veces escucha notas, a veces solo silencio 🛏️🎵🤫")
    await update.message.reply_text("📚 La clave está entre letras de un libro ✍️")
    await update.message.reply_text("💻 La clave mezclada entre códigos que escribiste tú ⌨️")
    await update.message.reply_text("🗂️ La clave está OCULTA en carpetas, Universidad 🎓 (sin .)")

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
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("pista", pista))  # Nuevo comando añadido
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot en ejecución...")
    app.run_polling()
