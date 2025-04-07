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
        "Uno de los mayores retos que se puede tener sobre tí es mantener tu mente activa y ocupada... 😊",
        "Quiero por sobre todas las cosas ser tu mejor amigo, y este es un intento de lograrlo. 😇",
        "Con este Bot intentaré mantener tu mente un poco ocupada, que aprendas cosas (espero que sean mejor que los nombres de los dictadores) y motivarte.",
        """Soy de los que piensan que en la vida son las pequeñas cosas las que valen, las cosas simples. Espero que este gran regalo conformado por muchos pequeños te guste. (E) (G). 😎 🤙

Te quiere

        - Jorge""",
        "Lista para el primer regalo? 🎉"






    ]

    for msg in mensajes:
        await update.message.reply_text(msg)

    context.user_data['estado'] = 'confirmacion_inicial'

async def manejar_flujo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notificar_admin(update, context)
    texto_original = update.message.text.strip()
    texto = normalizar_texto(texto_original)
    estado = context.user_data.get('estado', 'confirmacion_inicial')

    if estado == 'confirmacion_inicial':
        await update.message.reply_text(
            """                ⚙️ Acertijo 1

Soy un lenguaje sin palabras, soy un alma que habla sin voz. Los ciegos saben de mí porque nací del silencio. No tengo forma pero lleno el aire. No tengo reglas pero sí patrones. ¿Qué o Quién soy?!"""
        )
        context.user_data['estado'] = 'primer_acertijo'

    elif estado == 'primer_acertijo':
        if 'musica' in texto:
            await update.message.reply_text("✅ Respuesta correcta! 🎶")
            await update.message.reply_text("🧩 - Pieza desbloqueada (1/3)")














            await update.message.reply_text(
                """                  🎈  Datos curiosos 🎈





* Al escuchar música, tu corazón modifica sus latidos para intentar imitar el ritmo de la música que escuchas.

* ¿Sabés eso de tener todo el día una canción sonando en nuestra cabeza y no poder pararla? Este fenómeno se conoce como 'gusano musical'. 🐛🎵

* La música escuchada se guarda en áreas del cerebro diferentes a las de los recuerdos, por eso las personas con Alzheimer son capaces de recordar melodías de su pasado.

* Cuando escuchamos música se libera dopamina en nuestro cerebro, como cuando tomas drogas, practicas sexo o comes. 🧠💥

* Las flores pueden crecer más rápido si hay música a su alrededor. 🌸🎧

* El tipo de música que nos gusta a la edad de 20 años suele ser el tipo de música que nos gustará el resto de nuestra vida.

* La forma en la que concebimos el mundo se ve condicionada por el tipo de música que escuchamos."""




            )
            await update.message.reply_text("¿Estás lista para desbloquear la siguiente pieza? 🤓")
            context.user_data['estado'] = 'transicion_2'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")

    elif estado == 'transicion_2':
        await update.message.reply_text(
            """          🎯  Pregunta de conocimiento 

 ¿Cuál es el instrumento más antiguo de la historia? 🎵"""
        )
        context.user_data['estado'] = 'segundo_acertijo'

    elif estado == 'segundo_acertijo':
        if 'flauta' in texto:
            await update.message.reply_text("✅ Respuesta correcta! 🎼")
            await update.message.reply_text("🧩 - Pieza desbloqueada (2/3)")
            await update.message.reply_text("""Frase:\nLa música puede cambiar el mundo porque puede cambiar a las personas.\n– Bono 🎸""")
            await update.message.reply_text("""🧠 Otros datos curiosos: 












-- El instrumento más antiguo del mundo --

Un hueso de buitre perforado, hallado en Alemania, es considerado la flauta más antigua (40,000 años). Los neandertales ya hacían música. 🦴🎶

-- La palabra música viene de las musas --

Del griego mousikē (arte de las musas), diosas que inspiraban la creatividad. Curiosamente, en la mitología griega, no había una musa específica para la música. 

-- El instrumento que se toca sin tocarlo --

El theremin, inventado en 1920, se maneja moviendo las manos cerca de sus antenas. Fue clave en películas de ciencia ficción de los 50. 👽🎹

-- La nota que no existe --

En la escala cromática occidental, no hay una nota llamada Si sostenido, porque equivale a Do natural. ¡Es un intervalo enarmónico! 🎼🚫

--El piano se llamaba originalmente pianoforte--

Porque podía tocar piano (suave) y forte (fuerte), algo revolucionario en el siglo XVIII. 🎹⚡

-- El cerebro humano prefiere la música imperfecta --

Estudios muestran que pequeños errores en una interpretación (un slide en guitarra) la hacen sentir más emocional y auténtica. 🧠🎸""")
            await update.message.reply_text("¡Vas muy bien! ¿Lista para el último reto? 🔥")
            context.user_data['estado'] = 'transicion_3'


        else:
            await update.message.reply_text("🔄 Respuesta incorrecta. Intenta nuevamente ")

    elif estado == 'transicion_3':

        await update.message.reply_text(
            """      ⚙️ Acertijo 3:

Si fuera animal sería una zebra. Si fuera matemática seria 8oct = 5+7. Tengo sol y no luna. Tengo arte de ser arte y dicha de ser....¿Qué o Quién soy? """

        )
        context.user_data['estado'] = 'tercer_acertijo'

    elif estado == 'tercer_acertijo':
        if 'piano' in texto:
            await update.message.reply_text("✅ Respuesta correcta! 🎹✨")
            await update.message.reply_text("🧩 - Pieza desbloqueada (3/3)")
            await update.message.reply_text("✅️ Regalo desbloqueado 🎁")
            await update.message.reply_text(
                """                🎊 Préstamo del piano 🎹

Pues sí, pude convencer a mi padre de prestarte el piano 😇. Espero que le des un buen uso, sé que lo vas a cuidar. Te será tan útil como tu perseverancia sea capaz de llegar. La música es parte de nosotros, se puede llegar muy lejos con ella.

Me propuse hacer todo lo posible para sumarte...Quiero escucharte y verte, en cosas tan productivas y divertidas como sea posible.



No sé si cuenta como regalo, espero que lo sientas así el tiempo que este contigo 🌟"""
            )
            context.user_data['tarea_finalizada'] = True
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente 🔄")
