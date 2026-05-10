# src/display.py
# Terminal pretty-printing helpers

from datetime import datetime


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║   📈   STOCK MARKET DATA ANALYZER                    ║
║        Built with Python · Pandas · Matplotlib       ║
╚══════════════════════════════════════════════════════╝
""")


def print_summary(ticker: str, summary: dict):
    sep = "─" * 56
    ret = summary["total_return_%"]
    arrow = "📈" if ret >= 0 else "📉"

    print(f"\n{sep}")
    print(f"  {arrow}  ANALYSIS SUMMARY — {ticker}")
    print(f"  📅  {summary['period']}")
    print(sep)
    print(f"  Start Price        : {summary['start_price']}")
    print(f"  End Price          : {summary['end_price']}")
    print(f"  Highest Price      : {summary['highest_price']}")
    print(f"  Lowest Price       : {summary['lowest_price']}")
    print(f"  Total Return       : {ret}%")
    print(f"  Annual Volatility  : {summary['annual_volatility']}%")
    print(f"  Sharpe Ratio       : {summary['sharpe_ratio']}")
    print(f"  Current RSI        : {summary['current_rsi']}")
    print(f"  Best Day           : +{summary['best_day_%']}%")
    print(f"  Worst Day          : {summary['worst_day_%']}%")
    print(f"  Positive Days      : {summary['positive_days']}")
    print(f"  Negative Days      : {summary['negative_days']}")
    print(sep)


def print_insights(insights: list[str]):
    print("\n  💡  INSIGHTS")
    print("  " + "─" * 50)
    for i in insights:
        print(f"  {i}")
    print()


def print_saved_files(files: list[str]):
    print("\n  📁  SAVED FILES")
    print("  " + "─" * 50)
    for f in files:
        print(f"  ✅  {f}")
    print()
