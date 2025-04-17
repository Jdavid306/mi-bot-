import unicodedata
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
USUARIOS_PERMITIDOS = {5616748906, 5729631156, 8134739443}
ADMIN_ID = 5616748906

VALID_KEYS = [
    'sueños', 'amor', 'libro', 'corazon', 'vida', 
    'deciciones', 'quiero', 'estraño', 'canciones', 
    'musica', 'cicatrices', 'abrazos', 'luna', 'colores', 'iris', 'lirio', 'nota', 'tiempo'
]

RIDDLES = [
    {
        'pregunta': "🔍 Existe un mes en el que todas las personas duermen menos. ¿Cuál es? ",
        'respuesta': "febrero",
        'mensajes': [
            "🎉 ¡Siuu! Jaja te hice el mismo un día con elefantes 🐘",
            "✅ 1/7 completado",
            "✨ ERES: - UN SUEÑO - ✨",
            "📝 (...) Un sueño del que me pregunto si quiero despertar...\nTe he dicho muchas cosas, pero hoy, en estas notas eres un sueño.\nEse que siempre quise, que siempre esperé...\nEse donde me despertaba diciendo '¡Estas cosas no pasan!'(...)"
        ]
    },
    {
        'pregunta': " Estoy en todo y en nada. ¿Quién soy? ",
        'respuesta': "D",
        'mensajes': [
            "🎯 ¡Correcto! Me encantan estos tipos de acertijos",
            "✅ 2/7 completado",
            "💫 ERES: - HERMOSA -",
            "🌌 (...) Tú tienes una fórmula que mi cabeza no puede entender...\nEres dos en una, doblemente hermosa por separado e indescriptible junta. (...)"   
        ]
    },
    {
        'pregunta': "🔢 Tenemos esta secuencia: 1, 1, 2, 3, 5, 3, 8, 1. ¿Qué número sigue?",
        'respuesta': "9",
        'mensajes': [
            "🤖 ¡Correcto! Es que has programado, imagínate",
            "✅ 3/7 completado",
            "🚀 ERES: - UN SER SUPERIOR -",
            "📊 (...) Quizás eso explica por qué nada te es suficiente...\nTiendes a dar el doble de lo que se te da, y en eso se basa mi teoría sobre el ser superior que eres. (...)"
        ]
    },
    {
        'pregunta': "🌑 Sin luz no existo, pero si me da la luz me muero. ¿Quién soy? ",
        'respuesta': "sombra",
        'mensajes': [
            "👻 ¡Correcto! Este era difícil",
            "✅ 4/7 completado",
            "🌪 ERES: - UN HURACÁN -",
            "🎨 (...) Tú eres huracan categoría 7 y fuera de temporada.(...)Eres así... Me encanta como lo destrozas todo, los límites, los pares, Mis notas ! y todo en general. Como te atreves a invadir mi mundo de blanco y negro con un tarro de pintura. Te veo por todo mi mundo pintado flores de rosado, blanco, naranja y azul, pegando carteles con tu firma. (...)"
        ]
    },
    {
        'pregunta': "🐱 Cuatro gatos en un cuarto,\ncada gato en un rincón,\ncada gato ve tres gatos,\n¿Adivina cuántos gatos son?\n(Respuesta en número) ",
        'respuesta': "4", 
        'mensajes': [
            "😼 ¡Correcto! Venga este ni vale",
            "✅ 5/7 completado",
            "🌠 ERES: - UNA ESTRELLA FUGAZ -",
            "💫 (...) A tí te veo, y por eso cada segundo te miraba como si fuera el último, justo como una estrella fugaz.(...)\n(...) Entonces me gana el deseo, se me olvida quien soy y lo que te estoy haciendo, cada segundo necesito aprovecharte como la estrella fugaz que eres.(...)"
        ]
    },
    {
        'pregunta': "🧮 ¿Qué 3 números dan el mismo resultado cuando se multiplican y se suman? (Respuesta de los números de menor a mayor seprados por espacio)",
        'respuesta': "1 2 3", 
        'mensajes': [
            "🧠 ¡Correcto! Oye, no sé cómo lo hiciste, a mí me costó",
            "✅ 6/7 completado",
            "🤝 ERES: - MI AMIGA -",
            "💖 (...) Nadie es más sexy y deseable que tú...\nVienes en combo como esa amiga que estará ahí y aunque no me entiendas como quisiera, lo haces más que nadie. (...)"
        ]
    },
    {
        'pregunta': "🚖 En el taxi en el que yo entré había 3 pasajeros. Poco después, 2 personas bajaron y 1 entró.\n¿Cuántas personas hay ahora?(Respuesta en número) ",
        'respuesta': "4",
        'mensajes': [
            "🎯 ¡Correcto! Había 5 personas: 3 pasajeros, 1 conductor y yo.\nLuego se bajaron 2 y subió 1 = 4",
            "✅ 7/7 completado",
            "💫 ERES: - PEQUEÑA -",
            """💌 (...) Te lo pido de favor, nunca dejes de ser quien eres, nunca dejes de ser la niña pequeña que puede soñar y conseguirlo. Los años jamás pasarán sobre tí, y siempre serás joven.(...) 
(...)  me encanta todos esos cachetes pelliscables, por tu increíble personalidad, y la manera que eres una niña pequeña dentro de un adulto responsable. Eres todo ternura y perversidad en un mismo frasco..(...) 
(...)  No es justo que cada vez te abrace puedas sentir mi corazón y yo no el tuyo... PD: es que eres pequeña y me das por el pecho (...) 
(...)  Un beso, tu pequeña 🤍 (...) 
(...)  No sabia lo pequeña que era su cuerpo, y lo bien que quedaba alado de mi pecho, y lo bien que se juntan las piernas. Su calidez era impresionante, y estaba tan perfectamente ahí, que es como si toda mi vida hubiera esperado ese momento..(...)"""
        ]
    }
]

