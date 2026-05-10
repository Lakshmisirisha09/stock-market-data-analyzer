# src/visualizer.py
# ─────────────────────────────────────────────────────────
# Generates and saves all Matplotlib / Seaborn charts
# ─────────────────────────────────────────────────────────

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Dark theme setup ──────────────────────────────────────
DARK_BG   = "#0d1117"
PANEL_BG  = "#161b22"
GRID_COL  = "#21262d"
TEXT_COL  = "#e6edf3"
ACCENT    = "#58a6ff"
GREEN     = "#3fb950"
RED       = "#f85149"
ORANGE    = "#d29922"
PURPLE    = "#bc8cff"

def _style():
    plt.rcParams.update({
        "figure.facecolor":  DARK_BG,
        "axes.facecolor":    PANEL_BG,
        "axes.edgecolor":    GRID_COL,
        "axes.labelcolor":   TEXT_COL,
        "text.color":        TEXT_COL,
        "xtick.color":       TEXT_COL,
        "ytick.color":       TEXT_COL,
        "grid.color":        GRID_COL,
        "grid.linestyle":    "--",
        "grid.alpha":        0.6,
        "legend.facecolor":  PANEL_BG,
        "legend.edgecolor":  GRID_COL,
        "legend.labelcolor": TEXT_COL,
        "font.size":         10,
    })

def _save(fig, name: str) -> str:
    path = os.path.join(OUTPUT_DIR, name)
    plt.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


