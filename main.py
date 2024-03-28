import threading

import websocket
import json
import requests

TG_TOKEN = "7063385723:AAGuWLD-LQEIHalBZSWR4_qofgxYU20rt9k"
TG_CHAT_ID = "781607769"


alerts = []

def send_message(text):
    res = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(TG_TOKEN),
                        data={'chat_id': TG_CHAT_ID, 'text': text})


def on_open(ws):
    sub_msg = {"method": "SUBSCRIBE", "params": ["btcusdt@miniTicker"], "id": 1}
    ws.send(json.dumps(sub_msg))
    print("Connected to Binance WebSocket")

def on_message(ws, message):
    data = json.loads(message)
    print("Received data:", data)
    if 's' in data and 'c' in data:
        if isinstance(data['s'], str):
            check_price_alert("BTCUSDT", 69630, data)
    else:
        print("Invalid data format:", data)

def check_price_alert(symbol, price, data):
    if data.get('s') == symbol:
        current_price = float(data.get('c', 0))
        if current_price <= price and symbol not in alerts:
            print(f"{symbol}: Current price {current_price}, lower than {price}. Sending alert.")
            send_message(f"{symbol}: Current price {current_price}, lower than {price}.")
            alerts.append(symbol)
        elif current_price >= price and symbol in alerts:
            print(f"{symbol}: Current price {current_price}, higher than {price}. Sending alert.")
            send_message(f"{symbol}: Current price {current_price}, higher than {price}.")
            alerts.remove(symbol)

def start_websocket():
    url = "wss://fstream.binance.com/ws"
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message)

    ws.run_forever()

def start_bot():
    threading.Thread(target=start_websocket).start()

if __name__ == "__main__":
    start_bot()