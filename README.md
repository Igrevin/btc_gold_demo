# BTC Gold Demo

## 專案用途

本專案用於擷取 Bitcoin（BTC-USD）與黃金期貨（GC=F）的歷史行情資料，
分析兩種資產的價格趨勢，並以圖表方式呈現布林通道，方便進行市場觀察與
基礎技術分析。

## 專案目的

- 練習使用 Python 取得金融市場歷史資料。
- 計算 Bitcoin 與黃金的 20 日簡單移動平均線（SMA20）。
- 使用布林通道觀察價格、移動平均線及價格波動範圍。
- 將兩種資產的圖表上下排列，方便比較同一期間的價格變化。
- 預留 MariaDB 資料儲存功能，供後續查詢與分析使用。

目前程式預設擷取 2026 年 1 月 1 日至 2026 年 6 月 30 日的每日資料，
並移除沒有收盤價的非交易日資料，以避免影響技術指標計算。

## 相關技術

- **Python 3.12+**：主要開發語言。
- **yfinance**：從 Yahoo Finance 取得 BTC 與黃金期貨行情。
- **pandas**：處理時間序列與行情資料表。
- **ta**：計算 SMA20 與 Bollinger Bands 技術指標。
- **Matplotlib**：繪製 BTC 與 Gold 的上下排列比較圖。
- **MariaDB Connector/Python**：連接 MariaDB，預留行情資料寫入功能。
- **uv**：管理 Python 套件與專案環境。

## 執行方式

請先安裝依賴，再執行主程式：

```powershell
uv sync
uv run python btc_gold_parser.py
```

程式執行後會下載行情資料、輸出 SMA20，並開啟包含兩張布林通道圖的圖表視窗。

## MariaDB 設定

程式中已預留 MariaDB 寫入邏輯。啟用該功能前，請先建立可接受 TCP 連線的
MariaDB 服務。程式會自動建立資料庫 `btc_gold_db` 和資料表
`btc_gold_data`。

預設連線設定如下，也可以用環境變數覆寫：

```text
MARIADB_HOST=127.0.0.1
MARIADB_PORT=3306
MARIADB_USER=root
MARIADB_PASSWORD=
```

PowerShell 範例：

```powershell
$env:MARIADB_USER = "root"
$env:MARIADB_PASSWORD = "your-password"
uv run python btc_gold_parser.py
```

資料表以 `symbol` 和 `trade_date` 作為複合主鍵，重複執行時會更新同一天的資料。
