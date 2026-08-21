from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def portfolio_returns(
    returns: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    """
    Calculate portfolio daily returns.

    Example:
        weights = {
            "BTC": 0.5,
            "Gold": 0.5,
        }
    """

    missing_assets = set(weights) - set(returns.columns)

    if missing_assets:
        raise ValueError(
            f"Missing assets: {missing_assets}"
        )

    weight_sum = sum(weights.values())

    if not np.isclose(weight_sum, 1.0):
        raise ValueError(
            "Portfolio weights must sum to 1."
        )

    weight_series = pd.Series(weights)

    return returns[list(weights)].mul(
        weight_series,
        axis=1,
    ).sum(axis=1)


def portfolio_performance(
    returns: pd.DataFrame,
    weights: dict[str, float],
    risk_free_rate: float = 0.0,
) -> dict[str, float]:

    portfolio_ret = portfolio_returns(
        returns,
        weights,
    )

    cumulative_return = (
        (1 + portfolio_ret).prod() - 1
    )

    annualized_return = (
        (1 + portfolio_ret).prod()
        ** (TRADING_DAYS / len(portfolio_ret))
        - 1
    )

    volatility = (
        portfolio_ret.std()
        * np.sqrt(TRADING_DAYS)
    )

    daily_rf = (
        (1 + risk_free_rate)
        ** (1 / TRADING_DAYS)
        - 1
    )

    excess = portfolio_ret - daily_rf

    sharpe = (
        excess.mean()
        / excess.std()
        * np.sqrt(TRADING_DAYS)
        if excess.std() != 0
        else np.nan
    )

    cumulative = (1 + portfolio_ret).cumprod()

    running_max = cumulative.cummax()

    drawdown = cumulative / running_max - 1

    max_drawdown = drawdown.min()

    return {
        "Return": cumulative_return,
        "Annualized Return": annualized_return,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown,
    }


def generate_portfolio_grid(
    returns: pd.DataFrame,
    asset_a: str = "BTC",
    asset_b: str = "Gold",
    step: float = 0.05,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:

    results = []

    weights = np.arange(
        0,
        1 + step,
        step,
    )

    for weight_a in weights:

        weight_b = 1 - weight_a

        portfolio_weight = {
            asset_a: weight_a,
            asset_b: weight_b,
        }

        performance = portfolio_performance(
            returns,
            portfolio_weight,
            risk_free_rate,
        )

        performance["BTC Weight"] = weight_a
        performance["Gold Weight"] = weight_b

        results.append(performance)

    return pd.DataFrame(results)


def random_portfolios(
    returns: pd.DataFrame,
    n_portfolios: int = 5000,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:

    assets = list(returns.columns)

    results = []

    for _ in range(n_portfolios):

        raw_weights = np.random.random(
            len(assets)
        )

        weights = raw_weights / raw_weights.sum()

        weight_dict = dict(
            zip(assets, weights)
        )

        performance = portfolio_performance(
            returns,
            weight_dict,
            risk_free_rate,
        )

        performance.update(weight_dict)

        results.append(performance)

    return pd.DataFrame(results)


def efficient_frontier(
    returns: pd.DataFrame,
    n_portfolios: int = 5000,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:

    return random_portfolios(
        returns,
        n_portfolios,
        risk_free_rate,
    )
