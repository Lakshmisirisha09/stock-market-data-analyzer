# src/data_loader.py
# ─────────────────────────────────────────────────────────
# Loads stock data from yfinance (live) or local CSV (sim)
# ─────────────────────────────────────────────────────────

import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

AVAILABLE_TICKERS = ["AAPL", "GOOGL", "TSLA", "INFY", "TCS", "RELIANCE"]


def load_from_csv(ticker: str) -> pd.DataFrame | None:
    """Load stock data from a local CSV file."""
    path = os.path.join(DATA_DIR, f"{ticker.upper()}.csv")
    if not os.path.exists(path):
        print(f"❌ No CSV found for '{ticker}'. Available: {', '.join(AVAILABLE_TICKERS)}")
        return None
    df = pd.read_csv(path, parse_dates=["Date"])
    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def load_from_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame | None:
    """Fetch live stock data using yfinance."""
    try:
        import yfinance as yf
        raw = yf.download(ticker, start=start, end=end, progress=False)
        if raw.empty:
            print(f"❌ No data returned for '{ticker}'. Check the ticker symbol.")
            return None
        raw.reset_index(inplace=True)
        raw.columns = [c[0] if isinstance(c, tuple) else c for c in raw.columns]
        raw.rename(columns={"Date": "Date", "Adj Close": "Close"}, inplace=True)
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col not in raw.columns:
                raw[col] = 0
        return raw[["Date", "Open", "High", "Low", "Close", "Volume"]]
    except ImportError:
        print("⚠️  yfinance not installed. Falling back to CSV simulation.")
        return None
    except Exception as e:
        print(f"❌ yfinance error: {e}")
        return None


def load_stock_data(ticker: str, mode: str = "simulate",
                    start: str = "2023-01-01", end: str = "2024-01-01") -> pd.DataFrame | None:
    """
    Main loader. mode = 'simulate' | 'live'
    Returns a clean DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    ticker = ticker.upper()

    if mode == "live":
        print(f"  🌐  Fetching live data for {ticker} …")
        df = load_from_yfinance(ticker, start, end)
        if df is None:
            print("  ↩️  Falling back to simulation CSV …")
            df = load_from_csv(ticker)
    else:
        print(f"  📂  Loading simulation data for {ticker} …")
        df = load_from_csv(ticker)

    if df is not None:
        print(f"  ✅  Loaded {len(df)} trading days for {ticker}")

    return df
