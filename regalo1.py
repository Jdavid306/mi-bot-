from telegram import Update
from telegram.ext import ContextTypes
import unicodedata

async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        mensaje = update.message.text
        reporte = (
            f"📩 Mensaje de < {user.full_name} >\n\n"
            f"📝 {mensaje}"
        )
        await context.bot.send_message(chat_id=context.bot_data['ADMIN_ID'], text=reporte)
    except Exception as e:
        print(f"Error en notificación: {e}")

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.replace(" ", "")

async def iniciar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notificar_admin(update, context)
    
    mensajes = [
        "✅ Clave correcta!",
        # ... (mantener igual el resto de mensajes)
    ]
    
    for msg in mensajes:
        await update.message.reply_text(msg)
    
    context.user_data['estado'] = 'confirmacion_inicial'

async def manejar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notificar_admin(update, context)
    texto_original = update.message.text.strip()
    texto = normalizar_texto(texto_original)
    estado = context.user_data.get('estado', 'confirmacion_inicial')

    # ... (mantener igual toda la lógica existente)

    elif estado == 'tercer_acertijo':
        if 'piano' in texto:
            # ... (mensajes existentes)
            
            # Reinicio completo del estado
            context.user_data.clear()
            await update.message.reply_text(
                "🔁 Sistema reiniciado: Ahora recibirás notificaciones normales de nuevo"
            )
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")
