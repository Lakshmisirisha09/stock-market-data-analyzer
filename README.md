# 📈 Stock Market Data Analyzer

> A Python project that fetches/simulates stock data, calculates moving averages, daily returns, volatility, RSI, and generates dark-themed charts and reports — built as a student GitHub portfolio project.

---

## 📌 Problem Statement

Investors, analysts, and finance students need to analyse stock price trends, risk, and performance without expensive tools. This project automates the full analysis pipeline using free/public data.

---

## 🎯 Features

| Feature | Details |
|---|---|
| 📂 Simulation Mode | 6 pre-loaded stocks (AAPL, GOOGL, TSLA, INFY, TCS, RELIANCE) — no internet needed |
| 🌐 Live Mode | Fetch real data via `yfinance` for any global ticker |
| 📊 Moving Averages | SMA-20, SMA-50, SMA-200 |
| 📉 Returns | Daily return % with colour-coded bar chart |
| ⚠️ Volatility | 20-day rolling volatility chart |
| 💹 RSI | 14-day Relative Strength Index with overbought/oversold zones |
| 🖥️ Dashboard | Full summary dashboard in one chart |
| 📄 Reports | CSV data export + TXT insight report |
| 🔀 Comparison | Side-by-side multi-stock comparison table |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- `pandas` — data manipulation
- `numpy` — numerical calculations
- `matplotlib` + `seaborn` — dark-themed charts
- `yfinance` — live stock data (optional)
- `scipy` — statistical analysis

---

## 📁 Folder Structure

```
Stock-Market-Data-Analyzer/
├── data/
│   ├── AAPL.csv          ← Simulation CSVs (auto-generated)
│   ├── TSLA.csv
│   └── generate_sample_data.py
├── src/
│   ├── data_loader.py    ← CSV + yfinance loader
│   ├── analyzer.py       ← Returns, MAs, RSI, Volatility
│   ├── visualizer.py     ← All charts
│   ├── report_generator.py
│   └── display.py
├── outputs/              ← Generated PNG charts
├── reports/              ← Generated CSV + TXT reports
├── images/               ← Screenshots for README
├── notebooks/            ← Jupyter notebooks (optional)
├── docs/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

```bash
git clone https://github.com/your-username/Stock-Market-Data-Analyzer.git
cd Stock-Market-Data-Analyzer

python -m venv venv
# Windows:  venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 How to Run

### ✅ Simulation Mode (no internet needed)
```bash
python main.py --ticker AAPL
python main.py --ticker TSLA
python main.py --ticker INFY
python main.py --ticker TCS
python main.py --ticker RELIANCE

# Compare multiple stocks
python main.py --compare AAPL,TSLA,INFY
```

### 🌐 Live Mode (requires internet + yfinance)
```bash
python main.py --ticker AAPL --live
python main.py --ticker RELIANCE.NS --live   # Indian stocks
python main.py --ticker HDFCBANK.NS --live
```

### 🖥️ Interactive Menu
```bash
python main.py
```

---

## 📊 Available Simulation Stocks

| Ticker | Company |
|---|---|
| AAPL | Apple Inc. |
| GOOGL | Alphabet (Google) |
| TSLA | Tesla Inc. |
| INFY | Infosys (India) |
| TCS | Tata Consultancy Services |
| RELIANCE | Reliance Industries |

---

## 📄 Generated Outputs

Each run creates in `outputs/`:
- `{ticker}_price_ma.png` — Price + Moving Averages
- `{ticker}_daily_returns.png` — Daily return bars
- `{ticker}_distribution.png` — Return distribution
- `{ticker}_volatility.png` — Rolling volatility
- `{ticker}_rsi.png` — RSI indicator
- `{ticker}_dashboard.png` — Full summary dashboard

And in `reports/`:
- `{ticker}_analysis.csv` — Full data with all indicators
- `{ticker}_report.txt` — Human-readable insight report

---

## 🎓 Learning Outcomes

- Fetching and parsing financial data with `pandas`
- Time-series analysis and rolling window calculations
- Technical indicators (SMA, RSI, Volatility, Sharpe Ratio)
- Data visualisation with `matplotlib` and `seaborn`
- Modular Python project structure
- CSV report generation
- Git & GitHub workflow

---

## ⚠️ Disclaimer

> This project is for **educational purposes only** and does **not** constitute financial or investment advice. The analysis and insights generated are based on historical data and simulations. Always consult a qualified financial advisor before making investment decisions.

---

## 🏷️ GitHub Tags

`python` `stock-market` `data-analysis` `pandas` `matplotlib` `yfinance` `financial-analysis` `technical-analysis` `portfolio-project` `beginner-friendly`

---

## 👤 Author

**Your Name** — [@your-username](https://github.com/your-username)
