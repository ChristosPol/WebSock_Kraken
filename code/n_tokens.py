import sys
import json
import signal
import time
import websocket
import numpy as np
from sty import fg, bg, ef, rs


vol_sell_init = 0
vol_buy_init = 0

def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD", "ADA/USD", "SOL/USD", "ETH/USD", "XRP/USD", "DOGE/USD"], "subscription": {"name":"trade"}}')

def ws_message(ws, message):
    global vol_sell_init, vol_buy_init
    api_data = json.loads(message)
    print(api_data)
    
ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()