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
	data = downloaded[symbol].copy()
	data = data.dropna(subset=["Close"])
	sma_obj = ta.trend.SMAIndicator(close=data["Close"], window=20)
	data["SMA20"] = sma_obj.sma_indicator()
	market_data[symbol] = data
	print(f"{symbol} 二十日均值:\n{data['SMA20']}")

#save_to_mariadb(market_data)

fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
for axis, (symbol, data) in zip(axes, market_data.items()):
	bb = ta.volatility.BollingerBands(data["Close"], window=20, window_dev=2)
	data["bb_mband"] = bb.bollinger_mavg()
	data["bb_hband"] = bb.bollinger_hband()
	data["bb_lband"] = bb.bollinger_lband()
	data[["Close", "bb_hband", "bb_mband", "bb_lband"]].plot(ax=axis)
	axis.set_title(f"Bollinger Band for {symbol}")
	axis.set_ylabel("value")
	axis.legend()

fig.tight_layout()
plt.show()