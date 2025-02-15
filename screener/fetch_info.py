import yfinance as yf
import pandas as pd

def fetch_all_stocks(symbols=None):
    
    if symbols is None:

        symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
            "HINDUNILVR.NS", "ITC.NS", "KOTAKBANK.NS", "SBIN.NS", "LT.NS",
            "BHARTIARTL.NS", "AXISBANK.NS", "HCLTECH.NS", "MARUTI.NS", "ASIANPAINT.NS",
            "BAJFINANCE.NS", "SUNPHARMA.NS", "TITAN.NS", "TATASTEEL.NS", "ULTRACEMCO.NS",
            "WIPRO.NS", "INDUSINDBK.NS", "POWERGRID.NS", "NTPC.NS", "M&M.NS",
            "TECHM.NS", "NESTLEIND.NS", "JSWSTEEL.NS", "BAJAJFINSV.NS", "CIPLA.NS",
            "HDFCLIFE.NS", "DRREDDY.NS", "TATAMOTORS.NS", "ADANIENT.NS", "BRITANNIA.NS",
            "GRASIM.NS", "DIVISLAB.NS", "SBILIFE.NS", "HEROMOTOCO.NS", "BPCL.NS",
            "COALINDIA.NS", "EICHERMOT.NS", "APOLLOHOSP.NS", "ONGC.NS", "HAVELLS.NS",
            "BAJAJ-AUTO.NS", "DLF.NS", "PIDILITIND.NS", "ADANIPORTS.NS", "TATACONSUM.NS"]


    stock_data = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)

        try:
            info = stock.info

            stock_data.append({
                "symbol": symbol,
                "marketCap": info.get("marketCap", 0),
                "totalRevenue": info.get("totalRevenue", 0),
                "trailingPE": info.get("trailingPE", None),
                "returnOnEquity": info.get("returnOnEquity", None),
                "debtToEquity": info.get("debtToEquity", None),
                "priceToBook": info.get("priceToBooks", None),
                "earningPerShare": info.get("trailingEps", None),
                "dividendYeilds": info.get("dividendYield", None),
                "enterpriseValue": info.get("enterpriseValue", None),
                "netIncome": info.get("netIncome", None),
                "returnOnEquity": info.get("returnOnEquity", None),
                "returnOnAssets": info.get("returnOnAssets", None),
                "operatingMargin": info.get("operatingMargins", None),
                "profitMargin": info.get("profitMargins", None),
                "debtToEquityRatio": info.get("debtToEquity", None),
                "currentRatio": info.get("currentRatio", None),
                "quickRatio": info.get("quickRatio", None)
                })

        except Exception as e:
            print(f"data for {symbol} not available")

    return pd.DataFrame(stock_data)
