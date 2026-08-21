## MariaDB 設定

請先建立可接受 TCP 連線的 MariaDB 服務。程式會自動建立資料庫
`btc_gold_db` 和資料表 `btc_gold_data`。

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
