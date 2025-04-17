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
        """❤️   Los 5 lenguajes del amor   ✨
        
1) Palabras de afirmación (elogios o mensajes cariñosos)
2) Tiempo de calidad (compartir momentos con atención plena)
3) Recibir regalos (detalles simbólicos que demuestran pensamiento)
4) Actos de servicio (hacer cosas útiles por el otro)
5) Contacto físico (abrazos, besos, etc.)
La idea es que cada persona tiene uno o dos lenguajes principales que la hacen sentirse amada.""",
        """🧠   La mente humana es un misterio...  
        
La forma en que percibimos las cosas no es igual a la de los demás.
Intento saber quién eres, comprenderte... """,
"Te pregunto cuál es el tuyo ? Mientras tanto, he aquí mi lenguaje.",
             
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

    if estado == 'confirmacion_inicial':
        await update.message.reply_text(
            """⚙️ Acertijo 1 - Lógica 🔢
Completa esta secuencia: 16, 06, 68, 88, X, 98.
¿Qué número va en el lugar de la X?"""
        )
        context.user_data['estado'] = 'primer_acertijo'

    elif estado == 'primer_acertijo':
        if texto == "78":
            await update.message.reply_text("🧩 Pieza desbloqueada (1/4)")
            await update.message.reply_text("\"¡Eeehh bien, bien!\" Vamos al próximo, tambien pista de tu regalo.")
            await update.message.reply_text(
                """⚙️ Acertijo 2 - Pista

Del frio protejo y tambien del sol. A veces soy regalo de gran ilusión y diseño para tu ocasión. En letras voy, S, ?, L, !. De manera general que soy?"""
            )
            context.user_data['estado'] = 'segundo_acertijo'
        else:
            await update.message.reply_text("🔄 Respuesta incorrecta. Intenta nuevamente ")

    elif estado == 'segundo_acertijo':
        if 'ropa' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (2/4)")
            await update.message.reply_text("Siuu. Ropa e inteligencia dos cosas que te sobran")
            await update.message.reply_text("Proporcionalmente atractivas; No crees? intentare aumentar ambas") 
            await update.message.reply_text(
                """📜 -Datos históricos-

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
            await update.message.reply_text("Pulsa cualquier tecla para continuar, jeje ")
            context.user_data['estado'] = 'transicion_2'
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Intenta nuevamente")

    elif estado == 'transicion_2':
        await update.message.reply_text(
            """          ⚙️ Acertijo 2

Puedo estar en tu ropa, estoy casi seguro que ahora me llevas. Me ves y solo si ves, en las nubes del atardeceres, en la flor de sakura o en un flamenco. Quien soy?"""
        )
        context.user_data['estado'] = 'tercer_acertijo'  

    elif estado == 'tercer_acertijo':  
        if 'rosa' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (3/4)")
            await update.message.reply_text("\"¡Correcto !!\" Espero que no estes haciendo trampas.")
            await update.message.reply_text(
                """🔍 ¿Sabías que? 🌌

-El planeta rosa: En 2013, la NASA descubrió GJ 504b, un exoplaneta gigante con tonos rosados debido a su calor.
-Diamantes rosados: Los más raros y caros del mundo (como el Graff Pink), se forman por deformaciones en su estructura atómica.
-El término "rosa" proviene de la flor del mismo nombre, del latín rosa.
-En el siglo XIX, el rosa se asociaba a los niños varones (por ser un "rojo suave", color de la fuerza), y el azul a las niñas (por su conexión con la Virgen María). La inversión ocurrió en los años 1940-50, impulsada por el marketing.""",
            )
            await update.message.reply_text(
                """ 🌅 Amaneceres y atardeceres: El cielo se torna rosa por la dispersión de Rayleigh, que filtra los tonos azules y deja pasar los rojizos. 🌄


¿Qué es la dispersión de Rayleigh?

Es un fenómeno en el que las moléculas de la atmósfera (como el nitrógeno y el oxígeno) y pequeñas partículas dispersan la luz solar.

    Depende de la longitud de onda:

        Los colores con longitudes de onda cortas (azul, violeta) se dispersan más fácilmente que los de longitudes largas (rojo, naranja).

        Por eso, durante el día, el cielo se ve azul: la luz azul se dispersa en todas direcciones y llega a nuestros ojos desde cualquier punto del cielo.

¿Por qué el cielo se vuelve rosa/rojo en el amanecer o atardecer?

Cuando el Sol está cerca del horizonte (al salir o ponerse), su luz debe atravesar más atmósfera que cuando está alto en el cielo. Esto tiene dos efectos clave:

    La luz azul se dispersa y se "pierde":

        Al recorrer una mayor distancia atmosférica, la luz azul (de onda corta) se dispersa tanto que no llega directamente a nuestros ojos.

        Solo los colores de longitudes de onda largas (rojo, naranja) logran atravesar la atmósfera sin dispersarse demasiado.

    Mezcla de colores y partículas:

        Si hay partículas adicionales en el aire (contaminación, polvo, cenizas volcánicas o gotas de agua), estas refractan y dispersan la luz de manera diferente.

        Esto puede crear tonos rosados al mezclar el rojo dominante con restos de azul disperso."""
            )
            await update.message.reply_text(""" 🦩 Los flamencos son rosados debido a su dieta, específicamente por los carotenoides, pigmentos naturales presentes en los alimentos que consumen. Aquí está la explicación detallada:

      Fuente de los pigmentos:
    Los flamencos se alimentan principalmente de organismos acuáticos como artemias (camarones de salmuera), algas azul-verdosas y pequeños crustáceos. Estos organismos contienen carotenoides, como la astaxantina, un pigmento rojizo-anaranjado.

      Metabolismo de los carotenoides:
    Los carotenoides son procesados por el hígado del flamenco, donde se descomponen en pigmentos (como la cantaxantina). Estos pigmentos se depositan en las plumas, la piel y el pico, otorgando el color rosado característico. Sin esta dieta, los flamencos serían blancos o grises.

    Desarrollo del color:

        Las crías de flamenco nacen grises o blancas y adquieren su tono rosado gradualmente al comenzar a consumir alimentos ricos en carotenoides.

        La intensidad del color varía según la especie y la disponibilidad de estos pigmentos en su hábitat. Por ejemplo, los flamencos del Caribe suelen ser más vibrantes que otras especies.

    Función biológica y social:

        El color rosado actúa como un indicador de salud: un tono más intenso sugiere una dieta nutritiva y un individuo más atractivo para la reproducción.

        En cautiverio, si su alimentación carece de carotenoides, se les suplementa con pigmentos para mantener su coloración. """)
            await update.message.reply_text("- 📖 Ahora un poco de biblia, veamos que tanto sabes ")
            await update.message.reply_text("Lista para un último desafio? 🔥")
            context.user_data['estado'] = 'espera_final'  # Nuevo estado para esperar respuesta
        else:
            await update.message.reply_text(" ❌ Respuesta incorrecta. Intenta nuevamente ")

    # Nuevo bloque para manejar la espera antes del último acertijo
    elif estado == 'espera_final':
        await update.message.reply_text(
            """-                ⚙️ Acertijo Final ✨              -

Completa el texto:
"El señor es __ ______, y nada me faltará\""""
        )
        context.user_data['estado'] = 'cuarto_acertijo'

    elif estado == 'cuarto_acertijo':
        if 'mipastor' in texto:
            await update.message.reply_text("🧩 Pieza desbloqueada (4/4)")
            await update.message.reply_text(
                """🎁 Regalo desbloqueado (Pulóver rosa) 🧥

¿Pensabas que todos tendrían un pulóver con un versículo bíblico y tú no?
A todos los que considero familia y amigos les di uno,
¡y tú eres parte de ello!

¡Está muy lindo, espero que te guste! """
            )
            context.user_data['tarea_finalizada'] = True
        else:
            await update.message.reply_text("❌ Respuesta incorrecta. Lee salmos cap 20 - 25")
