import os
from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# URL del API de Minecraft
minecraft_api_url = "https://api.mcstatus.io/v2/status/java/34.176.13.246"

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/status")
def get_text():
    server_status = get_server_status()
    return server_status





def get_server_status():
    response = requests.get(minecraft_api_url)
    if response.status_code == 200:
        data = response.json()
        online_status = data.get("online", False)
        if online_status:
            return "El servidor de Minecraft está en línea. 🎮"
        else:
            return "El servidor de Minecraft no está disponible. 🚫"
    else:
        return "No se pudo verificar el estado del servidor de Minecraft. ❓"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    message = response.message()

    if "@bot" in incoming_msg:
        server_status = get_server_status()
        message.body(server_status)
    else:
        message.body("Mencióna al bot con '@bot' para saber el estado del servidor.")
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
