from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_returns(price: pd.Series) -> pd.Series:
    """
    Calculate simple daily returns.
    """
    return price.pct_change().dropna()


def total_return(price: pd.Series) -> float:
    """
    Calculate total return.
    """
    clean_price = price.dropna()

    if len(clean_price) < 2:
        return np.nan

    return clean_price.iloc[-1] / clean_price.iloc[0] - 1


def annualized_return(
    returns: pd.Series,
    trading_days: int = TRADING_DAYS,
) -> float:
    """
    Calculate annualized return from daily returns.
    """
    returns = returns.dropna()

    if len(returns) == 0:
        return np.nan

    cumulative_return = (1 + returns).prod()

    return cumulative_return ** (
        trading_days / len(returns)
    ) - 1


def annualized_volatility(
    returns: pd.Series,
    trading_days: int = TRADING_DAYS,
) -> float:
    """
    Calculate annualized volatility.
    """
    returns = returns.dropna()

    if len(returns) < 2:
        return np.nan

    return returns.std() * np.sqrt(trading_days)


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = TRADING_DAYS,
) -> float:
    """
    Calculate annualized Sharpe ratio.

    risk_free_rate should be expressed as decimal.
    Example:
        4.5% -> 0.045
    """
    returns = returns.dropna()

    if len(returns) < 2:
        return np.nan

    daily_rf = (1 + risk_free_rate) ** (
        1 / trading_days
    ) - 1

    excess_returns = returns - daily_rf

    volatility = excess_returns.std()

    if volatility == 0:
        return np.nan

    return (
        excess_returns.mean()
        / volatility
        * np.sqrt(trading_days)
    )


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = TRADING_DAYS,
) -> float:
    """
    Calculate annualized Sortino ratio.
    """
    returns = returns.dropna()

    if len(returns) == 0:
        return np.nan

    daily_rf = (1 + risk_free_rate) ** (
        1 / trading_days
    ) - 1

    excess_returns = returns - daily_rf

    downside_returns = excess_returns[
        excess_returns < 0
    ]

    if len(downside_returns) == 0:
        return np.nan

    downside_deviation = np.sqrt(
        (downside_returns**2).mean()
    )

    if downside_deviation == 0:
        return np.nan

    return (
        excess_returns.mean()
        / downside_deviation
        * np.sqrt(trading_days)
    )


def drawdown(price: pd.Series) -> pd.Series:
    """
    Calculate drawdown series.
    """
    running_max = price.cummax()

    return price / running_max - 1


def maximum_drawdown(price: pd.Series) -> float:
    """
    Calculate maximum drawdown.
    """
    dd = drawdown(price)

    if dd.empty:
        return np.nan

    return dd.min()


def value_at_risk(
    returns: pd.Series,
    confidence: float = 0.95,
) -> float:
    """
    Historical Value at Risk.

    Example:
        confidence=0.95
        means 5% worst daily returns are below VaR.
    """
    returns = returns.dropna()

    if len(returns) == 0:
        return np.nan

    return returns.quantile(1 - confidence)


def conditional_var(
    returns: pd.Series,
    confidence: float = 0.95,
) -> float:
    """
    Historical Conditional VaR / Expected Shortfall.
    """
    returns = returns.dropna()

    if len(returns) == 0:
        return np.nan

    var = value_at_risk(
        returns,
        confidence,
    )

    tail_losses = returns[returns <= var]

    if tail_losses.empty:
        return np.nan

    return tail_losses.mean()


def calculate_risk_metrics(
    price: pd.Series,
    risk_free_rate: float = 0.0,
) -> dict[str, float]:

    returns = calculate_returns(price)

    return {
        "Total Return": total_return(price),
        "Annualized Return": annualized_return(returns),
        "Annualized Volatility": annualized_volatility(
            returns
        ),
        "Sharpe Ratio": sharpe_ratio(
            returns,
            risk_free_rate,
        ),
        "Sortino Ratio": sortino_ratio(
            returns,
            risk_free_rate,
        ),
        "Maximum Drawdown": maximum_drawdown(
            price
        ),
        "VaR 95%": value_at_risk(
            returns,
            0.95,
        ),
        "CVaR 95%": conditional_var(
            returns,
            0.95,
        ),
    }


def compare_assets(
    prices: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:
    """
    Compare multiple assets.

    prices:
        DataFrame where columns are asset names
        and values are prices.
    """

    metrics = {}

    for column in prices.columns:
        metrics[column] = calculate_risk_metrics(
            prices[column],
            risk_free_rate,
        )

    return pd.DataFrame(metrics).T
