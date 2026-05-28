import requests
import time

TOKEN = "8887694669:AAFWg18ymxo3CV7yl7EWMSC6hK16RegxTug"
CHAT_ID = "7290895497"

def enviar(mensaje):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    requests.post(url, data=payload)

def precio_binance(simbolo):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=" + simbolo
    respuesta = requests.get(url)
    datos = respuesta.json()
    precio = datos["price"]
    return float(precio)

def responder(texto):
    texto = texto.upper().strip()
    enviar("Recibí exactamente esto: " + texto)

    if texto == "BTC":
        btc = precio_binance("BTCUSDT")
        enviar("🟠 BTC actual: " + str(round(btc, 2)) + " USDT")

    elif texto == "SOL":
        sol = precio_binance("SOLUSDT")
        enviar("🟢 SOL actual: " + str(round(sol, 2)) + " USDT")

    elif texto == "REPORTE" or texto == "PORTAFOLIO":
        btc = precio_binance("BTCUSDT")
        sol = precio_binance("SOLUSDT")

        mensaje = (
            "📊 REPORTE DEL MERCADO\n\n"
            "🟠 BTC: " + str(round(btc, 2)) + " USDT\n"
            "🟢 SOL: " + str(round(sol, 2)) + " USDT\n\n"
            "🤖 Secretaria financiera activa."
        )

        enviar(mensaje)

    else:
        enviar("Escribe BTC, SOL, REPORTE o PORTAFOLIO")

ultimo_update = 0

enviar("🤖 Secretaria financiera reiniciada correctamente.")

while True:
    try:
        url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates?offset=" + str(ultimo_update + 1)
        respuesta = requests.get(url)
        datos = respuesta.json()

        for item in datos["result"]:
            ultimo_update = item["update_id"]

            if "message" in item and "text" in item["message"]:
                texto = item["message"]["text"]
                responder(texto)

    except Exception as error:
        print("ERROR:", error)

    time.sleep(3)
