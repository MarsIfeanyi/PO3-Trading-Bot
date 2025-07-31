import MetaTrader5 as mt5
import pandas as pd
import datetime as dt
import pytz

# === CONFIG ===
symbol = "EURUSD"
lot = 0.1
sl_pips = 20
tp_pips = 50
timezone = pytz.timezone("Etc/UTC")  # Adjust if needed

# === INIT MT5 ===
if not mt5.initialize():
    print("MT5 init failed")
    quit()

# === FETCH HISTORICAL DATA ===
def fetch_data(days=5):
    end = dt.datetime.now(tz=timezone)
    start = end - dt.timedelta(days=days)
    data = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, start, end)
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

# === PO3 LOGIC ===
def detect_po3(df):
    results = []
    grouped = df.groupby(df.index.date)

    for date, day_data in grouped:
        try:
            asian = day_data.between_time("00:00", "06:00")
            london = day_data.between_time("07:00", "10:00")
            newyork = day_data.between_time("12:00", "16:00")

            asian_high = asian['high'].max()
            asian_low = asian['low'].min()
            london_high = london['high'].max()
            london_low = london['low'].min()

            ny_open_price = newyork.iloc[0]['open']
            ny_close_price = newyork.iloc[-1]['close']

            if london_high > asian_high and ny_close_price < ny_open_price:
                results.append({
                    "date": date,
                    "type": "SELL",
                    "entry": london_high,
                    "exit": ny_close_price,
                    "result": "TP" if london_high - ny_close_price >= tp_pips * 0.0001 else "SL"
                })

            elif london_low < asian_low and ny_close_price > ny_open_price:
                results.append({
                    "date": date,
                    "type": "BUY",
                    "entry": london_low,
                    "exit": ny_close_price,
                    "result": "TP" if ny_close_price - london_low >= tp_pips * 0.0001 else "SL"
                })
        except:
            continue

    return pd.DataFrame(results)

# === RUN BACKTEST ===
df = fetch_data(10)  # Last 10 days
results = detect_po3(df)
print(results)
print("Accuracy:", (results['result'] == "TP").mean())
