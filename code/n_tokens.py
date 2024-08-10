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

#sel_pairs=["XBT/USD", "ADA/USD", "SOL/USD", "ETH/USD", "XRP/USD", "DOGE/USD", "PEPE/USD", "TIA/USD","TIA/USD", "NEAR/USD", "LINK/USD", "ZEC/USD", "ARB/USD", "LTC/USD", "BONK/USD", "DYM/USD", "SCRT/USD", "DOT/USD", "RARI/USD", "ACA/USD", "INJ/USD", "ETC/USD", "OGN/USD", "INTR/USD", "NYM/USD", "NODL/USD", "ROOK/USD", "FXS/USD", "SPELL/USD", "SUI/USD", "EUL/USD", "SUPER/USD", "GST/USD", "BICO/USD", "DASH/USD", "ACH/USD", "FLR/USD"]
#part1='{"event":"subscribe","pair":'
#part2= ',"subscription": {"name":"trade"}}'
#send=part1+str(sel_pairs)+part2
#print("'"+send+"'")
def ws_open(ws):
    #ws.send('{"event":"subscribe","pair":["XBT/USD", "ADA/USD", "SOL/USD", "ETH/USD", "XRP/USD", "DOGE/USD", "PEPE/USD", "TIA/USD","TIA/USD", "NEAR/USD", "LINK/USD", "ZEC/USD", "ARB/USD", "LTC/USD", "BONK/USD", "DYM/USD", "SCRT/USD", "DOT/USD", "RARI/USD", "ACA/USD", "INJ/USD", "ETC/USD", "OGN/USD", "INTR/USD", "NYM/USD", "NODL/USD", "ROOK/USD", "FXS/USD", "SPELL/USD", "SUI/USD", "EUL/USD", "SUPER/USD", "GST/USD", "BICO/USD", "DASH/USD", "ACH/USD" , "FLR/USD"], "subscription": {"name":"trade"}}')
    ws.send('{"event":"subscribe","pair":["1INCH/USD", "AAVE/USD", "ACA/USD", "ACH/USD", "ADA/USD", "ADX/USD", "AEVO/USD", "AGLD/USD", "AIR/USD", "AKT/USD", "ALCX/USD", "ALGO/USD", "ALICE/USD", "ALPHA/USD", "ALT/USD", "ANKR/USD", "ANT/USD", "APE/USD", "API3/USD", "APT/USD", "ARB/USD", "ARKM/USD", "ARPA/USD", "ASTR/USD", "ATLAS/USD", "ATOM/USD", "AUDIO/USD", "AVAX/USD", "AXS/USD", "BADGER/USD", "BAL/USD", "BAND/USD", "BAT/USD", "BCH/USD", "BEAM/USD", "BICO/USD", "BIGTIME/USD", "BIT/USD", "BLUR/USD", "BLZ/USD", "BNC/USD", "BNT/USD", "BOBA/USD", "BODEN/USD", "BOND/USD", "BONK/USD", "BRICK/USD", "BSX/USD", "BTT/USD", "C98/USD", "CELR/USD", "CFG/USD", "CHR/USD", "CHZ/USD", "CLOUD/USD", "COMP/USD", "COTI/USD", "CQT/USD", "CRV/USD", "CSM/USD", "CTSI/USD", "CVC/USD", "CVX/USD", "CXT/USD", "DASH/USD", "DENT/USD", "DOT/USD", "DRIFT/USD", "DYDX/USD", "DYM/USD", "EGLD/USD", "ENA/USD", "ENJ/USD", "ENS/USD", "EOS/USD", "ETHFI/USD", "ETHPY/USD", "ETHW/USD", "EUL/USD", "EWT/USD", "FARM/USD", "FET/USD", "FIDA/USD", "FIL/USD", "FIS/USD", "FLOKI/USD", "FLOW/USD", "FLR/USD", "FORTH/USD", "FTM/USD", "FXS/USD", "GALA/USD", "GAL/USD", "GARI/USD", "GHST/USD", "GLMR/USD", "GMT/USD", "GMX/USD", "GNO/USD", "GRT/USD", "GST/USD", "GTC/USD", "HDX/USD", "HFT/USD", "HNT/USD", "HONEY/USD", "ICP/USD", "ICX/USD", "IDEX/USD", "IMX/USD", "INJ/USD", "INTR/USD", "JASMY/USD", "JTO/USD", "JUNO/USD", "JUP/USD", "KAR/USD", "KAVA/USD", "KEEP/USD", "KEY/USD", "KILT/USD", "KINT/USD", "KIN/USD", "KNC/USD", "KP3R/USD", "KSM/USD", "KUJI/USD", "L3/USD", "LCX/USD", "LDO/USD", "LINK/USD", "LMWR/USD", "LPT/USD", "LRC/USD", "LSK/USD", "LUNA2/USD", "LUNA/USD", "MANA/USD", "MASK/USD", "MATIC/USD", "MC/USD", "MINA/USD", "MIR/USD", "MKR/USD", "MNGO/USD", "MNT/USD", "MOON/USD", "MOVR/USD", "MPL/USD", "MULTI/USD", "MV/USD", "MXC/USD", "NANO/USD", "NEAR/USD", "NMR/USD", "NODL/USD", "NOS/USD", "NTRN/USD", "NYM/USD", "OCEAN/USD", "OGN/USD", "OMG/USD", "ONDO/USD", "OP/USD", "ORCA/USD", "OSMO/USD", "OXT/USD", "OXY/USD",  "PDA/USD", "PENDLE/USD", "PEPE/USD", "PERP/USD", "PHA/USD", "POLIS/USD", "POLS/USD", "POL/USD", "POND/USD", "PORTAL/USD", "POWR/USD", "PSTAKE/USD", "PYTH/USD", "QNT/USD", "QTUM/USD", "RAD/USD", "RARE/USD", "RARI/USD", "RAY/USD", "RBC/USD", "RENDER/USD", "REN/USD", "REPV2/USD", "REQ/USD", "REZ/USD", "RLC/USD", "ROOK/USD", "RPL/USD", "RUNE/USD", "SAFE/USD", "SAGA/USD", "SAMO/USD", "SAND/USD", "SBR/USD", "SCRT/USD", "SC/USD", "SDN/USD", "SEI/USD", "SGB/USD", "SHIB/USD", "SNX/USD", "SOL/USD", "SPELL/USD", "SRM/USD", "STEP/USD", "STG/USD", "STORJ/USD", "STRD/USD", "STRK/USD", "STX/USD", "SUI/USD", "SUPER/USD", "SUSHI/USD", "SYN/USD", "TAO/USD",  "TEER/USD", "TIA/USD", "TLM/USD", "TNSR/USD", "TOKE/USD", "TRAC/USD", "TREMP/USD", "TRU/USD", "TRX/USD", "T/USD", "TVK/USD", "UMA/USD", "UNFI/USD", "UNI/USD",  "WAXL/USD", "WBTC/USD", "WEN/USD", "WIF/USD", "WOO/USD", "W/USD", "XCN/USD", "DOGE/USD", "ETC/USD", "ETH/USD", "LTC/USD", "MLN/USD", "REP/USD", "XRT/USD", "XTZ/USD", "XBT/USD", "XLM/USD", "XMR/USD", "XRP/USD", "ZEC/USD", "YFI/USD", "YGG/USD", "ZETA/USD" , "ZEUS/USD", "ZRO/USD", "ZRX/USD"], "subscription": {"name":"trade"}}')
