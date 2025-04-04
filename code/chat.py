import sys
import json
import time
import websocket
from collections import deque
from sty import fg, bg, ef, rs

# Global variables to store cumulative volumes and costs
vol_sell_init = 0
vol_buy_init = 0
cost_sell_init = 0
cost_buy_init = 0

# Deques to store (timestamp, volume) tuples for different time windows
volumes_buy = {
    '1m': deque(),
    '5m': deque(),
    '15m': deque(),
    '1h': deque()
}

volumes_sell = {
    '1m': deque(),
    '5m': deque(),
    '15m': deque(),
    '1h': deque()
}

def ws_open(ws):
    ws.send('{"event":"subscribe","pair":["XBT/USD"], "subscription": {"name":"trade"}}')

def clean_old_entries(volumes_dict, timeframe):
    """Removes entries older than the specified timeframe."""
    current_time = time.time()
    if timeframe == '1m':
        threshold = 60
    elif timeframe == '5m':
        threshold = 300
    elif timeframe == '15m':
        threshold = 900
    elif timeframe == '1h':
        threshold = 3600
    
    while volumes_dict[timeframe] and (current_time - volumes_dict[timeframe][0][0]) > threshold:
        volumes_dict[timeframe].popleft()

def sum_volumes(volumes_dict, timeframe):
    """Sums up the volumes within the specified timeframe."""
    return sum(volume for _, volume in volumes_dict[timeframe])

def update_volumes(volumes_dict, vol, current_time):
    """Updates the volume dictionary for all timeframes."""
    for timeframe in volumes_dict.keys():
        volumes_dict[timeframe].append((current_time, vol))
        clean_old_entries(volumes_dict, timeframe)

def ws_message(ws, message):
    global vol_sell_init, vol_buy_init, cost_buy_init, cost_sell_init
    api_data = json.loads(message)
    
    if len(api_data) == 4:
        dat = api_data
        for x in range(len(dat[1])):
            current_time = time.time()
            human_readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
            
            if dat[1][x][3] == "b":
                vol_buy = float(dat[1][x][1])
                price_buy = float(dat[1][x][0])
                cost_buy = vol_buy * price_buy
                vol_buy_init += vol_buy
                cost_buy_init += cost_buy
                update_volumes(volumes_buy, vol_buy, current_time)

                buy_message = (
                    f"{human_readable_time} - " + 
                    bg.da_green + 
                    f'BTC buy cost: {round(cost_buy, 3)}$ volume: {vol_buy} at {round(price_buy, 3)}$' + 
                    bg.rs
                )
                print(buy_message)
                
            else:
                vol_sell = float(dat[1][x][1])
                price_sell = float(dat[1][x][0])
                cost_sell = vol_sell * price_sell
                vol_sell_init += vol_sell
                cost_sell_init += cost_sell
                update_volumes(volumes_sell, vol_sell, current_time)

                sell_message = (
                    f"{human_readable_time} - " + 
                    bg.da_red + 
                    f'BTC sell cost: {round(cost_sell, 3)}$ volume: {vol_sell} at {round(price_sell, 3)}$' + 
                    bg.rs
                )
                print(sell_message)

            # Calculate the Buy/Sell ratio as a percentage
            if vol_buy_init + vol_sell_init > 0:
                buy_sell_ratio = (vol_buy_init / (vol_buy_init + vol_sell_init)) * 100
            else:
                buy_sell_ratio = 0  # Avoid division by zero

        print(f"Buy/Sell Ratio Volume: {round(buy_sell_ratio, 3)}%")
        print(f"Total buys in $: {round(cost_buy_init, 3)} - Total sells in $: {round(cost_sell_init, 3)}")

        # Sum volumes for the latest minute, 5 minutes, 15 minutes, and hour
        for timeframe in ['1m', '5m', '15m', '1h']:
            total_vol_buy = sum_volumes(volumes_buy, timeframe)
            total_vol_sell = sum_volumes(volumes_sell, timeframe)
            print(f"Total Buy Volume in last {timeframe}: {total_vol_buy}")
            print(f"Total Sell Volume in last {timeframe}: {total_vol_sell}")

ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()