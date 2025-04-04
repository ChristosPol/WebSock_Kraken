import json
import signal
import time
import pandas as pd
import websocket
import numpy as np
from sty import fg, bg, ef, rs
from datetime import datetime


#def ws_open(ws):
 #   ws.send('{"event":"subscribe","pair":["BTC/USD"], "subscription": {"name":"ticker"}}')

#def ws_message(ws, message):
 #   api_data = json.loads(message)
  #  if len(api_data)>2:
   #     print(api_data)

#ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
#ws.run_forever()

#wss://ws.kraken.com/v2

def ws_open(ws):
    ws.send('{"method":"subscribe","params":{"symbol":["ADA/USD"], "channel": "ticker"}}')

def ws_message(ws, message):
    api_data = json.loads(message)
    if len(api_data)>2:
        #print(api_data)
        print(api_data['data'])
        


ws = websocket.WebSocketApp('wss://ws.kraken.com/v2', on_open=ws_open, on_message=ws_message)
ws.run_forever()
