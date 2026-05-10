#!/usr/bin/env python3
"""
main.py — Stock Market Data Analyzer
======================================
Usage:
  python main.py                        # interactive menu
  python main.py --ticker AAPL          # simulate AAPL
  python main.py --ticker TSLA --live   # live data (needs yfinance)
  python main.py --compare AAPL,TSLA,INFY
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_loader      import load_stock_data, AVAILABLE_TICKERS
from analyzer         import full_analysis, get_summary
from visualizer       import (plot_price_and_ma, plot_daily_returns,
                               plot_return_distribution, plot_volatility,
                               plot_rsi, plot_dashboard)
from report_generator import save_csv_report, save_text_report, generate_insights
from display          import print_banner, print_summary, print_insights, print_saved_files


# ─────────────────────────────────────────────────────────
def analyse_ticker(ticker: str, mode: str = "simulate",
                   start: str = "2023-01-01", end: str = "2024-01-01"):
    """Full pipeline for one ticker."""
    print(f"\n{'─'*56}")
    print(f"  Analysing: {ticker.upper()}  [{mode} mode]")
    print(f"{'─'*56}")

    # 1. Load
    df = load_stock_data(ticker, mode=mode, start=start, end=end)
    if df is None:
        return

    # 2. Analyse
    df = full_analysis(df)

    # 3. Summary + insights
    summary  = get_summary(ticker.upper(), df)
    insights = generate_insights(summary)
    print_summary(ticker.upper(), summary)
    print_insights(insights)

    # 4. Charts
    saved = []
    print("  📊  Generating charts …", end=" ", flush=True)
    try:
        saved.append(plot_price_and_ma(ticker.upper(), df))
        saved.append(plot_daily_returns(ticker.upper(), df))
        saved.append(plot_return_distribution(ticker.upper(), df))
        saved.append(plot_volatility(ticker.upper(), df))
        saved.append(plot_rsi(ticker.upper(), df))
        saved.append(plot_dashboard(ticker.upper(), df, summary))
        print("done ✅")
    except Exception as e:
        print(f"⚠️  Chart error: {e}")

    # 5. Reports
    print("  📝  Saving reports …", end=" ", flush=True)
    try:
        saved.append(save_csv_report(ticker.upper(), df, summary))
        saved.append(save_text_report(ticker.upper(), summary, insights))
        print("done ✅")
    except Exception as e:
        print(f"⚠️  Report error: {e}")

    print_saved_files(saved)


# ─────────────────────────────────────────────────────────
def compare_tickers(tickers: list[str], mode: str = "simulate"):
    """Compare multiple stocks side-by-side (summary table)."""
    import pandas as pd

    summaries = []
    for t in tickers:
        df = load_stock_data(t, mode=mode)
        if df is None:
            continue
        df = full_analysis(df)
        summaries.append(get_summary(t.upper(), df))

    if not summaries:
        print("No data loaded.")
        return

    comp = pd.DataFrame(summaries).set_index("ticker")
    cols = ["total_return_%", "annual_volatility", "sharpe_ratio",
            "current_rsi", "highest_price", "lowest_price"]
    available_cols = [c for c in cols if c in comp.columns]

    print("\n" + "="*60)
    print("  📊  COMPARISON TABLE")
    print("="*60)
    print(comp[available_cols].to_string())
    print("="*60 + "\n")

    # Save comparison CSV
    out = os.path.join("reports", "comparison_" +
                       "_".join(t.lower() for t in tickers) + ".csv")
    os.makedirs("reports", exist_ok=True)
    comp[available_cols].to_csv(out)
    print(f"  ✅  Comparison saved → {out}\n")


# ─────────────────────────────────────────────────────────
def interactive_menu():
    print_banner()
    print("  Choose an option:")
    print("    [1] Analyse a single stock (simulation)")
    print("    [2] Analyse a single stock (live API — needs yfinance)")
    print("    [3] Compare multiple stocks")
    print("    [4] Exit")

    choice = input("\n  Your choice [1/2/3/4]: ").strip()

    if choice == "1":
        print(f"\n  Available tickers: {', '.join(AVAILABLE_TICKERS)}")
        t = input("  Enter ticker: ").strip().upper()
        analyse_ticker(t, mode="simulate")

    elif choice == "2":
        t     = input("  Enter ticker (e.g. AAPL, RELIANCE.NS): ").strip().upper()
        start = input("  Start date [2023-01-01]: ").strip() or "2023-01-01"
        end   = input("  End date   [2024-01-01]: ").strip() or "2024-01-01"
        analyse_ticker(t, mode="live", start=start, end=end)

    elif choice == "3":
        print(f"\n  Available: {', '.join(AVAILABLE_TICKERS)}")
        raw = input("  Enter tickers separated by comma (e.g. AAPL,TSLA,INFY): ")
        tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
        compare_tickers(tickers)

    elif choice == "4":
        print("\n  Goodbye! 👋\n")
        sys.exit(0)
    else:
        print("❌ Invalid choice.")


# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    parser.add_argument("--ticker",  type=str, help="Single ticker to analyse")
    parser.add_argument("--live",    action="store_true", help="Use live yfinance data")
    parser.add_argument("--compare", type=str, help="Comma-separated tickers to compare")
    parser.add_argument("--start",   type=str, default="2023-01-01")
    parser.add_argument("--end",     type=str, default="2024-01-01")
    args = parser.parse_args()

    print_banner()

    if args.compare:
        tickers = [t.strip().upper() for t in args.compare.split(",")]
        compare_tickers(tickers, mode="live" if args.live else "simulate")
    elif args.ticker:
        analyse_ticker(args.ticker,
                       mode="live" if args.live else "simulate",
                       start=args.start, end=args.end)
    else:
        interactive_menu()
