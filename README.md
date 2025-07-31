# PO3 Strategy - Power of 3 Forex Trading System

This repository contains a full implementation of the Power of 3 (PO3) trading concept, automated for both:

- ✅ Historical backtesting (Python + MetaTrader 5)
- ✅ Live trading (MetaTrader 5 Expert Advisor in MQL5)

---

## 🧠 Strategy Overview

Core Idea (Power of 3 Strategy)
Asian Session (Accumulation)

Price moves sideways in a range (low volatility).

London Session (Manipulation / Liquidity Grab)

Price takes out liquidity (fakeout above or below Asian range).

New York Session (Distribution / True Move)

Price reverses and shows the real direction of the day.

The Power of 3 (PO3) is based on:

1. **Accumulation (Asian session)**
2. **Manipulation (London session)**
3. **Distribution (New York session)**

The EA detects fakeouts during London and takes directional trades in NY session.

🧠 Strategy Rules (Derived from Charts)
For SELL Setup (as shown in your example):
Asian range is formed.

During London, price sweeps the high of the Asian range (enters a key level).

Wait for a rejection or confirmation candle (e.g., bearish engulfing) after the sweep.

Enter SHORT trade.

Target is a measured move down, likely at or beyond Asian low.

For BUY Setup (opposite logic):
Price sweeps Asian low in London session.

New York gives true move upward.

---

## 📁 Files

### `/backtester/PO3_Backtester.py`

Python script that:

- Pulls historical M15 EURUSD data
- Detects PO3 pattern
- Logs trade entries, exits, and accuracy

📌 Requirements:

```bash
pip install MetaTrader5 pandas pytz
```

/expert_advisor/PO3_EA.mq5
MetaTrader 5 Expert Advisor that:

Detects PO3 setup in live market

Trades based on session-based manipulation

Can be compiled and deployed via MetaEditor

🚀 How to Use

1. Backtest with Python
   cd backtester
   python PO3_Backtester.py

2. Use EA in MT5
   Copy PO3_EA.mq5 into:
   MQL5/Experts/PO3/

Author
Built by [Marcellus Ifeanyi] — based on the Power of 3 forex trading concept.

---

### 📜 `LICENSE` (Optional — MIT)

```text
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy...
```
