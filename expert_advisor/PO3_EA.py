import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time

# === Config ===
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M15
LOT = 0.1
MAGIC = 123456
SL_PIPS = 20
TP_PIPS = 50

# === Time Definitions ===
ASIAN_START = datetime.strptime("00:00", "%H:%M").time()
ASIAN_END = datetime.strptime("06:00", "%H:%M").time()
LONDON_START = datetime.strptime("07:00", "%H:%M").time()
LONDON_END = datetime.strptime("10:00", "%H:%M").time()

# === Initialize MT5 ===
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# === Fetch Historical Data ===
def get_data():
    rates = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, 500)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

# === Asian Range Detection ===
def get_asian_range(df):
    asian_data = df.between_time(ASIAN_START.strftime("%H:%M"), ASIAN_END.strftime("%H:%M"))
    high = asian_data['high'].max()
    low = asian_data['low'].min()
    return high, low

# === Entry Criteria ===
def check_po3_setup(df):
    asian_high, asian_low = get_asian_range(df)

    # Get London session data
    london_data = df.between_time(LONDON_START.strftime("%H:%M"), LONDON_END.strftime("%H:%M"))

    # Look for sweep above Asian high or below Asian low
    london_high = london_data['high'].max()
    london_low = london_data['low'].min()

    if london_high > asian_high:
        print("Bearish PO3 setup detected.")
        return 'SELL', asian_high, asian_low
    elif london_low < asian_low:
        print("Bullish PO3 setup detected.")
        return 'BUY', asian_high, asian_low
    else:
        return None, None, None

# === Place Order ===
def place_order(direction, sl, tp):
    price = mt5.symbol_info_tick(SYMBOL).ask if direction == 'BUY' else mt5.symbol_info_tick(SYMBOL).bid
    sl_price = price - SL_PIPS * 0.0001 if direction == 'BUY' else price + SL_PIPS * 0.0001
    tp_price = price + TP_PIPS * 0.0001 if direction == 'BUY' else price - TP_PIPS * 0.0001

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT,
        "type": mt5.ORDER_TYPE_BUY if direction == 'BUY' else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": MAGIC,
        "comment": "PO3 Strategy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order failed:", result.retcode)
    else:
        print("Trade placed successfully!")

# === Main Bot Loop ===
def run_bot():
    df = get_data()
    signal, high, low = check_po3_setup(df)
    
    if signal:
        place_order(signal, SL_PIPS, TP_PIPS)

# === Run Daily Check ===
run_bot()
