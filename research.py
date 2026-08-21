from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.btd_gold_demo.analysis import (
    build_report,
    prepare_prices,
)
from src.btd_gold_demo.backtest import (
    moving_average_strategy,
    rsi_strategy,
    bollinger_strategy,
)


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_risk_metrics(
    metrics: pd.DataFrame,
) -> None:

    metrics.to_csv(
        OUTPUT_DIR / "risk_metrics.csv"
    )

    print("\n=== Risk Metrics ===")
    print(metrics.round(4))


def plot_normalized_performance(
    normalized: pd.DataFrame,
) -> None:

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    for column in normalized.columns:
        ax.plot(
            normalized.index,
            normalized[column],
            label=column,
            linewidth=2,
        )

    ax.axhline(
        100,
        color="gray",
        linestyle="--",
        alpha=0.5,
    )

    ax.set_title(
        "Bitcoin vs Gold — Normalized Performance"
    )

    ax.set_ylabel(
        "Normalized Value"
    )

    ax.legend()

    ax.grid(
        alpha=0.2
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "normalized_performance.png",
        dpi=200,
    )

    plt.close(fig)


def plot_drawdown(
    prices: pd.DataFrame,
) -> None:

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    for column in prices.columns:

        running_max = (
            prices[column]
            .cummax()
        )

        drawdown = (
            prices[column]
            / running_max
            - 1
        )

        ax.plot(
            drawdown.index,
            drawdown,
            label=column,
        )

    ax.axhline(
        0,
        color="black",
        linewidth=0.8,
    )

    ax.set_title(
        "Bitcoin vs Gold — Drawdown"
    )

    ax.set_ylabel(
        "Drawdown"
    )

    ax.legend()

    ax.grid(
        alpha=0.2
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "drawdown.png",
        dpi=200,
    )

    plt.close(fig)


def plot_correlation(
    correlation: pd.Series,
) -> None:

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        correlation.index,
        correlation,
        color="purple",
        linewidth=2,
    )

    ax.axhline(
        0,
        color="black",
        linewidth=0.8,
    )

    ax.axhline(
        0.5,
        color="green",
        linestyle="--",
        alpha=0.5,
    )

    ax.axhline(
        -0.5,
        color="red",
        linestyle="--",
        alpha=0.5,
    )

    ax.set_ylim(
        -1,
        1,
    )

    ax.set_title(
        "BTC / Gold — 30D Rolling Correlation"
    )

    ax.set_ylabel(
        "Correlation"
    )

    ax.grid(
        alpha=0.2
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "rolling_correlation.png",
        dpi=200,
    )

    plt.close(fig)


def plot_portfolio(
    portfolio_grid: pd.DataFrame,
) -> None:

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        portfolio_grid["Volatility"],
        portfolio_grid["Return"],
        marker="o",
        linewidth=2,
    )

    ax.set_xlabel(
        "Annualized Volatility"
    )

    ax.set_ylabel(
        "Total Return"
    )

    ax.set_title(
        "BTC / Gold Portfolio Risk-Return"
    )

    ax.grid(
        alpha=0.2
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "portfolio_risk_return.png",
        dpi=200,
    )

    plt.close(fig)


def run_backtests(
    btc_price: pd.Series,
) -> None:

    ma = moving_average_strategy(
        btc_price
    )

    rsi = rsi_strategy(
        btc_price
    )

    bollinger = bollinger_strategy(
        btc_price
    )

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        ma.index,
        ma["Buy_Hold"],
        label="Buy & Hold",
        linewidth=2,
    )

    ax.plot(
        ma.index,
        ma["Strategy_Equity"],
        label="MA Strategy",
    )

    ax.plot(
        rsi.index,
        rsi["Equity"],
        label="RSI Strategy",
    )

    ax.plot(
        bollinger.index,
        bollinger["Equity"],
        label="Bollinger Strategy",
    )

    ax.set_title(
        "BTC Strategy Backtest"
    )

    ax.set_ylabel(
        "Portfolio Value"
    )

    ax.legend()

    ax.grid(
        alpha=0.2
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "backtest_comparison.png",
        dpi=200,
    )

    plt.close(fig)


def main():

    # ------------------------------------------------
    # Replace this section with your existing data
    # loading function.
    # ------------------------------------------------

    btc = pd.read_csv(
        "data/btc.csv",
        index_col=0,
        parse_dates=True,
    )["Close"]

    gold = pd.read_csv(
        "data/gold.csv",
        index_col=0,
        parse_dates=True,
    )["Close"]

    prices = prepare_prices(
        btc,
        gold,
    )

    report = build_report(
        prices,
        risk_free_rate=0.04,
    )

    save_risk_metrics(
        report["risk_metrics"]
    )

    plot_normalized_performance(
        report["normalized"]
    )

    plot_drawdown(
        report["prices"]
    )

    plot_correlation(
        report["correlation"]
    )

    plot_portfolio(
        report["portfolio_grid"]
    )

    run_backtests(
        prices["BTC"]
    )

    print(
        "\nResearch completed."
    )

    print(
        f"Output directory: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()
