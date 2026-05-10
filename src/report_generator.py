# src/report_generator.py
# ─────────────────────────────────────────────────────────
# Saves analysis results to CSV and TXT reports
# ─────────────────────────────────────────────────────────

import csv
import os
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_csv_report(ticker: str, df, summary: dict) -> str:
    """Save full processed data + summary to CSV."""
    fname = f"{ticker.lower()}_analysis_{_ts()}.csv"
    path  = os.path.join(REPORTS_DIR, fname)

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Summary section
        w.writerow(["=== STOCK ANALYSIS SUMMARY ==="])
        w.writerow(["Ticker", ticker])
        w.writerow(["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        w.writerow([])
        for k, v in summary.items():
            w.writerow([k.replace("_", " ").title(), v])
        w.writerow([])

        # Data section
        w.writerow(["=== DAILY DATA ==="])
        cols = ["Date", "Open", "High", "Low", "Close", "Volume",
                "Daily_Return", "SMA_20", "SMA_50", "SMA_200",
                "Volatility", "RSI"]
        available = [c for c in cols if c in df.columns]
        w.writerow(available)
        for _, row in df[available].iterrows():
            w.writerow([str(v) for v in row.values])

    return path


def save_text_report(ticker: str, summary: dict, insights: list[str]) -> str:
    """Save a human-readable analysis report."""
    fname = f"{ticker.lower()}_report_{_ts()}.txt"
    path  = os.path.join(REPORTS_DIR, fname)
    sep   = "=" * 58

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{sep}\n")
        f.write(f"  STOCK MARKET ANALYSIS REPORT\n")
        f.write(f"  Ticker    : {ticker}\n")
        f.write(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{sep}\n\n")

        f.write("KEY STATISTICS\n")
        f.write(f"  Period             : {summary['period']}\n")
        f.write(f"  Trading Days       : {summary['trading_days']}\n")
        f.write(f"  Start Price        : {summary['start_price']}\n")
        f.write(f"  End Price          : {summary['end_price']}\n")
        f.write(f"  Highest Price      : {summary['highest_price']}\n")
        f.write(f"  Lowest Price       : {summary['lowest_price']}\n")
        f.write(f"  Total Return       : {summary['total_return_%']}%\n")
        f.write(f"  Avg Daily Return   : {summary['avg_daily_return']}%\n")
        f.write(f"  Annual Volatility  : {summary['annual_volatility']}%\n")
        f.write(f"  Sharpe Ratio       : {summary['sharpe_ratio']}\n")
        f.write(f"  Current RSI        : {summary['current_rsi']}\n")
        f.write(f"  Best Day           : +{summary['best_day_%']}%\n")
        f.write(f"  Worst Day          : {summary['worst_day_%']}%\n")
        f.write(f"  Positive Days      : {summary['positive_days']}\n")
        f.write(f"  Negative Days      : {summary['negative_days']}\n\n")

        f.write("ANALYSIS INSIGHTS\n")
        for insight in insights:
            f.write(f"  {insight}\n")

        f.write(f"\n{sep}\n")
        f.write("  ⚠️  DISCLAIMER\n")
        f.write("  This report is for EDUCATIONAL PURPOSES ONLY.\n")
        f.write("  It does NOT constitute financial or investment advice.\n")
        f.write("  Always consult a qualified financial advisor.\n")
        f.write(f"{sep}\n")

    return path


def generate_insights(summary: dict) -> list[str]:
    """Rule-based insights from summary statistics."""
    insights = []

    ret = summary["total_return_%"]
    if ret > 20:
        insights.append(f"📈 Strong performer: {ret}% total return over the period.")
    elif ret > 0:
        insights.append(f"📈 Modest positive return of {ret}% over the period.")
    else:
        insights.append(f"📉 Negative return of {ret}% — stock declined over this period.")

    vol = summary["annual_volatility"]
    if vol > 40:
        insights.append(f"⚠️  High annual volatility ({vol}%) — suitable for risk-tolerant investors.")
    elif vol > 20:
        insights.append(f"📊 Moderate volatility ({vol}%) — typical for growth stocks.")
    else:
        insights.append(f"✅ Low volatility ({vol}%) — relatively stable stock.")

    sharpe = summary["sharpe_ratio"]
    if sharpe > 1.5:
        insights.append(f"💹 Excellent Sharpe ratio ({sharpe}) — good risk-adjusted returns.")
    elif sharpe > 0.5:
        insights.append(f"💹 Acceptable Sharpe ratio ({sharpe}).")
    else:
        insights.append(f"⚠️  Low Sharpe ratio ({sharpe}) — poor risk-adjusted performance.")

    rsi = summary["current_rsi"]
    if rsi:
        if rsi > 70:
            insights.append(f"🔴 RSI {rsi} — stock may be OVERBOUGHT. Watch for pullback.")
        elif rsi < 30:
            insights.append(f"🟢 RSI {rsi} — stock may be OVERSOLD. Possible recovery signal.")
        else:
            insights.append(f"🟡 RSI {rsi} — stock is in NEUTRAL territory.")

    pos  = summary["positive_days"]
    neg  = summary["negative_days"]
    total = pos + neg
    win_rate = round(pos / total * 100, 1) if total else 0
    insights.append(f"📅 Win rate: {pos}/{total} days positive ({win_rate}%).")

    return insights
