from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def moving_average_strategy(
    price: pd.Series,
    fast: int = 20,
    slow: int = 50,
) -> pd.DataFrame:

    df = pd.DataFrame(index=price.index)

    df["Price"] = price

    df["Fast_MA"] = (
        price.rolling(fast).mean()
    )

    df["Slow_MA"] = (
        price.rolling(slow).mean()
    )

    df["Signal"] = (
        df["Fast_MA"] > df["Slow_MA"]
    ).astype(int)

    df["Market_Return"] = price.pct_change()

    # Signal is shifted by one day to avoid look-ahead bias.
    df["Strategy_Return"] = (
        df["Signal"].shift(1)
        * df["Market_Return"]
    )

    df["Buy_Hold"] = (
        1 + df["Market_Return"]
    ).cumprod()

    df["Strategy_Equity"] = (
        1 + df["Strategy_Return"].fillna(0)
    ).cumprod()

    return df


def rsi_strategy(
    price: pd.Series,
    period: int = 14,
    oversold: float = 30,
    overbought: float = 70,
) -> pd.DataFrame:

    delta = price.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (
        100 / (1 + rs)
    )

    df = pd.DataFrame(index=price.index)

    df["Price"] = price
    df["RSI"] = rsi

    df["Signal"] = np.select(
        [
            rsi < oversold,
            rsi > overbought,
        ],
        [
            1,
            0,
        ],
        default=np.nan,
    )

    df["Signal"] = (
        df["Signal"]
        .ffill()
        .fillna(0)
    )

    df["Return"] = price.pct_change()

    df["Strategy_Return"] = (
        df["Signal"].shift(1)
        * df["Return"]
    )

    df["Equity"] = (
        1 + df["Strategy_Return"].fillna(0)
    ).cumprod()

    return df


def bollinger_strategy(
    price: pd.Series,
    window: int = 20,
    num_std: float = 2,
) -> pd.DataFrame:

    middle = price.rolling(window).mean()

    std = price.rolling(window).std()

    upper = middle + num_std * std

    lower = middle - num_std * std

    df = pd.DataFrame(index=price.index)

    df["Price"] = price
    df["Middle"] = middle
    df["Upper"] = upper
    df["Lower"] = lower

    # Mean-reversion strategy:
    #
    # Below lower band -> long
    # Above upper band -> cash

    df["Signal"] = np.where(
        price < lower,
        1,
        np.where(
            price > upper,
            0,
            np.nan,
        ),
    )

    df["Signal"] = (
        pd.Series(
            df["Signal"],
            index=df.index,
        )
        .ffill()
        .fillna(0)
    )

    df["Return"] = price.pct_change()

    df["Strategy_Return"] = (
        df["Signal"].shift(1)
        * df["Return"]
    )

    df["Equity"] = (
        1 + df["Strategy_Return"].fillna(0)
    ).cumprod()

    return df


def backtest_statistics(
    strategy_returns: pd.Series,
) -> dict[str, float]:

    returns = strategy_returns.dropna()

    if returns.empty:
        return {}

    equity = (
        1 + returns
    ).cumprod()

    total_return = equity.iloc[-1] - 1

    annualized_return = (
        equity.iloc[-1]
        ** (TRADING_DAYS / len(returns))
        - 1
    )

    volatility = (
        returns.std()
        * np.sqrt(TRADING_DAYS)
    )

    sharpe = (
        returns.mean()
        / returns.std()
        * np.sqrt(TRADING_DAYS)
        if returns.std() != 0
        else np.nan
    )

    running_max = equity.cummax()

    drawdown = (
        equity / running_max - 1
    )

    max_drawdown = drawdown.min()

    winning_days = (
        returns > 0
    ).sum()

    trading_days = (
        returns != 0
    ).sum()

    win_rate = (
        winning_days / trading_days
        if trading_days > 0
        else np.nan
    )

    return {
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_drawdown,
        "Win Rate": win_rate,
        "Trading Days": trading_days,
    }
