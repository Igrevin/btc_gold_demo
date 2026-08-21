from __future__ import annotations

import pandas as pd

from .risk import compare_assets
from .portfolio import (
    generate_portfolio_grid,
    efficient_frontier,
)


def prepare_prices(
    btc: pd.Series,
    gold: pd.Series,
) -> pd.DataFrame:

    prices = pd.concat(
        [
            btc.rename("BTC"),
            gold.rename("Gold"),
        ],
        axis=1,
    )

    prices = prices.dropna()

    return prices


def prepare_returns(
    prices: pd.DataFrame,
) -> pd.DataFrame:

    return prices.pct_change().dropna()


def normalized_prices(
    prices: pd.DataFrame,
) -> pd.DataFrame:

    return (
        prices
        / prices.iloc[0]
        * 100
    )


def btc_gold_ratio(
    prices: pd.DataFrame,
) -> pd.Series:

    return (
        prices["BTC"]
        / prices["Gold"]
    )


def rolling_correlation(
    returns: pd.DataFrame,
    window: int = 30,
) -> pd.Series:

    return (
        returns["BTC"]
        .rolling(window)
        .corr(returns["Gold"])
    )


def build_report(
    prices: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> dict:

    returns = prepare_returns(prices)

    risk_metrics = compare_assets(
        prices,
        risk_free_rate,
    )

    portfolio_grid = generate_portfolio_grid(
        returns,
        risk_free_rate=risk_free_rate,
    )

    frontier = efficient_frontier(
        returns,
        risk_free_rate=risk_free_rate,
    )

    return {
        "prices": prices,
        "returns": returns,
        "normalized": normalized_prices(
            prices
        ),
        "btc_gold_ratio": btc_gold_ratio(
            prices
        ),
        "correlation": rolling_correlation(
            returns
        ),
        "risk_metrics": risk_metrics,
        "portfolio_grid": portfolio_grid,
        "efficient_frontier": frontier,
    }
