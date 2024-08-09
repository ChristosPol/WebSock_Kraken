import sys
import json
import signal
import time
import websocket
import numpy as np
from sty import fg, bg, ef, rs


vol_sell_init = 0
vol_buy_init = 0
cost_sell_init = 0
cost_buy_init = 0


def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"trade"}}')

def ws_message(ws, message):
    global vol_sell_init, vol_buy_init, cost_buy_init, cost_sell_init
    api_data = json.loads(message)
    
    if len(api_data)==4:
        dat = api_data
        for x in range(len(dat[1])):
            if(dat[1][x][3]=="b"):
                vol_buy = dat[1][x][1]
                price_buy = dat[1][x][0]
                cost_buy = float(vol_buy) * float(price_buy)
                vol_buy_init = float(vol_buy_init)+float(vol_buy)
                cost_buy_init = float(cost_buy_init)+float(cost_buy)
                buy_message = bg.da_green + 'BTC buy cost: '+str(round(cost_buy,1))+'$ '+'volume: '+str(vol_buy)+' at '+str(round(float(price_buy), 1))+'$'+ bg.rs
                print(buy_message)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                
            else:
                vol_sell = dat[1][x][1]
                price_sell = dat[1][x][0]
                cost_sell = float(vol_sell) * float(price_sell)
                cost_sell_init = float(cost_sell_init)+float(cost_sell)
                vol_sell_init = float(vol_sell_init)+float(vol_sell)
                sell_message = bg.da_red + 'BTC sell cost: '+str(round(cost_sell,1))+'$ '+'volume: '+str(vol_sell)+' at '+str(round(float(price_sell),1))+'$'+ bg.rs
                print(sell_message)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                
        print("Buy/Sell Ratio Volume " + str(round(percent*100,1)) +"%" )    
        print("Total buys in $ "+ str(round(cost_buy_init,1)) + " - Total sells in $ "+ str(round(cost_sell_init, 1)) )    
ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()