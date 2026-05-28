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
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})


def precio_binance(simbolo):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=" + simbolo
    return float(requests.get(url).json()["price"])


def precio_yahoo(ticker):
    data = yf.Ticker(ticker).history(period="1d")
    return float(data["Close"].iloc[-1])


def linea(nombre, invertido, actual):
    ganancia = actual - invertido
    rent = (ganancia / invertido) * 100
    return f"""
{nombre}
Invertido: ${invertido:,.0f} COP
Actual: ${actual:,.0f} COP
Ganancia/Pérdida: ${ganancia:,.0f} COP
Rentabilidad: {rent:.2f}%
"""


def reporte_portafolio():
    btc_price = precio_binance("BTCUSDT")
    sol_price = precio_binance("SOLUSDT")

    btc_actual = BTC_QTY * btc_price * USD_COP
    sol_actual = SOL_QTY * sol_price * USD_COP
    usdc_actual = USDC_QTY * USD_COP

    pfb_price = precio_yahoo("PFBCOLOM.CL")
    eco_price = precio_yahoo("ECOPETROL.CL")

    pfb_actual = PFBCOLOM_QTY * pfb_price
    eco_actual = ECOPETROL_QTY * eco_price

    total_inv = BTC_INV + SOL_INV + USDC_INV + PFBCOLOM_INV + ECOPETROL_INV
    total_act = btc_actual + sol_actual + usdc_actual + pfb_actual + eco_actual
    ganancia_total = total_act - total_inv
    rent_total = (ganancia_total / total_inv) * 100

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

💰 TOTAL INVERTIDO: ${total_inv:,.0f} COP
📈 VALOR ACTUAL: ${total_act:,.0f} COP
📌 GANANCIA/PÉRDIDA TOTAL: ${ganancia_total:,.0f} COP
📊 RENTABILIDAD TOTAL: {rent_total:.2f}%
"""
    return mensaje


ultimo_update = 0
enviar("🤖 Secretaria financiera actualizada. Escribe BTC, SOL o PORTAFOLIO.")

while True:
    datos = requests.get(
        "https://api.telegram.org/bot" + TOKEN + "/getUpdates?offset=" + str(ultimo_update + 1)
    ).json()

    for item in datos["result"]:
        ultimo_update = item["update_id"]

        if "message" in item and "text" in item["message"]:
            texto = item["message"]["text"].upper().strip()

            if texto == "BTC":
                enviar(f"🟠 BTC actual: {precio_binance('BTCUSDT'):,.2f} USDT")

            elif texto == "SOL":
                enviar(f"🟢 SOL actual: {precio_binance('SOLUSDT'):,.2f} USDT")

            elif texto in ["PORTAFOLIO", "REPORTE"]:
                enviar(reporte_portafolio())

            else:
                enviar("Escribe: BTC, SOL o PORTAFOLIO")

    time.sleep(3)
