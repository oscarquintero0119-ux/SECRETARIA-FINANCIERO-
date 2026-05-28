import requests
import time
import yfinance as yf

TOKEN = "8887694669:AAFWg18ymxo3CV7yl7EWMSC6hK16RegxTug"
CHAT_ID = "7290895497"

BTC_QTY = 0.00291896
SOL_QTY = 0.99062948
USDC_QTY = 80.07315188

BTC_INV = 800000
SOL_INV = 300000
USDC_INV = 300000

PFBCOLOM_QTY = 11
PFBCOLOM_INV = 706200

ECOPETROL_QTY = 110
ECOPETROL_INV = 300000

USD_COP = 4000


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


def precio_yahoo(ticker):
    data = yf.Ticker(ticker).history(period="1d")

    return float(data["Close"].iloc[-1])


def linea(nombre, invertido, actual):

    ganancia = actual - invertido

    rentabilidad = (ganancia / invertido) * 100

    return f"""
{nombre}
Invertido: ${invertido:,.0f} COP
Valor actual: ${actual:,.0f} COP
Ganancia/Pérdida: ${ganancia:,.0f} COP
Rentabilidad: {rentabilidad:.2f}%
"""


def reporte_portafolio():

    btc_price = precio_binance("BTCUSDT")
    sol_price = precio_binance("SOLUSDT")

    btc_actual = BTC_QTY * btc_price * USD_COP
    sol_actual = SOL_QTY * sol_price * USD_COP
    usdc_actual = USDC_QTY * USD_COP

    try:
        pfb_price = precio_yahoo("PFBCOLOM.CL")
    except:
        pfb_price = PFBCOLOM_INV / PFBCOLOM_QTY

    try:
        eco_price = precio_yahoo("ECOPETROL.CL")
    except:
        eco_price = ECOPETROL_INV / ECOPETROL_QTY

    pfb_actual = PFBCOLOM_QTY * pfb_price
    eco_actual = ECOPETROL_QTY * eco_price

    total_invertido = (
        BTC_INV +
        SOL_INV +
        USDC_INV +
        PFBCOLOM_INV +
        ECOPETROL_INV
    )

    total_actual = (
        btc_actual +
        sol_actual +
        usdc_actual +
        pfb_actual +
        eco_actual
    )

    ganancia_total = total_actual - total_invertido

    rentabilidad_total = (
        ganancia_total / total_invertido
    ) * 100

    mensaje = f"""
🤖 SECRETARIA FINANCIERA

📊 REPORTE REAL DEL PORTAFOLIO

🟠 BTC precio: {btc_price:,.2f} USDT
🟢 SOL precio: {sol_price:,.2f} USDT

🏦 PFBCOLOM precio: ${pfb_price:,.0f} COP
🛢️ ECOPETROL precio: ${eco_price:,.0f} COP

{linea("🟠 BTC", BTC_INV, btc_actual)}

{linea("🟢 SOL", SOL_INV, sol_actual)}

{linea("💵 USDC", USDC_INV, usdc_actual)}

{linea("🏦 PFBCOLOM", PFBCOLOM_INV, pfb_actual)}

{linea("🛢️ ECOPETROL", ECOPETROL_INV, eco_actual)}

💰 TOTAL INVERTIDO:
${total_invertido:,.0f} COP

📈 VALOR ACTUAL:
${total_actual:,.0f} COP

📌 GANANCIA/PÉRDIDA:
${ganancia_total:,.0f} COP

📊 RENTABILIDAD TOTAL:
{rentabilidad_total:.2f}%
"""

    return mensaje


ultimo_update = 0

enviar("🤖 Secretaria financiera actualizada.")


while True:

    try:

        url = (
            "https://api.telegram.org/bot"
            + TOKEN
            + "/getUpdates?offset="
            + str(ultimo_update + 1)
        )

        datos = requests.get(url).json()

        for item in datos["result"]:

            ultimo_update = item["update_id"]

            if (
                "message" in item and
                "text" in item["message"]
            ):

                texto = (
                    item["message"]["text"]
                    .upper()
                    .strip()
                )

                if texto == "BTC":

                    enviar(
                        f"🟠 BTC actual: "
                        f"{precio_binance('BTCUSDT'):,.2f} USDT"
                    )

                elif texto == "SOL":

                    enviar(
                        f"🟢 SOL actual: "
                        f"{precio_binance('SOLUSDT'):,.2f} USDT"
                    )

                elif (
                    texto == "PORTAFOLIO" or
                    texto == "REPORTE"
                ):

                    enviar(
                        reporte_portafolio()
                    )

                else:

                    enviar(
                        "Escribe BTC, SOL, REPORTE o PORTAFOLIO"
                    )

    except Exception as e:

        print("Error:", e)

    time.sleep(3)
