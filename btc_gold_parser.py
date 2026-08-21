import math
import os
from pprint import pprint

import matplotlib.pyplot as plt
import mariadb
import ta
import yfinance as yf


SYMBOLS = ("BTC-USD", "GC=F")
START_DATE = "2026-01-01"
END_DATE = "2026-07-01"

'''#資料已寫入
def as_db_value(value):
	if value is None:
		return None
	if isinstance(value, float) and math.isnan(value):
		return None
	return value.item() if hasattr(value, "item") else value


def save_to_mariadb(market_data):
	connection_config = {
		"host": os.getenv("MARIADB_HOST", "localhost"),
		"port": int(os.getenv("MARIADB_PORT", "3306")),
		"user": os.getenv("MARIADB_USER", "root"),
		"password": os.getenv("MARIADB_PASSWORD", ""),
	}

	connection = mariadb.connect(**connection_config)
	cursor = connection.cursor()
	try:
		cursor.execute("CREATE DATABASE IF NOT EXISTS btc_gold_db")
		connection.select_db("btc_gold_db")
		cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS btc_gold_data (
				symbol VARCHAR(10) NOT NULL,
				trade_date DATE NOT NULL,
				open_price DOUBLE,
				high_price DOUBLE,
				low_price DOUBLE,
				close_price DOUBLE,
				adj_close DOUBLE,
				volume BIGINT,
				sma20 DOUBLE,
				PRIMARY KEY (symbol, trade_date)
			)
			"""
		)

		rows = []
		for symbol, data in market_data.items():
			for trade_date, values in data.iterrows():
				rows.append(
					(
						symbol,
						trade_date.date(),
						as_db_value(values.get("Open")),
						as_db_value(values.get("High")),
						as_db_value(values.get("Low")),
						as_db_value(values.get("Close")),
						as_db_value(values.get("Adj Close")),
						as_db_value(values.get("Volume")),
						as_db_value(values.get("SMA20")),
					)
				)

		cursor.executemany(
			"""
			INSERT INTO btc_gold_data
				(symbol, trade_date, open_price, high_price, low_price,
				 close_price, adj_close, volume, sma20)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
			ON DUPLICATE KEY UPDATE
				open_price = VALUES(open_price),
				high_price = VALUES(high_price),
				low_price = VALUES(low_price),
				close_price = VALUES(close_price),
				adj_close = VALUES(adj_close),
				volume = VALUES(volume),
				sma20 = VALUES(sma20)
			""",
			rows,
		)
		connection.commit()
		print(f"已寫入 {len(rows)} 筆資料至 btc_gold_db.btc_gold_data")
	finally:
		cursor.close()
		connection.close()
'''

downloaded = yf.download(
	list(SYMBOLS),
	start=START_DATE,
	end=END_DATE,
	interval="1d",
	group_by="ticker",
	auto_adjust=False,
)
pprint(downloaded)

market_data = {}
for symbol in SYMBOLS:
	data = downloaded[symbol].copy().dropna(subset=["Close"])
	data["SMA20"] = ta.trend.SMAIndicator(
		close=data["Close"], window=20
	).sma_indicator()
	data["SMA50"] = ta.trend.SMAIndicator(
		close=data["Close"], window=50
	).sma_indicator()
	data["SMA200"] = ta.trend.SMAIndicator(
		close=data["Close"], window=200
	).sma_indicator()
	data["EMA20"] = ta.trend.EMAIndicator(
		close=data["Close"], window=20
	).ema_indicator()
	data["RSI14"] = ta.momentum.RSIIndicator(
		close=data["Close"], window=14
	).rsi()
	macd = ta.trend.MACD(close=data["Close"])
	data["MACD"] = macd.macd()
	data["MACD_signal"] = macd.macd_signal()
	data["MACD_diff"] = macd.macd_diff()
	data["ATR14"] = ta.volatility.AverageTrueRange(
		high=data["High"], low=data["Low"], close=data["Close"], window=14
	).average_true_range()
	data["Return"] = data["Close"].pct_change()
	data["Volatility30D"] = data["Return"].rolling(30).std() * math.sqrt(252)
	data["OBV"] = ta.volume.OnBalanceVolumeIndicator(
		close=data["Close"], volume=data["Volume"]
	).on_balance_volume()
	bb = ta.volatility.BollingerBands(data["Close"], window=20, window_dev=2)
	data["Bollinger_middle"] = bb.bollinger_mavg()
	data["Bollinger_upper"] = bb.bollinger_hband()
	data["Bollinger_lower"] = bb.bollinger_lband()
	data["Drawdown"] = data["Close"] / data["Close"].cummax() - 1
	market_data[symbol] = data
	print(f"{symbol} 指標計算完成，共 {len(data)} 筆交易日資料")

# save_to_mariadb(market_data)

