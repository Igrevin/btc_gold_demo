# ₿ Bitcoin vs 🥇 Gold

## Is Bitcoin Really Digital Gold?

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Analysis-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?logo=python&logoColor=white)](https://matplotlib.org/)
[![MariaDB](https://img.shields.io/badge/MariaDB-Database-003545?logo=mariadb&logoColor=white)](https://mariadb.org/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)

> A quantitative comparison of Bitcoin and Gold during the first half of 2026,
> focusing on performance, trend, momentum, volatility, drawdown,
> relative strength, and correlation.

---

## 🔎 The Question

Bitcoin is often described as **"Digital Gold"**.

But does Bitcoin actually behave like Gold?

This project analyzes Bitcoin (`BTC-USD`) and Gold futures (`GC=F`)
during **H1 2026** to investigate how these two assets behaved across
different dimensions of market performance and risk.

The analysis does **not** attempt to predict future prices.

Instead, it asks:

> **Was Bitcoin really behaving like a digital version of Gold during H1 2026?**

---

## 🎯 Research Questions

### 📈 1. Performance

Which asset generated the stronger performance during H1 2026?

### ⚠️ 2. Risk

Did Bitcoin's return come with substantially higher volatility and drawdown?

### 🔗 3. Correlation

Did Bitcoin consistently move together with Gold?

### ⚖️ 4. Relative Strength

When Bitcoin and Gold diverged, which asset was stronger?

---

# 📊 Analysis Framework

```text
                         Market Data
                              │
                              ▼
                    ┌──────────────────┐
                    │ Data Collection   │
                    │ & Cleaning       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Technical        │
                    │ Indicators       │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           Trend          Momentum         Risk
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    Cross-Asset Analysis
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          BTC/Gold       Correlation      Drawdown
            Ratio
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    Quantitative Findings

📈 Key Analysis
1. Price & Trend
The project analyzes:

SMA 20 / 50 / 200
EMA 20
Bollinger Bands
These indicators are used to identify:

Short-term trends
Medium-term trends
Long-term trends
Price extremes
Changes in trend strength
2. Momentum
RSI
14-day Relative Strength Index.

Used to identify potential overbought / oversold conditions.

MACD
12 / 26 / 9 MACD configuration.

Used to analyze changes in trend momentum.

3. Volatility
The project measures market risk using:

ATR
30-day rolling volatility
Annualized volatility
This allows Bitcoin and Gold to be compared not only by return,
but also by the amount of risk required to achieve that return.

4. Drawdown
Maximum drawdown is calculated from the historical running maximum:

Drawdown = Close / CumMax(Close) - 1

This helps answer:

How severe were the declines from previous highs?

5. BTC / Gold Ratio
Instead of comparing the absolute price of Bitcoin and Gold,
the project calculates:

BTC_Gold_Ratio = BTC_Close / Gold_Close

Interpretation
Ratio ↑ → Bitcoin is outperforming Gold
Ratio ↓ → Gold is outperforming Bitcoin
This provides a more meaningful cross-asset comparison than
plotting their raw prices on the same scale.

6. Rolling Correlation
The project calculates a 30-day rolling correlation between
Bitcoin and Gold daily returns.

Correlation

 +1 ─────────────────────────
    │
  0 ─────────────────────────
    │
 -1 ─────────────────────────
       Jan → Feb → Mar → Apr → May → Jun

A stable high correlation would suggest similar market behavior.

A highly unstable correlation would suggest that Bitcoin and Gold
play different roles depending on market conditions.

📊 Visualizations
Figure 1 — Price & Trend
Includes:

BTC price
Gold price
Bollinger Bands
SMA20
SMA50
EMA20
Figure 2 — Technical Indicators
Includes:

RSI
MACD
ATR
30-day annualized volatility
OBV
Figure 3 — Bitcoin vs Gold
Includes:

Normalized price
BTC / Gold ratio
Rolling correlation
Drawdown
🧮 Risk & Performance
The current analysis focuses on historical behavior.

The next stage of the project will extend the analysis with
risk-adjusted performance metrics.

Metric	Bitcoin	Gold
Total Return	—	—
Annualized Return	—	—
Annualized Volatility	—	—
Sharpe Ratio	—	—
Sortino Ratio	—	—
Maximum Drawdown	—	—

Metrics will be calculated directly from the H1 2026 dataset
to ensure reproducibility.

🗄️ Data Pipeline
Yahoo Finance
      │
      ▼
   yfinance
      │
      ▼
Data Cleaning
      │
      ▼
Indicator Calculation
      │
      ├───────────────┐
      ▼               ▼
 Visualization     MariaDB
      │               │
      └───────┬───────┘
              ▼
       Research Output

Data
Item	Value
Bitcoin	BTC-USD
Gold	GC=F
Frequency	Daily
Analysis Period	2026-01-01 → 2026-06-30
Source	Yahoo Finance
Download Library	yfinance

🛠️ Tech Stack
Technology	Purpose
Python	Core development
Pandas	Time-series analysis
NumPy	Numerical calculations
yfinance	Market data
ta	Technical indicators
Matplotlib	Visualization
MariaDB	Persistent data storage
uv	Dependency management

📁 Project Structure
btc_gold_demo/
│
├── src/
│   └── btd_gold_demo/
│       └── ...
│
├── btc_gold_parser.py
│
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
└── .gitignore

🚀 Quick Start
Requirements
Python 3.12+
uv
Internet connection for Yahoo Finance data
MariaDB is optional unless database storage is enabled.

Installation
Clone the repository:

git clone https://github.com/Igrevin/btc_gold_demo.git
cd btc_gold_demo

Install dependencies:

uv sync

Run the analysis:

uv run python btc_gold_parser.py

The program downloads the market data, calculates the indicators,
and generates the analysis figures.

🗃️ MariaDB
The project includes optional MariaDB integration.

Database:

btc_gold_db

Table:

btc_gold_data

Current schema stores:

Symbol
Trade date
OHLC prices
Adjusted close
Volume
SMA20
Database writing is intentionally optional so that the analysis
can run without a configured database.

🧪 Data Considerations
Different Trading Calendars
Bitcoin trades 24/7, while Gold futures have specific trading
sessions and market holidays.

Therefore, the two assets do not necessarily contain the same
number of observations.

Volume Interpretation
Bitcoin volume and Gold futures volume represent different
market structures and should not be interpreted as directly
equivalent measures of liquidity.

Indicator Warm-up
Longer indicators such as SMA200 require sufficient historical
data before meaningful values can be calculated.

Data Source
Historical data is retrieved from Yahoo Finance and may change
in availability, formatting, or historical adjustments.

🗺️ Roadmap
Phase 1 — Market Analysis
 Bitcoin price analysis
 Gold price analysis
 SMA / EMA
 Bollinger Bands
 RSI
 MACD
 ATR
 OBV
 Rolling volatility
 Drawdown
 BTC / Gold ratio
 Rolling correlation
 MariaDB integration
Phase 2 — Quantitative Risk Analysis
 Sharpe Ratio
 Sortino Ratio
 Value at Risk
 Conditional VaR
 Risk / Return comparison
 Portfolio analysis
 Efficient Frontier
Phase 3 — Macro Analysis
 DXY
 US 10Y Treasury Yield
 S&P 500
 VIX
 Inflation indicators
 Risk-on / Risk-off regime analysis
Phase 4 — Strategy Research
 Moving Average strategy
 RSI strategy
 Bollinger Band strategy
 Backtesting engine
 Transaction costs
 Monte Carlo simulation
Phase 5 — Interactive Dashboard
 Streamlit dashboard
 Interactive price charts
 Risk dashboard
 BTC / Gold portfolio simulator
 Strategy comparison
 Automated research summary
🔬 Future Research
The next version of this project will investigate whether Bitcoin
and Gold behave differently under different macroeconomic regimes.

Potential extensions include:

DXY
 │
 ├──► Bitcoin
 │
 └──► Gold

US10Y
 │
 ├──► Bitcoin
 │
 └──► Gold

S&P 500 / VIX
 │
 ├──► Bitcoin
 │
 └──► Gold

This would allow the project to move from pure technical analysis
toward a broader quantitative market-regime analysis.

⚠️ Disclaimer
This project is intended for educational and research purposes only.

It does not provide financial advice, investment recommendations,
or predictions of future asset prices.

Past performance does not guarantee future results.

👤 Author
Igrevin

GitHub:

https://github.com/Igrevin/Igrevin

⭐ Project Goal
The ultimate goal of this project is to answer a simple but
important question:

Is Bitcoin really Digital Gold?

Rather than relying on a single indicator, the project evaluates
Bitcoin and Gold across:

Performance → Trend → Momentum → Volatility → Drawdown → Correlation → Risk

The result is intended to provide a reproducible quantitative
framework for comparing these two very different assets.