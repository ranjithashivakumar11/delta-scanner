import requests
import time

import requests
import time

# ============================
# DELTA SCANNER V3 - PART 1
# ============================

BOT_TOKEN = "8864363630:AAHznwSl9sx7yIYIhgsMK7aEY7Um7USOjDU"
CHAT_ID = "7803319325"

PRODUCTS_URL = "https://api.india.delta.exchange/v2/products"
TICKERS_URL = "https://api.india.delta.exchange/v2/tickers"
CANDLES_URL = "https://api.india.delta.exchange/v2/history/candles"

print("=" * 50)
print("DELTA SCANNER V3")
print("=" * 50)

print("Loading products...")

products = requests.get(PRODUCTS_URL).json()["result"]

perpetuals = []

for product in products:

    if product.get("contract_type") == "perpetual_futures":
        perpetuals.append(product)

print("Perpetual Futures :", len(perpetuals))

print("Loading live prices...")

tickers = requests.get(TICKERS_URL).json()["result"]

price_dict = {}

for ticker in tickers:

    symbol = ticker.get("symbol")
    price = ticker.get("close")

    if price is None:
        price = ticker.get("mark_price")

    if symbol is not None and price is not None:
        price_dict[symbol] = price

print("Live Prices :", len(price_dict))

end_time = int(time.time())
start_time = end_time - (3 * 24 * 60 * 60)

print("Scanner Ready")
print("-" * 50)
# ============================
# DELTA SCANNER V3 - PART 2
# ============================

def get_yesterday_candle(symbol):

    params = {
        "symbol": symbol,
        "resolution": "1d",
        "start": start_time,
        "end": end_time
    }

    try:

        response = requests.get(CANDLES_URL, params=params)

        if response.status_code != 200:
            return None

        candles = response.json()["result"]

        if len(candles) < 2:
            return None

        return candles[-2]

    except Exception:
        return None


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        requests.post(url, data=data, timeout=10)

    except Exception as e:

        print("Telegram Error :", e)
        # ============================
# DELTA SCANNER V3 - PART 3
# ============================

print("Starting Breakout Scanner...")
print("-" * 50)

buy_count = 0
sell_count = 0

for coin in perpetuals:

    symbol = coin.get("symbol")

    if symbol not in price_dict:
        continue

    candle = get_yesterday_candle(symbol)

    if candle is None:
        continue

    current_price = float(price_dict[symbol])
    yesterday_high = float(candle["high"])
    yesterday_low = float(candle["low"])

    if current_price > yesterday_high:

        buy_count += 1

        message = (
            f"🟢 BUY SIGNAL\n\n"
            f"Coin : {symbol}\n"
            f"Current Price : {current_price}\n"
            f"Yesterday High : {yesterday_high}"
        )

        print(message)
        print("-" * 50)

        send_telegram(message)

    elif current_price < yesterday_low:

        sell_count += 1

        message = (
            f"🔴 SELL SIGNAL\n\n"
            f"Coin : {symbol}\n"
            f"Current Price : {current_price}\n"
            f"Yesterday Low : {yesterday_low}"
        )

        print(message)
        print("-" * 50)

send_telegram(message)

print("=" * 50)
print("SCAN COMPLETED")
print("BUY Signals :", buy_count)
print("SELL Signals :", sell_count)
print("=" * 50)

while True:
    print("Waiting 5 minutes for next scan...")
    time.sleep(300)print("-" * 50)

send_telegram(message)

print("=" * 50)
print("SCAN COMPLETED")
print("BUY Signals :", buy_count)
print("SELL Signals :", sell_count)
print("=" * 50)

while True:
    print("Waiting 5 minutes for next scan...")
    time.sleep(300)