fig, price_axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
for axis, (symbol, data) in zip(price_axes, market_data.items()):
	data[[
		"Close", "Bollinger_upper", "Bollinger_middle", "Bollinger_lower",
		"SMA20", "SMA50", "EMA20",
	]].plot(ax=axis)
	axis.set_title(f"{symbol} Price, Bollinger Bands and Moving Averages")
	axis.set_ylabel("Price")
	axis.legend(loc="best")

fig.suptitle("Bitcoin and Gold Technical Analysis", fontsize=18)
fig.tight_layout(rect=(0, 0, 1, 0.98))

indicator_fig, indicator_axes = plt.subplots(
	5, 2, figsize=(14, 16), sharex=True, layout="constrained"
)
for column, (symbol, data) in enumerate(market_data.items()):
	data["RSI14"].plot(ax=indicator_axes[0, column], color="tab:purple")
	indicator_axes[0, column].axhline(70, color="red", linestyle="--", linewidth=1)
	indicator_axes[0, column].axhline(30, color="green", linestyle="--", linewidth=1)
	indicator_axes[0, column].set_title(f"{symbol} RSI (14)")
	indicator_axes[0, column].set_ylabel("RSI")
	indicator_axes[0, column].set_ylim(0, 100)

	macd_axis = indicator_axes[1, column]
	data[["MACD", "MACD_signal"]].plot(ax=macd_axis)
	macd_axis.bar(
		data.index,
		data["MACD_diff"].fillna(0),
		width=0.8,
		alpha=0.25,
		color="tab:gray",
		label="MACD histogram",
	)
	macd_axis.set_title(f"{symbol} MACD")
	macd_axis.set_ylabel("MACD")
	macd_axis.legend(loc="upper right")

	(data["Volatility30D"] * 100).plot(
		ax=indicator_axes[2, column], color="tab:orange"
	)
	indicator_axes[2, column].set_title(f"{symbol} 30-Day Annualized Volatility")
	indicator_axes[2, column].set_ylabel("Percent")

	data["ATR14"].plot(ax=indicator_axes[3, column], color="tab:brown")
	indicator_axes[3, column].set_title(f"{symbol} ATR (14)")
	indicator_axes[3, column].set_ylabel("ATR")

	data["OBV"].plot(ax=indicator_axes[4, column], color="tab:cyan")
	indicator_axes[4, column].set_title(f"{symbol} On-Balance Volume")
	indicator_axes[4, column].set_ylabel("OBV")
	indicator_axes[4, column].set_xlabel("")

indicator_fig.suptitle("Bitcoin and Gold Indicator Analysis", fontsize=18)
indicator_fig.supxlabel("Date")

comparison = market_data["BTC-USD"]["Close"].rename("BTC-USD").to_frame()
comparison["GC=F"] = market_data["GC=F"]["Close"]
comparison = comparison.dropna()
comparison["BTC_normalized"] = comparison["BTC-USD"] / comparison["BTC-USD"].iloc[0] * 100
comparison["Gold_normalized"] = comparison["GC=F"] / comparison["GC=F"].iloc[0] * 100
comparison["BTC_Gold_Ratio"] = comparison["BTC-USD"] / comparison["GC=F"]
comparison["BTC_Return"] = comparison["BTC-USD"].pct_change()
comparison["Gold_Return"] = comparison["GC=F"].pct_change()
comparison["Rolling_Correlation_30D"] = comparison["BTC_Return"].rolling(30).corr(
	comparison["Gold_Return"]
)

comparison_fig, comparison_axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True)
comparison[["BTC_normalized", "Gold_normalized"]].plot(ax=comparison_axes[0, 0])
comparison_axes[0, 0].set_title("Normalized Price (Start = 100)")
comparison_axes[0, 0].set_ylabel("Index")

comparison["BTC_Gold_Ratio"].plot(ax=comparison_axes[0, 1], color="tab:orange")
comparison_axes[0, 1].set_title("BTC / Gold Price Ratio")
comparison_axes[0, 1].set_ylabel("Ratio")

comparison["Rolling_Correlation_30D"].plot(ax=comparison_axes[1, 0], color="tab:purple")
comparison_axes[1, 0].axhline(0, color="black", linewidth=1)
comparison_axes[1, 0].set_title("30-Day Return Correlation")
comparison_axes[1, 0].set_ylabel("Correlation")
comparison_axes[1, 0].set_ylim(-1, 1)

comparison[["BTC-USD", "GC=F"]].apply(
	lambda prices: prices / prices.cummax() - 1
).plot(ax=comparison_axes[1, 1])
comparison_axes[1, 1].set_title("Drawdown Comparison")
comparison_axes[1, 1].set_ylabel("Drawdown")

comparison_fig.suptitle("Bitcoin vs. Gold Comparison", fontsize=18)
comparison_fig.tight_layout(rect=(0, 0, 1, 0.97))
plt.show()