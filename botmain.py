from flask import Flask, request, jsonify
import telegram
import os

app = Flask(__name__)

# Configura el token de tu bot de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")  # <-- Usa una variable de entorno en Render
bot = telegram.Bot(token=TOKEN)

# Ruta para UptimeRobot (ping cada 5 min)
@app.route('/ping')
def ping():
    return jsonify({"status": "active", "message": "¡Bot en línea!"}), 200

# Webhook para Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(), bot)
        
        # Procesa los mensajes recibidos
        chat_id = update.message.chat.id
        text = update.message.text
        
        # Responde con un eco
        bot.send_message(chat_id=chat_id, text=f"Recibí: {text}")
        
        return jsonify({"status": "success"}), 200

# Configura el webhook al iniciar
def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook"  # <-- Usa tu URL de Render
    bot.set_webhook(url=webhook_url)

if __name__ == '__main__':
    set_webhook()  # Configura el webhook al inicio
    app.run(host='0.0.0.0', port=10000)  # Puerto obligatorio en Render
