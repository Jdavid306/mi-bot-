from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import unicodedata
import os  # Nueva línea añadida para manejar variables de entorno
 
TOKEN = os.environ.get("TELEGRAM_TOKEN", "")  # Modificado para usar variable de entorno
USUARIOS_PERMITIDOS = {5616748906, 5729631156}

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.replace(" ", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    await update.message.reply_text("¡Hola!  ¿Quieres un regalo?  🎁  ¡Ingresa una clave!")
    context.user_data.clear()
    context.user_data['estado'] = 'esperando_clave'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return

    texto_original = update.message.text.strip()
    texto = normalizar_texto(texto_original)
    estado = context.user_data.get('estado', 'esperando_clave')

    if estado == 'esperando_clave':
        if texto_original == "P278v":
            await update.message.reply_text("✅ Clave correcta!")
            
            await update.message.reply_text("Uno de los mayores retos que se puede tener sobre tí es mantener tu mente activa y ocupada... 😊")
            
            await update.message.reply_text("Quiero por sobre todas las cosas ser tu mejor amigo, y este es un intento de lograrlo. 😇")
            
            await update.message.reply_text("Con este Bot intentaré mantener tu mente un poco ocupada, que aprendas cosas (espero que sean mejor que los nombres de los dictadores) y motivarte.")
            
            await update.message.reply_text(
                """Soy de los que piensan que en la vida son las pequeñas cosas las que valen, las cosas simples. Espero que este gran regalo conformado por muchos pequeños te guste. (E) (G). 😎 🤙

Te quiere

        - Jorge"""
            )
            
            await update.message.reply_text("Lista para el primer regalo?")
            context.user_data['estado'] = 'confirmacion_inicial'
        else:
            await update.message.reply_text("❌ Clave incorrecta")

    elif estado == 'confirmacion_inicial':
       
        await update.message.reply_text(
            """                ⚙️Acertijo 1

Soy un lenguaje sin palabras, soy un alma que habla sin voz. Los ciegos saben de mí porque nací del silencio. No tengo forma pero lleno el aire. No tengo reglas pero sí patrones. ¿Qué o Quién soy?!"""
        )
        context.user_data['estado'] = 'primer_acertijo'

    elif estado == 'primer_acertijo':
        if 'musica' in texto:
            await update.message.reply_text("✅ Respuesta correcta!")
            await update.message.reply_text("🧩 - Pieza desbloqueada (1/3)")
            await update.message.reply_text(
                """                  🎈  Datos curiosos 🎈

• Al escuchar música, tu corazón modifica sus latidos para intentar imitar el ritmo de la música que escuchas.

• ¿Sabés eso de tener todo el día una canción sonando en nuestra cabeza y no poder pararla? Este fenómeno se conoce como 'gusano musical'.

• La música escuchada se guarda en áreas del cerebro diferentes a las de los recuerdos, por eso las personas con Alzheimer son capaces de recordar melodías de su pasado.

• Cuando escuchamos música se libera dopamina en nuestro cerebro, como cuando tomas drogas, practicas sexo o comes.

• Las flores pueden crecer más rápido si hay música a su alrededor.

• El tipo de música que nos gusta a la edad de 20 años suele ser el tipo de música que nos gustará el resto de nuestra vida.

• La forma en la que concebimos el mundo se ve condicionada por el tipo de música que escuchamos.

¿Por qué el oído absoluto es común en compositores pero raro en matemáticos?

¿ Sabes lo qué es el oído absoluto ?
Investiga del tema. Y me cuentas.

Si un cantante plagia inconscientemente una melodía, ¿es culpable?

Al final tanto los escritores como los músicos no hacen nada 100% auténtico """
            )
            await update.message.reply_text("¿Estás lista para la desbloqueadar la siguiente pieza? 🤓")
            context.user_data['estado'] = 'transicion_2'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'transicion_2':
        await update.message.reply_text(
            """          🎯  Pregunta de conocimiento 

 ¿Cuál es el instrumento más antiguo de la historia? """
           
        )
        context.user_data['estado'] = 'segundo_acertijo'

    elif estado == 'segundo_acertijo':
        if 'flauta' in texto:
            await update.message.reply_text("✅ Respuesta correcta!")
            await update.message.reply_text("🧩 - Pieza desbloquear (2/3)")
            
            await update.message.reply_text("""Frase:\nLa música puede cambiar el mundo porque puede cambiar a las personas.\n– Bono""")
            
            await update.message.reply_text("""🧠 Otros datos curiosos: 

--El instrumento más antiguo del mundo--

Un hueso de buitre perforado, hallado en Alemania, es considerado la flauta más antigua (40,000 años). Los neandertales ya hacían música.

--La palabra música viene de las musas--

Del griego mousikē (arte de las musas), diosas que inspiraban la creatividad. Curiosamente, en la mitología griega, no había una musa específica para la música.

--El instrumento que se toca sin tocarlo--

El theremin, inventado en 1920, se maneja moviendo las manos cerca de sus antenas. Fue clave en películas de ciencia ficción de los 50.

--La nota que no existe--

En la escala cromática occidental, no hay una nota llamada Si sostenido, porque equivale a Do natural. ¡Es un intervalo enarmónico!

--El piano se llamaba originalmente pianoforte--

Porque podía tocar piano (suave) y forte (fuerte), algo revolucionario en el siglo XVIII.

--El cerebro humano prefiere la música imperfecta--

Estudios muestran que pequeños errores en una interpretación (un slide en guitarra) la hacen sentir más emocional y auténtica.""")
            
            await update.message.reply_text("¡Vas muy bien! ¿Lista para el último reto? ")
            context.user_data['estado'] = 'transicion_3'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'transicion_3':
        await update.message.reply_text(
            """      ⚙️ Acertijo 3:

Si fuera animal sería una zebra. Si fuera matemática seria 8oct = 5+7. Tengo sol y no luna. Tengo arte de ser arte y dicha de ser....¿Qué o Quién soy? """
        )
        context.user_data['estado'] = 'tercer_acertijo'

    elif estado == 'tercer_acertijo':
        if 'piano' in texto:
            await update.message.reply_text("✅ Respuesta correcta!")
            await update.message.reply_text("🧩 - Pieza desbloqueada (3/3)")
            await update.message.reply_text("✅️ Regalo desbloqueado 🎁")
            await update.message.reply_text(
                """                🎊 Préstamo del piano 🎹

Pues sí, pude convencer a mi padre de prestarte el piano 😇. Espero que le des un buen uso, sé que lo vas a cuidar. Te será tan útil como tu perseverancia sea capaz de llegar. La música es parte de nosotros, se puede llegar muy lejos con ella.

Me propuse hacer todo lo posible para sumarte...Quiero escucharte y verte, en cosas tan productivas y divertidas como sea posible.

No sé si cuenta como regalo, espero que lo sientas así el tiempo que este contigo"""
            )
            context.user_data.clear()
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

if __name__ == "__main__":  # Corregido (error tipográfico original)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot en ejecución...")
    app.run_polling()