def ws_message(ws, message):
    global vol_sell_init, vol_buy_init, cost_buy_init, cost_sell_init
    api_data = json.loads(message)
    if len(api_data)==4:
        dat = api_data
        #print(dat)
        for x in range(len(dat[1])):
            pair=dat[3]
            if(dat[1][x][3]=="b"):
                vol_buy = dat[1][x][1]
                price_buy = dat[1][x][0]
                cost_buy = float(vol_buy) * float(price_buy)
                vol_buy_init = float(vol_buy_init)+float(vol_buy)
                cost_buy_init = float(cost_buy_init)+float(cost_buy)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                #buy_message = bg.da_green +str(pair) +' buy cost: '+str(round(cost_buy,5))+'$ '+'volume: '+str(vol_buy)+' at '+str(round(float(price_buy), 5))+'$'+" Volume buy sell ratio: "+str(round(percent*100, 2)) + bg.rs
                buy_message = bg.da_green +str(pair) +' buy cost: '+str(round(cost_buy,5))+'$ '+'volume: '+str(vol_buy)+' at '+str(round(float(price_buy), 5))+'$' + bg.rs
                print(buy_message)
                

            else:
                vol_sell = dat[1][x][1]
                price_sell = dat[1][x][0]
                cost_sell = float(vol_sell) * float(price_sell)
                cost_sell_init = float(cost_sell_init)+float(cost_sell)
                vol_sell_init = float(vol_sell_init)+float(vol_sell)
                percent=float(vol_buy_init)/(float(vol_buy_init)+float(vol_sell_init))
                #sell_message = bg.da_red + str(pair)+' sell cost: '+str(round(cost_sell,5))+'$ '+'volume: '+str(vol_sell)+' at '+str(round(float(price_sell),5))+'$'+" Volume buy sell ratio: "+str(round(percent*100, 2))+ bg.rs
                sell_message = bg.da_red + str(pair)+' sell cost: '+str(round(cost_sell,5))+'$ '+'volume: '+str(vol_sell)+' at '+str(round(float(price_sell),5))+'$'+ bg.rs
                print(sell_message)
                
        #print("Buy/Sell Ratio Volume " + str(round(percent*100,1)) +"%" )    
        #print("Total buys in $ "+ str(round(cost_buy_init,1)) + " - Total sells in $ "+ str(round(cost_sell_init, 1)) )
ws = websocket.WebSocketApp('wss://ws.kraken.com/', on_open=ws_open, on_message=ws_message)
ws.run_forever()
