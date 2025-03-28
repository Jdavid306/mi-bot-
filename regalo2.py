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
        "Has escuchado sobre los lenguajes del amor?\n\nLos 5 lenguajes del amor son formas en que las personas expresan y perciben el amor.\n1) Palabras de afirmación (elogios o mensajes cariñosos),\n2) Tiempo de calidad (compartir momentos con atención plena),\n3) Recibir regalos (detalles simbólicos que demuestran pensamiento),\n4) Actos de servicio (hacer cosas útiles por el otro)\n5) Contacto físico (abrazos, besos, etc.).\nLa idea es que cada persona tiene uno o dos lenguajes principales que la hacen sentirse amada.",
        "La mente humana es un misterio...\nLa forma en la perisivimos las cosas no es igual a la de los demas, y en eso se vasan los comflicos en las personas.\nIntento saber quien eres, comprenderte, mientras tanto, he aqui mi lenjugaje.",
        "Lista para ganarte el proximo regalo ?! pongamos a prueba tu mente."
    ]
    
    for msg in mensajes:
        await update.message.reply_text(msg)
    
    context.user_data.update({
        'estado': 'confirmacion_inicial',
        'piezas': 0
    })

async def manejar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notificar_admin(update, context)
    texto_original = update.message.text.strip()
    texto = normalizar_texto(texto_original)
    estado = context.user_data.get('estado', 'confirmacion_inicial')
    piezas = context.user_data.get('piezas', 0)

    if estado == 'confirmacion_inicial':
        await update.message.reply_text(
            """acertijo 1 logica{ Completa esta secuencia: 16, 06, 68, 88, X, 98.

¿Qué número va en el lugar de la X?
}"""
        )
        context.user_data['estado'] = 'primer_acertijo'

    elif estado == 'primer_acertijo':
        if texto == "78":
            context.user_data['piezas'] = 1
            await update.message.reply_text("🧩 - Pieza desbloqueada (1/4)")
            await update.message.reply_text("\"eeehh bien, bien \". Vamos al proximo, una pista de tu regalo.")
            await update.message.reply_text(
                """Otro aceertijo{
Del frio protejo y tambien del sol. A veces soy regalo de gran ilusión, Soy diseño para
de tu ocasión. En letras voy, S, M, X, L. De manera general que soy?"""
            )
            context.user_data['estado'] = 'segundo_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'segundo_acertijo':
        if 'ropa' in texto:
            context.user_data['piezas'] = 2
            await update.message.reply_text("🧩 - Pieza desbloqueada (2/4)")
            await update.message.reply_text("Correcto!")
            await update.message.reply_text(
                """La primera aguja de coser tiene unos 40,000 años y fue hecha de hueso por los neandertales.
Los romanos consideraban la púrpura (extraída de un caracol marino) como el color más valioso: teñir una toga costaba el salario anual de un trabajador.
El tejido más antiguo descubierto es de hace 34,000 años, hecho de fibras de lino en Georgia (Europa).
El botón se inventó en el 2500 a.C. (Valle del Indo), pero hasta el siglo XIII no se usó para cerrar ropa.

Los jeans fueron creados en 1873 por Levi Strauss y Jacob Davis, usando remaches de cobre para reforzar los bolsillos de los mineros.

El sujetador moderno lo patentó Mary Phelps Jacob en 1914, usando dos pañuelos y una cinta.

El color blanco en bodas lo popularizó la reina Victoria en 1840, pero en países como China o India, el rojo es el color tradicional.
La minifalda fue creada en los 60 por Mary Quant, quien dijo: \"Quería que las mujeres pudieran correr tras un autobús sin tropezar\".

En 2017, se subastó el vestido de Marilyn Monroe de \"Los caballeros las prefieren rubias\" por $4.8 millones.
Los bolsillos pequeños de los vaqueros, que ahora solemos utilizar para guardar alguna moneda,  se crearon originariamente para guardar los relojes de bolsillo.
La corbata nació en Croacia en el siglo XVII: los soldados usaban pañuelos en el cuello, y los franceses la llamaron \"cravate\" (de \"croata\")."""
            )
            await update.message.reply_text("Te imaginas que es?  (Pulsa cualquier tecla para continuar, ajaja)")
            await update.message.reply_text(
                """acertijo{ Puedo estar en tu ropa, estoy casi seguro que ahora me llevas. Me ves y solo si ves, en las nubes del atardeceres, en las flores, en los mas raros animales. La niña sakura me dibuja, me dibuja en una ave de largas patas cominendo en la orilla de un lago. Quien soy?"""
            )
            context.user_data['estado'] = 'tercer_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'tercer_acertijo':
        if 'rosado' in texto:
            context.user_data['piezas'] = 3
            await update.message.reply_text("🧩 - Pieza desbloqueada (3/4)")
            await update.message.reply_text("Sabias que?\n\nEl planeta rosa: En 2013, la NASA descubrió GJ 504b, un exoplaneta gigante con tonos rosados debido a su calor.\nDiamantes rosados: Los más raros y caros del mundo (como el Graff Pink), se forman por deformaciones en su estructura atómica.\nEl término \"rosa\" proviene de la flor del mismo nombre, del latín rosa.\nEn el siglo XIX, el rosa se asociaba a los niños varones (por ser un \"rojo suave\", color de la fuerza), y el azul a las niñas (por su conexión con la Virgen María). La inversión ocurrió en los años 1940-50, impulsada por el marketing.\n\nAmaneceres y atardeceres: El cielo se torna rosa por la dispersión de Rayleigh, que filtra los tonos azules y deja pasar los rojizos.")
            await update.message.reply_text(
                """¿Qué es la dispersión de Rayleigh?

Es un fenómeno en el que las moléculas de la atmósfera (como el nitrógeno y el oxígeno) y pequeñas partículas dispersan la luz solar.

Depende de la longitud de onda:

Los colores con longitudes de onda cortas (azul, violeta) se dispersan más fácilmente que los de longitudes largas (rojo, naranja).

Por eso, durante el día, el cielo se ve azul: la luz azul se dispersa en todas direcciones y llega a nuestros ojos desde cualquier punto del cielo.

¿Por qué el cielo se vuelve rosa/rojo en el amanecer o atardecer?

Cuando el Sol está cerca del horizonte (al salir o ponerse), su luz debe atravesar más atmósfera que cuando está alto en el cielo. Esto tiene dos efectos clave:

La luz azul se dispersa y se \"pierde\":

Al recorrer una mayor distancia atmosférica, la luz azul (de onda corta) se dispersa tanto que no llega directamente a nuestros ojos.

Solo los colores de longitudes de onda largas (rojo, naranja) logran atravesar la atmósfera sin dispersarse demasiado.

Mezcla de colores y partículas:

Si hay partículas adicionales en el aire (contaminación, polvo, cenizas volcánicas o gotas de agua), estas refractan y dispersan la luz de manera diferente.

Esto puede crear tonos rosados al mezclar el rojo dominante con restos de azul disperso."""
            )
            await update.message.reply_text(
                """acertijo{Completa el siguiente texto:
El señor es __ ______, y nada me faltara."""
            )
            context.user_data['estado'] = 'cuarto_acertijo'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'cuarto_acertijo':
        if 'mipastor' in texto:
            context.user_data['piezas'] = 4
            await update.message.reply_text("🧩 - Pieza desbloqueada (4/4)")
            await update.message.reply_text("✅️ Regalo desbloqueado 🎁")
            await update.message.reply_text(
                """Regalo desbloqueado (Pulover rosa)

Que pensabas que todos tendrian un polover con un versiculo biblico y tu no?
a todos los que concidero familia y amigos tenemos uno, y tu eres parte de ello. 
Esta muy lindo, espero que te guste."""
            )
            context.user_data['tarea_finalizada'] = True
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")
