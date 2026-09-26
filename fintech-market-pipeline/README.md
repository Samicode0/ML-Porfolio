# FinTech Market Data Pipeline

A Python ETL pipeline that collects Bitcoin and Ethereum market snapshots from the CoinGecko public API, stores them in MySQL, summarizes recorded prices, and generates price-trend charts.

## What It Does

1. **Extract:** requests USD price, 24-hour trading volume, and 24-hour price change for Bitcoin and Ethereum.
2. **Load:** saves the API response as JSON and inserts one timestamped row per asset into MySQL.
3. **Analyze:** calculates average, minimum, and maximum recorded prices by asset, plus the volume from the last row returned by the query.
4. **Visualize:** plots the stored BTC and ETH prices over time and saves the chart as a PNG.
5. **Schedule:** repeats extraction, loading, and chart generation every 30 seconds.

The scheduler interval is configured in `src/scheduler.py`. This is a learning/portfolio project, not a production trading or financial-advice system.

## Project Structure

```text
fintech-market-pipeline/
|-- data/
|   |-- raw/market_data.json       # Latest API response; overwritten on each extraction
|   `-- processed/price_trend.png  # Generated price chart
|-- src/
|   |-- extract.py                 # CoinGecko API client
|   |-- load.py                    # MySQL schema setup and JSON loader
|   |-- analyse.py                 # Database summary
|   |-- plot.py                    # Price chart generation
|   `-- scheduler.py               # Repeated extract-load-plot run
|-- .env.example
|-- requirements.txt
`-- README.md
```

## Requirements

- Python 3.9 or newer
- A running MySQL server and a MySQL user that can create databases and tables
- Network access to `api.coingecko.com`

The pipeline uses the CoinGecko public simple-price endpoint; no API key is configured in this project.

## Setup

Run these commands from the `fintech-market-pipeline` directory. In PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `.env` in the project root using `.env.example` as a reference, then set the credentials for your MySQL server:

```dotenv
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
```

The current scripts use the database name `fintech_db` directly. Although `.env.example` includes `MYSQL_DATABASE`, changing that variable alone will not change the database used by the code.

## Run the Pipeline

Bootstrap the database and create an initial market snapshot. This also creates `fintech_db` and its `market_logs` table:

```powershell
python src/extract.py
python src/load.py
```

Run an individual task:

```powershell
python src/extract.py   # Fetch and save data/raw/market_data.json
python src/load.py      # Insert the JSON snapshot into MySQL
python src/analyse.py   # Print grouped price summary
python src/plot.py      # Save data/processed/price_trend.png
```

Start the recurring pipeline after the database has been initialized:

```powershell
python src/scheduler.py
```

Stop the scheduler with `Ctrl+C`. Each successful cycle adds BTC and ETH records to MySQL. Re-running the loader manually also adds rows; it does not replace existing history.

## Database

The loader creates a `fintech_db.market_logs` table with these fields:

| Column | Description |
| --- | --- |
| `id` | Auto-incrementing row identifier |
| `asset_symbol` | `BTC` or `ETH` |
| `price_usd` | USD price at collection time |
| `volume_24h` | 24-hour trading volume in USD |
| `change_24h` | 24-hour price change reported by CoinGecko |
| `recorded_at` | MySQL timestamp assigned when the row is inserted |

## Generated Output

- `data/raw/market_data.json` contains only the most recently fetched API response. Historical snapshots live in MySQL.
- `data/processed/price_trend.png` contains separate BTC and ETH price charts built from database history.
- `src/analyse.py` prints average, minimum, and maximum recorded price by asset. Its volume field is taken from the last row returned by the database query, which currently does not specify a sort order.

## Troubleshooting

- **MySQL connection or unknown database error:** confirm the server is running and `.env` credentials are correct. Run `python src/load.py` once to create the database and table before starting the scheduler.
- **Missing JSON file or keys:** run `python src/extract.py` and check that the API request succeeded and `data/raw/market_data.json` contains `bitcoin` and `ethereum` objects with `usd`, `usd_24h_vol`, and `usd_24h_change` values.
- **Import errors:** activate the virtual environment and install `requirements.txt` from the project root.
- **API request failures:** verify network access and try again later; the extractor reports request errors, but the loader expects a valid JSON file.

## Dependencies

Dependencies are listed in [`requirements.txt`](requirements.txt): `requests`, `mysql-connector-python`, `python-dotenv`, `pandas`, `matplotlib`, and `schedule`.
