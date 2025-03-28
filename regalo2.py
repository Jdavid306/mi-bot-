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
        "✅ ¡Clave correcta!",
        """✨ *Los 5 lenguajes del amor* ✨
        
1) Palabras de afirmación (elogios o mensajes cariñosos),
2) Tiempo de calidad (compartir momentos con atención plena),
3) Recibir regalos (detalles simbólicos que demuestran pensamiento),
4) Actos de servicio (hacer cosas útiles por el otro),
5) Contacto físico (abrazos, besos, etc.).
La idea es que cada persona tiene uno o dos lenguajes principales que la hacen sentirse amada.""",
        """🧠 *La mente humana es un misterio...*
        
La forma en que percibimos las cosas no es igual a la de los demás, y en eso se basan los conflictos en las personas.
Intento saber quién eres, comprenderte... mientras tanto, he aquí mi lenguaje.""",
        "🔍 ¿Lista para ganarte el próximo regalo? ¡Pongamos a prueba tu mente!"
    ]
    
    for msg in mensajes:
        await update.message.reply_text(msg)
    
    context.user_data['estado'] = 'confirmacion_inicial'

async def manejar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notificar_admin(update, context)
    texto_original = update.message.text.strip()
    texto = normalizar_texto(texto_original)
    estado = context.user_data.get('estado', 'confirmacion_inicial')

    if context.user_data.get('tarea_finalizada'):
        await update.message.reply_text("🔧¡El bot está en reparación! Espera hasta mañana.\n\n😴 Jorge necesita tiempo para mejorarlo. ¡Gracias por tu paciencia! 🌙")
        return

    if estado == 'confirmacion_inicial':
        await update.message.reply_text(
            """⚙️ *Acertijo 1 - Lógica* 🔢
Completa esta secuencia: 16, 06, 68, 88, X, 98.
¿Qué número va en el lugar de la X?"""
        )
        context.user_data['estado'] = 'primer_acertijo'

    elif estado == 'primer_acertijo':
        if texto == "78":
            await update.message.reply_text("🧩 Pieza desbloqueada (1/4)")
            await update.message.reply_text("\"¡Eeehh bien, bien!\" Vamos al próximo, una pista de tu regalo.")
            await update.message.reply_text(
                """⚙️ *Acertijo 2 - Pista* 🧥
Del frío protejo y también del sol.
A veces soy regalo de gran ilusión,
soy diseño para tu ocasión.
En tallas voy: S, M, X, L.
¿Qué soy en general?"""
            )
            context.user_data['estado'] = 'segundo_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")

    elif estado == 'segundo_acertijo':
        if 'ropa' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (2/4)")
            await update.message.reply_text(
                """📜 *Datos históricos* 🕰️
1. La primera aguja de coser tiene unos 40,000 años y fue hecha de hueso por los neandertales.
2. Los romanos consideraban la púrpura (extraída de un caracol marino) como el color más valioso: teñir una toga costaba el salario anual de un trabajador.
3. El tejido más antiguo descubierto es de hace 34,000 años, hecho de fibras de lino en Georgia (Europa).
4. El botón se inventó en el 2500 a.C. (Valle del Indo), pero hasta el siglo XIII no se usó para cerrar ropa.
5. Los jeans fueron creados en 1873 por Levi Strauss y Jacob Davis, usando remaches de cobre para reforzar los bolsillos de los mineros.
6. El sujetador moderno lo patentó Mary Phelps Jacob en 1914, usando dos pañuelos y una cinta.
7. El color blanco en bodas lo popularizó la reina Victoria en 1840, pero en países como China o India, el rojo es el color tradicional.
8. La minifalda fue creada en los 60 por Mary Quant, quien dijo: "Quería que las mujeres pudieran correr tras un autobús sin tropezar".
9. En 2017, se subastó el vestido de Marilyn Monroe de "Los caballeros las prefieren rubias" por $4.8 millones.
10. Los bolsillos pequeños de los vaqueros se crearon originariamente para guardar los relojes de bolsillo.
11. La corbata nació en Croacia en el siglo XVII: los soldados usaban pañuelos en el cuello, y los franceses la llamaron "cravate" (de "croata")."""
            )
            await update.message.reply_text("(Pulsa cualquier tecla para continuar, ajaja)")
            context.user_data['estado'] = 'tercer_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")

    elif estado == 'tercer_acertijo':
        if 'rosado' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (3/4)")
            await update.message.reply_text(
                """🔍 *¿Sabías que?* 🌌
- El planeta rosa: En 2013, la NASA descubrió GJ 504b, un exoplaneta gigante con tonos rosados debido a su calor.
- Diamantes rosados: Los más raros y caros del mundo (como el Graff Pink), se forman por deformaciones en su estructura atómica.
- El término "rosa" proviene de la flor del mismo nombre, del latín rosa.
- En el siglo XIX, el rosa se asociaba a los niños varones, y el azul a las niñas. La inversión ocurrió en los años 1940-50.

🌈 *¿Qué es la dispersión de Rayleigh?*
Es un fenómeno en el que las moléculas de la atmósfera y pequeñas partículas dispersan la luz solar.

🌅 *¿Por qué el cielo se vuelve rosa/rojo?*
- El sol cerca del horizonte: la luz atraviesa más atmósfera
- La luz azul se dispersa y solo llega el rojo/naranja
- Partículas adicionales crean tonos rosados"""
            )
            await update.message.reply_text(
                """⚙️ *Acertijo Final* ✨
Completa el texto:
"El señor es __ ______, y nada me faltará\""""
            )
            context.user_data['estado'] = 'cuarto_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")

    elif estado == 'cuarto_acertijo':
        if 'mipastor' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (4/4)")
            await update.message.reply_text(
                """🎁 *Regalo desbloqueado (Pulóver rosa)* 🧥
¿Pensabas que todos tendrían un pulóver con un versículo bíblico y tú no?
A todos los que considero familia y amigos les dimos uno,
¡y tú eres parte de ello!

¡Está muy lindo, espero que te guste! ❤️"""
            )
            context.user_data['tarea_finalizada'] = True
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")
