import sys
import json
import signal
import time
import pandas as pd
import websocket
import numpy as np
from sty import fg, bg, ef, rs
from datetime import datetime

df_buys=pd.DataFrame()
df_sells=pd.DataFrame()
levels_buy_out=pd.DataFrame()
levels_sell_out=pd.DataFrame()
def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"trade"}}')

def ws_message(ws, message):
    global df_buys, df_sells, levels_buy_out, levels_sell_out
    api_data = json.loads(message)
    
    if len(api_data)==4:
        dat = api_data
        for x in range(len(dat[1])):
            pair=dat[3]
            if(dat[1][x][3]=="b"):
                vol_buy = float(dat[1][x][1])
                time_buy=datetime.fromtimestamp(float(dat[1][x][2])).strftime("%Y-%m-%d %H:%M:%S")
                price_buy = float(dat[1][x][0])
                cost_buy = vol_buy * price_buy
                rounded_price_buy=round(float(price_buy), -2)
                d_temp = {'rounded_price': [rounded_price_buy], 'cost_buy': [cost_buy]}
                temp_buys=pd.DataFrame(data=d_temp)
                df_buys=df_buys._append(temp_buys,ignore_index=True)
                levels_buy=df_buys.groupby(['rounded_price']).sum().reset_index()
                levels_buy=levels_buy.round(1)
                levels_buy_out=levels_buy
                
            else:
                vol_sell = float(dat[1][x][1])
                time_sell=datetime.fromtimestamp(float(dat[1][x][2])).strftime("%Y-%m-%d %H:%M:%S")
                price_sell = float(dat[1][x][0])
                cost_sell = vol_sell * price_sell
                rounded_price_sell=round(float(price_sell), -2)
                d_temp = {'rounded_price': [rounded_price_sell], 'cost_sell': [cost_sell]}
                temp_sells=pd.DataFrame(data=d_temp)
                df_sells=df_sells._append(temp_sells,ignore_index=True)
                levels_sell=df_sells.groupby(['rounded_price']).sum().reset_index()
                levels_sell=levels_sell.round(1)
                levels_sell_out=levels_sell
                
        if len(levels_sell_out.index)>0 and len(levels_buy_out.index)>0:
            merged = pd.merge(levels_buy_out, levels_sell_out, how='outer', on='rounded_price').fillna(0)
            merged['total']=merged['cost_sell']+merged['cost_buy']
            merged['percent_buy']=round(merged['cost_buy'] / merged['total']*100,1)
            print(merged)
            merged.to_csv("merged.csv")
    
ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()