# ── 1. Price + Moving Averages ────────────────────────────
def plot_price_and_ma(ticker: str, df) -> str:
    _style()
    fig, ax = plt.subplots(figsize=(13, 5))

    ax.plot(df["Date"], df["Close"],  color=ACCENT,  linewidth=1.5,
            label="Close Price", zorder=3)

    colors = [GREEN, ORANGE, PURPLE]
    for col, c in zip(["SMA_20", "SMA_50", "SMA_200"], colors):
        if col in df.columns:
            ax.plot(df["Date"], df[col], color=c, linewidth=1.2,
                    linestyle="--", label=col, zorder=2)

    ax.set_title(f"{ticker} — Price & Moving Averages", fontsize=14,
                 fontweight="bold", color=TEXT_COL, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    return _save(fig, f"{ticker.lower()}_price_ma.png")


# ── 2. Daily Returns ──────────────────────────────────────
def plot_daily_returns(ticker: str, df) -> str:
    _style()
    fig, ax = plt.subplots(figsize=(13, 4))

    colors = [GREEN if r >= 0 else RED for r in df["Daily_Return"].fillna(0)]
    ax.bar(df["Date"], df["Daily_Return"], color=colors, width=1.0, zorder=3)
    ax.axhline(0, color=TEXT_COL, linewidth=0.8)

    ax.set_title(f"{ticker} — Daily Returns (%)", fontsize=14,
                 fontweight="bold", color=TEXT_COL, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Return (%)")
    ax.grid(True, axis="y")

    return _save(fig, f"{ticker.lower()}_daily_returns.png")


# ── 3. Return Distribution ────────────────────────────────
def plot_return_distribution(ticker: str, df) -> str:
    _style()
    fig, ax = plt.subplots(figsize=(9, 5))

    returns = df["Daily_Return"].dropna()
    ax.hist(returns, bins=50, color=ACCENT, edgecolor=DARK_BG,
            alpha=0.8, zorder=3, label="Daily Returns")

    # Normal curve overlay
    mu, sigma = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 300)
    from scipy.stats import norm
    try:
        y = norm.pdf(x, mu, sigma) * len(returns) * (returns.max() - returns.min()) / 50
        ax.plot(x, y, color=ORANGE, linewidth=2, label="Normal fit")
    except Exception:
        pass

    ax.axvline(mu,       color=GREEN,  linestyle="--", linewidth=1.5, label=f"Mean {mu:.2f}%")
    ax.axvline(mu+sigma, color=RED,    linestyle=":",  linewidth=1.2, label=f"+1σ {mu+sigma:.2f}%")
    ax.axvline(mu-sigma, color=RED,    linestyle=":",  linewidth=1.2, label=f"-1σ {mu-sigma:.2f}%")

    ax.set_title(f"{ticker} — Return Distribution", fontsize=14,
                 fontweight="bold", color=TEXT_COL, pad=12)
    ax.set_xlabel("Daily Return (%)")
    ax.set_ylabel("Frequency")
    ax.legend()
    ax.grid(True, axis="y")

    return _save(fig, f"{ticker.lower()}_distribution.png")


# ── 4. Volatility ─────────────────────────────────────────
def plot_volatility(ticker: str, df) -> str:
    _style()
    fig, ax = plt.subplots(figsize=(13, 4))

    ax.fill_between(df["Date"], df["Volatility"], color=ORANGE,
                    alpha=0.4, zorder=2)
    ax.plot(df["Date"], df["Volatility"], color=ORANGE, linewidth=1.5, zorder=3)

    ax.set_title(f"{ticker} — 20-Day Rolling Volatility", fontsize=14,
                 fontweight="bold", color=TEXT_COL, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility (Std Dev of Returns)")
    ax.grid(True)

    return _save(fig, f"{ticker.lower()}_volatility.png")


# ── 5. RSI ────────────────────────────────────────────────
def plot_rsi(ticker: str, df) -> str:
    _style()
    fig, ax = plt.subplots(figsize=(13, 4))

    ax.plot(df["Date"], df["RSI"], color=PURPLE, linewidth=1.5, zorder=3)
    ax.axhline(70, color=RED,   linestyle="--", linewidth=1.2, label="Overbought (70)")
    ax.axhline(30, color=GREEN, linestyle="--", linewidth=1.2, label="Oversold (30)")
    ax.fill_between(df["Date"], df["RSI"], 70,
                    where=(df["RSI"] >= 70), color=RED,   alpha=0.15)
    ax.fill_between(df["Date"], df["RSI"], 30,
                    where=(df["RSI"] <= 30), color=GREEN, alpha=0.15)

    ax.set_ylim(0, 100)
    ax.set_title(f"{ticker} — RSI (14-day)", fontsize=14,
                 fontweight="bold", color=TEXT_COL, pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("RSI")
    ax.legend()
    ax.grid(True)

    return _save(fig, f"{ticker.lower()}_rsi.png")


# ── 6. Summary Dashboard ──────────────────────────────────
def plot_dashboard(ticker: str, df, summary: dict) -> str:
    _style()
    fig = plt.figure(figsize=(16, 10), facecolor=DARK_BG)
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3)

    # Price + MA
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(PANEL_BG)
    ax1.plot(df["Date"], df["Close"], color=ACCENT, linewidth=1.5, label="Close")
    for col, c in zip(["SMA_20","SMA_50","SMA_200"], [GREEN, ORANGE, PURPLE]):
        if col in df.columns:
            ax1.plot(df["Date"], df[col], color=c, linewidth=1, linestyle="--", label=col)
    ax1.set_title(f"{ticker} — Price & MAs", fontweight="bold")
    ax1.legend(fontsize=8); ax1.grid(True)

    # Daily returns
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(PANEL_BG)
    colors = [GREEN if r >= 0 else RED for r in df["Daily_Return"].fillna(0)]
    ax2.bar(df["Date"], df["Daily_Return"], color=colors, width=1.0)
    ax2.axhline(0, color=TEXT_COL, linewidth=0.6)
    ax2.set_title("Daily Returns (%)", fontweight="bold"); ax2.grid(True, axis="y")

    # Volatility
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(PANEL_BG)
    ax3.fill_between(df["Date"], df["Volatility"], color=ORANGE, alpha=0.4)
    ax3.plot(df["Date"], df["Volatility"], color=ORANGE, linewidth=1.2)
    ax3.set_title("20-Day Volatility", fontweight="bold"); ax3.grid(True)

    # RSI
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.set_facecolor(PANEL_BG)
    ax4.plot(df["Date"], df["RSI"], color=PURPLE, linewidth=1.2)
    ax4.axhline(70, color=RED,   linestyle="--", linewidth=1)
    ax4.axhline(30, color=GREEN, linestyle="--", linewidth=1)
    ax4.set_ylim(0, 100)
    ax4.set_title("RSI (14-day)", fontweight="bold"); ax4.grid(True)

    # Summary stats text box
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.set_facecolor(PANEL_BG)
    ax5.axis("off")
    stats = [
        f"Period :  {summary['period']}",
        f"Start  :  {summary['start_price']}",
        f"End    :  {summary['end_price']}",
        f"High   :  {summary['highest_price']}",
        f"Low    :  {summary['lowest_price']}",
        f"Return :  {summary['total_return_%']}%",
        f"Ann. Vol: {summary['annual_volatility']}%",
        f"Sharpe :  {summary['sharpe_ratio']}",
        f"RSI    :  {summary['current_rsi']}",
        f"Best Day: +{summary['best_day_%']}%",
        f"Worst  :  {summary['worst_day_%']}%",
    ]
    color = GREEN if summary["total_return_%"] >= 0 else RED
    ax5.text(0.05, 0.95, f"📊 {ticker} Summary",
             transform=ax5.transAxes, fontsize=11, fontweight="bold",
             color=color, va="top")
    ax5.text(0.05, 0.80, "\n".join(stats),
             transform=ax5.transAxes, fontsize=9,
             color=TEXT_COL, va="top", family="monospace")

    fig.suptitle(f"{ticker} — Full Analysis Dashboard",
                 fontsize=16, fontweight="bold", color=TEXT_COL, y=1.01)

    return _save(fig, f"{ticker.lower()}_dashboard.png")
