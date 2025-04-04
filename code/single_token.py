import sys
import json
import signal
import time
import pandas as pd
import websocket
import numpy as np
from sty import fg, bg, ef, rs
from datetime import datetime


vol_sell_init = 0
vol_buy_init = 0
cost_sell_init = 0
cost_buy_init = 0


buy_volumes=[]
sell_volumes=[]
buy_costs=[]
sell_costs=[]

last_prices=[]

def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["BTC/USD"], "subscription": {"name":"trade"}}')

def ws_message(ws, message):
    global vol_sell_init, vol_buy_init, cost_buy_init, cost_sell_init, buy_volumes, sell_volumes,buy_costs,sell_costs
    api_data = json.loads(message)
    
    if len(api_data)==4:
        dat = api_data
        for x in range(len(dat[1])):
            pair=dat[3]
            if(dat[1][x][3]=="b"):
                vol_buy = dat[1][x][1]
                time_buy=datetime.fromtimestamp(float(dat[1][x][2])).strftime("%Y-%m-%d %H:%M:%S")
                price_buy = dat[1][x][0]
                cost_buy = float(vol_buy) * float(price_buy)
                vol_buy_init = float(vol_buy_init)+float(vol_buy)
                cost_buy_init = float(cost_buy_init)+float(cost_buy)
                buy_message = bg.da_green +str(time_buy)+" | "+ pair+' | BUY cost: '+str(round(cost_buy,3))+'$ | '+'volume: '+str(vol_buy)+' | @'+str(round(float(price_buy), 3))+'$'+ bg.rs
                print(buy_message)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                buy_volumes.append(float(vol_buy))
                sell_volumes.append(0)
                buy_costs.append(cost_buy)
                sell_costs.append(0)
                last_prices.append(float(price_buy))
                
            else:
                vol_sell = dat[1][x][1]
                time_sell=datetime.fromtimestamp(float(dat[1][x][2])).strftime("%Y-%m-%d %H:%M:%S")
                price_sell = dat[1][x][0]
                cost_sell = float(vol_sell) * float(price_sell)
                cost_sell_init = float(cost_sell_init)+float(cost_sell)
                vol_sell_init = float(vol_sell_init)+float(vol_sell)
                sell_message = bg.da_red + str(time_sell)+" | "+pair+' | SELL cost: '+str(round(cost_sell,3))+'$ | '+'volume: '+str(vol_sell)+' | @'+str(round(float(price_sell),3))+'$'+ bg.rs
                print(sell_message)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                buy_volumes.append(0)
                sell_volumes.append(float(vol_sell))
                buy_costs.append(0)
                sell_costs.append(cost_sell)
                last_prices.append(float(price_sell))
                
        last_50=100*sum(buy_volumes[-50:])/(sum(buy_volumes[-50:])+sum(sell_volumes[-50:]))
        last_50_b=sum(buy_costs[-50:])
        last_50_s=sum(sell_costs[-50:])
        print(fg.li_blue + 'Last 50 Buy/Sell Ratio Volume ' +str(round(last_50, 2))+'%' + ' | Buys: '+ str(round(last_50_b, 2))+'$'+' | Sells: '+ str(round(last_50_s, 2))+'$'+ fg.rs)

        last_100=100*sum(buy_volumes[-100:])/(sum(buy_volumes[-100:])+sum(sell_volumes[-100:]))
        last_100_b=sum(buy_costs[-100:])
        last_100_s=sum(sell_costs[-100:])
        print(fg.li_blue + 'Last 100 Buy/Sell Ratio Volume ' +str(round(last_100, 2))+'%' + ' | Buys: '+ str(round(last_100_b, 2))+'$'+' | Sells: '+ str(round(last_100_s, 2))+'$'+ fg.rs)
        last_200=100*sum(buy_volumes[-200:])/(sum(buy_volumes[-200:])+sum(sell_volumes[-200:]))
        last_200_b=sum(buy_costs[-200:])
        last_200_s=sum(sell_costs[-200:])
        print(fg.li_blue + 'Last 200 Buy/Sell Ratio Volume ' +str(round(last_200, 2))+'%' + ' | Buys: '+ str(round(last_200_b, 2))+'$'+' | Sells: '+ str(round(last_200_s, 2))+'$'+ fg.rs)
        last_500=100*sum(buy_volumes[-500:])/(sum(buy_volumes[-500:])+sum(sell_volumes[-500:]))
        last_500_b=sum(buy_costs[-500:])
        last_500_s=sum(sell_costs[-500:])
        print(fg.li_blue + 'Last 500 Buy/Sell Ratio Volume ' +str(round(last_500, 2))+'%' + ' | Buys: '+ str(round(last_500_b, 2))+'$'+' | Sells: '+ str(round(last_500_s, 2))+'$'+ fg.rs)
        last_1000=100*sum(buy_volumes[-1000:])/(sum(buy_volumes[-1000:])+sum(sell_volumes[-1000:]))
        last_1000_b=sum(buy_costs[-1000:])
        last_1000_s=sum(sell_costs[-1000:])
        print(fg.li_blue + 'Last 1000 Buy/Sell Ratio Volume ' +str(round(last_1000, 2))+'%' + ' | Buys: '+ str(round(last_1000_b, 2))+'$'+' | Sells: '+ str(round(last_1000_s, 2))+'$'+ fg.rs)
        #df=pd.DataFrame({'types':types, 'volumes':volumes})
        last_50_prices=last_prices[-50:]
        last_50_prices_change=round(((last_50_prices[-1] - last_50_prices[0])/last_50_prices[0])*100, 1)
        print(f"Price change, last 50 {last_50_prices_change}")

        last_100_prices=last_prices[-100:]
        last_100_prices_change=round(((last_100_prices[-1] - last_100_prices[0])/last_100_prices[0])*100, 1)
        print(f"Price change, last 100 {last_100_prices_change}")

        last_200_prices=last_prices[-200:]
        last_200_prices_change=round(((last_200_prices[-1] - last_200_prices[0])/last_200_prices[0])*100, 1)
        print(f"Price change, last 200 {last_200_prices_change}")

        last_500_prices=last_prices[-500:]
        last_500_prices_change=round(((last_500_prices[-1] - last_500_prices[0])/last_500_prices[0])*100, 1)
        print(f"Price change, last 500 {last_500_prices_change}")

        last_1000_prices=last_prices[-1000:]
        last_1000_prices_change=round(((last_1000_prices[-1] - last_1000_prices[0])/last_1000_prices[0])*100, 1)
        print(f"Price change, last 1000 {last_1000_prices_change}")

        last_session_prices=last_prices
        last_session_prices_change=round(((last_session_prices[-1] - last_session_prices[0])/last_session_prices[0])*100, 1)
        print(f"Price change, session {last_session_prices_change}")
        print(fg.blue + "Session start Buy/Sell Ratio Volume " + str(round(percent*100,3)) +"%" + " | Total buys "+ str(round(cost_buy_init,3)) +"$"+ " | Total sells "+ str(round(cost_sell_init, 3))+"$"+ fg.rs)   
ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()


#import pandas as pd
#types=["s", "b", "b", "b", "b", "s", "s", "s", "b", "s"]
#vol=[2, 4, 1, 3, 2, 6, 7, 2, 6, 65]
#df=pd.DataFrame({'types':types, 'vol':vol})
#print(df.tail(3))
