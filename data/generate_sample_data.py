import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

STOCKS = {
    "AAPL":  {"start_price": 150.0, "trend": 0.0004, "volatility": 0.018},
    "GOOGL": {"start_price": 2800.0,"trend": 0.0003, "volatility": 0.020},
    "TSLA":  {"start_price": 250.0, "trend": 0.0005, "volatility": 0.040},
    "INFY":  {"start_price": 1600.0,"trend": 0.0003, "volatility": 0.016},
    "TCS":   {"start_price": 3400.0,"trend": 0.0003, "volatility": 0.014},
    "RELIANCE": {"start_price": 2400.0,"trend": 0.0004,"volatility": 0.017},
}

START_DATE = datetime(2023, 1, 1)
DAYS = 365

out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(out_dir, exist_ok=True)

dates = []
d = START_DATE
while len(dates) < DAYS:
    if d.weekday() < 5:   # Mon-Fri only
        dates.append(d)
    d += timedelta(days=1)

for ticker, cfg in STOCKS.items():
    price = cfg["start_price"]
    rows  = []
    for date in dates:
        open_p  = price * (1 + np.random.normal(0, cfg["volatility"] * 0.3))
        high_p  = open_p * (1 + abs(np.random.normal(0, cfg["volatility"] * 0.5)))
        low_p   = open_p * (1 - abs(np.random.normal(0, cfg["volatility"] * 0.5)))
        close_p = open_p * (1 + np.random.normal(cfg["trend"], cfg["volatility"]))
        close_p = max(close_p, low_p * 1.001)
        volume  = int(np.random.normal(5_000_000, 1_500_000))
        rows.append({
            "Date":   date.strftime("%Y-%m-%d"),
            "Open":   round(open_p, 2),
            "High":   round(high_p, 2),
            "Low":    round(low_p, 2),
            "Close":  round(close_p, 2),
            "Volume": max(volume, 100_000),
        })
        price = close_p

    df = pd.DataFrame(rows)
    path = os.path.join(out_dir, f"{ticker}.csv")
    df.to_csv(path, index=False)
    print(f"  ✅  {ticker}.csv  ({len(df)} rows)")

print("\nAll sample CSVs generated.")
