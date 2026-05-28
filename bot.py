import requests
import time

TOKEN = "TU_NUEVO_TOKEN"
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
    data = requests.get(url).json()
    return float(data["price"])

ultimo_update = 0

enviar("🤖 Secretaria financiera activada 24/7.")

while True:
    url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates?offset=" + str(ultimo_update + 1)
    datos = requests.get(url).json()

    for item in datos["result"]:
        ultimo_update = item["update_id"]

        if "message" in item and "text" in item["message"]:
            texto = item["message"]["text"].upper().strip()

            if texto == "BTC":
                btc = precio_binance("BTCUSDT")
                enviar(f"🟠 BTC ACTUAL: {btc} USDT")

            elif texto == "SOL":
                sol = precio_binance("SOLUSDT")
                enviar(f"🟢 SOL ACTUAL: {sol} USDT")

            elif texto == "REPORTE":
                btc = precio_binance("BTCUSDT")
                sol = precio_binance("SOLUSDT")

                mensaje = f"""
📊 REPORTE MERCADO

🟠 BTC: {btc} USDT
🟢 SOL: {sol} USDT

🤖 Secretaria financiera activa.
"""
                enviar(mensaje)

            else:
                enviar("Escribe BTC, SOL o REPORTE")

    time.sleep(3)
