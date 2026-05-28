import requests
import time

TOKEN = "8887694669:AAFWg18ymxo3CV7yl7EWMSC6hK16RegxTug"
CHAT_ID = "7290895497"

BTC_CANTIDAD = 0.00291896
SOL_CANTIDAD = 0.99062948
USDC_CANTIDAD = 80.07315188

BTC_INVERTIDO = 800000
SOL_INVERTIDO = 300000
USDC_INVERTIDO = 300000

PFBCOLOM_INVERTIDO = 706200
ECOPETROL_INVERTIDO = 300000

DOLAR_COP = 4000

def enviar(mensaje):
url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
datos = {
"chat_id": CHAT_ID,
"text": mensaje
}
requests.post(url, data=datos)

def precio_binance(simbolo):
url = "https://api.binance.com/api/v3/ticker/price?symbol=" + simbolo
respuesta = requests.get(url)
datos = respuesta.json()
return float(datos["price"])

def reporte_portafolio():
btc_precio = precio_binance("BTCUSDT")
sol_precio = precio_binance("SOLUSDT")

```
btc_actual = BTC_CANTIDAD * btc_precio * DOLAR_COP
sol_actual = SOL_CANTIDAD * sol_precio * DOLAR_COP
usdc_actual = USDC_CANTIDAD * DOLAR_COP

total_invertido = (
    BTC_INVERTIDO +
    SOL_INVERTIDO +
    USDC_INVERTIDO +
    PFBCOLOM_INVERTIDO +
    ECOPETROL_INVERTIDO
)

total_actual = (
    btc_actual +
    sol_actual +
    usdc_actual +
    PFBCOLOM_INVERTIDO +
    ECOPETROL_INVERTIDO
)

ganancia = total_actual - total_invertido
rentabilidad = (ganancia / total_invertido) * 100

mensaje = (
    "🤖 SECRETARIA FINANCIERA\n\n"
    "📊 REPORTE DEL PORTAFOLIO\n\n"
    "🟠 BTC\n"
    "Precio actual: " + str(round(btc_precio, 2)) + " USDT\n"
    "Valor actual aprox: $" + str(round(btc_actual)) + " COP\n\n"
    "🟢 SOL\n"
    "Precio actual: " + str(round(sol_precio, 2)) + " USDT\n"
    "Valor actual aprox: $" + str(round(sol_actual)) + " COP\n\n"
    "💵 USDC\n"
    "Valor actual aprox: $" + str(round(usdc_actual)) + " COP\n\n"
    "🏦 PFBCOLOM\n"
    "Invertido: $" + str(PFBCOLOM_INVERTIDO) + " COP\n\n"
    "🛢️ ECOPETROL\n"
    "Invertido: $" + str(ECOPETROL_INVERTIDO) + " COP\n\n"
    "💰 TOTAL INVERTIDO: $" + str(round(total_invertido)) + " COP\n"
    "📈 VALOR ACTUAL APROX: $" + str(round(total_actual)) + " COP\n"
    "📌 GANANCIA/PÉRDIDA: $" + str(round(ganancia)) + " COP\n"
    "📊 RENTABILIDAD: " + str(round(rentabilidad, 2)) + "%"
)

return mensaje
```

def responder(texto):
texto = texto.upper().strip()

```
if texto == "BTC":
    btc = precio_binance("BTCUSDT")
    enviar("🟠 BTC actual: " + str(round(btc, 2)) + " USDT")

elif texto == "SOL":
    sol = precio_binance("SOLUSDT")
    enviar("🟢 SOL actual: " + str(round(sol, 2)) + " USDT")

elif texto == "PORTAFOLIO" or texto == "REPORTE":
    enviar(reporte_portafolio())

else:
    enviar("Escribe BTC, SOL, REPORTE o PORTAFOLIO")
```

ultimo_update = 0

enviar("🤖 Secretaria financiera activada correctamente.")

while True:
try:
url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates?offset=" + str(ultimo_update + 1)
respuesta = requests.get(url)
datos = respuesta.json()

```
    for item in datos["result"]:
        ultimo_update = item["update_id"]

        if "message" in item and "text" in item["message"]:
            texto = item["message"]["text"]
            responder(texto)

except Exception as error:
    print("ERROR:", error)

time.sleep(3)
```
