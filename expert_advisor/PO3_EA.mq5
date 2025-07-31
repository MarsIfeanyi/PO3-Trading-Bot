//+------------------------------------------------------------------+
//|                      Power of 3 EA (PO3)                         |
//|              EURUSD M15 - Accumulation, Manipulation, Expansion |
//+------------------------------------------------------------------+
#property strict

input double LotSize = 0.1;
input int SL_Pips = 20;
input int TP_Pips = 50;
input string TradeSession = "New York";  // Changeable if needed

datetime lastTradeTime = 0;

//+------------------------------------------------------------------+
void OnTick()
{
    if (TimeHour(TimeCurrent()) < 12 || TimeHour(TimeCurrent()) > 17) return; // Only trade NY session

    if (TimeCurrent() - lastTradeTime < 60 * 60) return;  // Avoid double trade per hour

    double asianHigh, asianLow, londonHigh, londonLow;
    GetSessionHighLow(asianHigh, asianLow, 0, 6);
    GetSessionHighLow(londonHigh, londonLow, 7, 10);

    double price = SymbolInfoDouble(_Symbol, SYMBOL_BID);

    if (londonHigh > asianHigh && price < londonHigh)
    {
        // Bearish PO3 Detected
        OpenTrade(ORDER_TYPE_SELL, price);
        lastTradeTime = TimeCurrent();
    }
    else if (londonLow < asianLow && price > londonLow)
    {
        // Bullish PO3 Detected
        OpenTrade(ORDER_TYPE_BUY, price);
        lastTradeTime = TimeCurrent();
    }
}

//+------------------------------------------------------------------+
void GetSessionHighLow(double &high, double &low, int startHour, int endHour)
{
    high = -DBL_MAX;
    low = DBL_MAX;

    for (int i = 0; i < 96; i++)
    {
        datetime t = TimeCurrent() - i * 15 * 60;
        if (TimeHour(t) >= startHour && TimeHour(t) <= endHour)
        {
            double h = iHigh(_Symbol, PERIOD_M15, i);
            double l = iLow(_Symbol, PERIOD_M15, i);
            if (h > high) high = h;
            if (l < low) low = l;
        }
    }
}

//+------------------------------------------------------------------+
void OpenTrade(int type, double price)
{
    double sl = (type == ORDER_TYPE_BUY) ? price - SL_Pips * _Point : price + SL_Pips * _Point;
    double tp = (type == ORDER_TYPE_BUY) ? price + TP_Pips * _Point : price - TP_Pips * _Point;

    trade.Buy(LotSize, _Symbol, price, sl, tp, "PO3 EA");
}

//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
CTrade trade;