FINAL_MESSAGES = [
    "🎁✨  ¡Regalo desbloqueado!  ✨🎉",
    "💭 Ni te imaginas lo que siento después de tener que leer tantas notas para hacer este bot...",
    "Supe que lo haría después de soñar estando acostado a tu lado en la arena de la playa.",
    "Llevo la mañana completa trabajando en él, desesperando para que me contestaras si venías o no (Hoy es miércoles 17).",
    "Son las 12:45 pm, y no sé qué me duele más: Que te hayas perdido el potaje o que te hayas enojado conmigo por decirte que hicieras vida hogar...",
    "Terminé este boceto, ahora solo me queda la tarde completa para programarlo...",
    "Mi única forma de dejar de pensar en ti y en lo que haces, es pensando en cosas para ti.",
    "Estos mensajes no iban aquí, pero quiero regalarte un poco de contexto jeje. Al final esto se trata de eso, de regalos.",
    "Por eso pienso profundamente que el amor es más que un sentimiento. Da igual lo que siento ahora, es la decisión de darte este regalo en forma de notas, en cosas que te seran útiles...",
    "🎉 El regalo es......",
    "📱 ¡UN REGALO SORPRESA!* Tu me haces sufrir y yo te lo devuelvo ",
    " Te llegará un mensaje pronto en tu móvil, entonces lo sabrás. Saludos.",
    """ Te quiero Mi...     
      
                  guapisexy  😇"""
]

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto.strip()

def contiene_clave_valida(texto):
    texto_normalizado = normalizar(texto)
    for clave in VALID_KEYS:
        if normalizar(clave) in texto_normalizado:
            return clave
    return None

async def notificar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        mensaje = update.message.text
        reporte = (
            f"📩 Mensaje de <{user.full_name}>\n\n"
            f"📝 Contenido: {mensaje}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=reporte)
    except Exception as e:
        print(f"🔴 Error en notificación: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USUARIOS_PERMITIDOS:
        return
    
    context.user_data.clear()
    mensajes = [
        "🚨 ¡El bot está en estado de emergencia!",
        "⏳ Durante las próximas 48h el modo especial estará activo",
        "🔑 No existen claves alfanuméricas, solo palabras...",
        "\n💞 Encuentra las palabras que nos unen, que compartimos",
        "🎁 Al final tendrás un regalo especial, solo si eres capaz de controlarlas 😉",
        "💡 ¿Estás lista para este desafío?! En cuanto des aceptar tendrás 48h para completarlo"
    ]
    
    for mensaje in mensajes:
        await update.message.reply_text(mensaje)
    
    context.user_data.update({
        'esperando_confirmacion': True,
        'progress': 0,
        'found_keys': []
    })

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        return
    
    await notificar_admin(update, context)
    
    user_data = context.user_data
    texto = update.message.text

    if user_data.get('esperando_confirmacion'):
        await update.message.reply_text("📜 Querías una lista de todo lo que te he dicho que eres...\n✨ Por cada acertijo completado tendrás una\n\n💡 PD: Todas son sacadas de las notas")
        await update.message.reply_text("🔎 Ingresa una palabra que nos une, que compartimos, lo que somos, lo que eres")
        user_data['esperando_confirmacion'] = False
        return

    if user_data.get('expecting_answer'):
        respuesta_normalizada = normalizar(RIDDLES[user_data['current_riddle']]['respuesta'])
        input_normalizado = normalizar(texto)
        
        if respuesta_normalizada in input_normalizado:
            user_data['progress'] += 1
            
            for msg in RIDDLES[user_data['current_riddle']]['mensajes']:
                await update.message.reply_text(msg)

            if user_data['progress'] == 7:
                for mensaje in FINAL_MESSAGES:
                    await update.message.reply_text(mensaje)
                context.user_data.clear()
            else:
                await update.message.reply_text(
                    f"💬 ¿Lista para el próximo? Ingresa una palabra clave 🔑"
                )
                user_data['expecting_answer'] = False
        else:
            await update.message.reply_text("❌ Incorrecto. Intenta de nuevo:")
        return

    clave_detectada = contiene_clave_valida(texto)
    if clave_detectada and clave_detectada not in user_data['found_keys']:
        user_data['found_keys'].append(clave_detectada)
        await update.message.reply_text("🎉 ¡Correcto! Has encontrado una clave ✅")
        await update.message.reply_text(RIDDLES[user_data['progress']]['pregunta'])
        user_data['current_riddle'] = user_data['progress']
        user_data['expecting_answer'] = True
    else:
        await update.message.reply_text("❌ Incorrecto o clave ya usada.🔍 Sigue buscando...")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot en ejecución...")
    application.run_polling()

if __name__ == "__main__":
    main()
