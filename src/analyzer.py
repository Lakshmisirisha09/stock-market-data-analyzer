# src/analyzer.py
# ─────────────────────────────────────────────────────────
# Core financial calculations:
#   daily returns, moving averages, volatility, risk metrics
# ─────────────────────────────────────────────────────────

import pandas as pd
import numpy as np


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Add Daily_Return column (percentage change in Close price)."""
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change() * 100
    return df


def calculate_moving_averages(df: pd.DataFrame,
                               windows: list[int] = [20, 50, 200]) -> pd.DataFrame:
    """Add SMA (Simple Moving Average) columns for given windows."""
    df = df.copy()
    for w in windows:
        col = f"SMA_{w}"
        df[col] = df["Close"].rolling(window=w).mean().round(2)
    return df


def calculate_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Add rolling volatility (std dev of daily returns) column."""
    df = df.copy()
    df["Volatility"] = df["Daily_Return"].rolling(window=window).std().round(4)
    return df


def calculate_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """Add RSI (Relative Strength Index) — momentum indicator."""
    df = df.copy()
    delta = df["Close"].diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI"] = (100 - (100 / (1 + rs))).round(2)
    return df


def full_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Run all calculations in one call."""
    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df, windows=[20, 50, 200])
    df = calculate_volatility(df)
    df = calculate_rsi(df)
    return df


def get_summary(ticker: str, df: pd.DataFrame) -> dict:
    """Return a dict of key statistics for the stock."""
    clean = df.dropna(subset=["Daily_Return"])

    total_return = ((df["Close"].iloc[-1] - df["Close"].iloc[0])
                    / df["Close"].iloc[0] * 100)

    return {
        "ticker":          ticker,
        "period":          f"{df['Date'].iloc[0].date()} → {df['Date'].iloc[-1].date()}",
        "trading_days":    len(df),
        "start_price":     round(df["Close"].iloc[0], 2),
        "end_price":       round(df["Close"].iloc[-1], 2),
        "highest_price":   round(df["High"].max(), 2),
        "lowest_price":    round(df["Low"].min(), 2),
        "total_return_%":  round(total_return, 2),
        "avg_daily_return":round(clean["Daily_Return"].mean(), 4),
        "daily_volatility":round(clean["Daily_Return"].std(), 4),
        "annual_volatility":round(clean["Daily_Return"].std() * np.sqrt(252), 2),
        "best_day_%":      round(clean["Daily_Return"].max(), 2),
        "worst_day_%":     round(clean["Daily_Return"].min(), 2),
        "positive_days":   int((clean["Daily_Return"] > 0).sum()),
        "negative_days":   int((clean["Daily_Return"] < 0).sum()),
        "sharpe_ratio":    round(
            clean["Daily_Return"].mean() / clean["Daily_Return"].std() * np.sqrt(252), 3
        ) if clean["Daily_Return"].std() != 0 else 0,
        "current_rsi":     round(df["RSI"].dropna().iloc[-1], 2) if "RSI" in df else None,
    }
