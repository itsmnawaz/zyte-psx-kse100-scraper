# PSX KSE-100 Scrapy Spider (Zyte API)

Scrapes all **100 KSE-100 constituent stocks** from the Pakistan Stock Exchange
Data Portal using Scrapy + Zyte API browser rendering.

## Output

`kse100_stocks.json` — one object per stock:

```json
[
  {
    "symbol":        "ENGRO",
    "company_name":  "Engro Corporation Limited",
    "sector":        "Fertilizer",
    "ldcp":          312.45,
    "open_price":    313.00,
    "high":          315.80,
    "low":           310.10,
    "current_price": 311.20,
    "change":        -1.25,
    "change_pct":    -0.40,
    "volume":        2345678,
    "scraped_at":    "2026-05-04T10:30:00+00:00"
  },
  ...
]
```

## Prerequisites

- Python 3.9+
- A [Zyte API](https://www.zyte.com/zyte-api/) account and key

## Setup

```bash
# 1. Clone / unzip the project
cd zyte-psx-kse100-scraper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Zyte API key:
cp .env.example .env

Then add the key in env for ZYTE_API_KEY
```

## Run

```bash
# From the zyte-psx-kse100-scraper/ directory:
scrapy crawl kse100
```

or

```bash
# From the zyte-psx-kse100-scraper/ directory:
python -m scrapy crawl kse100
```

Output is written to **`kse100_stocks.json`** in the current directory.

## How It Works

The PSX indices page is fully JavaScript-rendered. The spider uses Zyte API's
**browser actions** to automate the following sequence in a real browser:

| Step | Action                                                       |
| ---- | ------------------------------------------------------------ |
| 1    | Load `https://dps.psx.com.pk/indices` with JS enabled        |
| 2    | Wait for the indices table to appear                         |
| 3    | Click the **KSE100** row link                                |
| 4    | Wait for the DataTable of constituents to render             |
| 5    | Set the DataTable length dropdown to **100** (show all rows) |
| 6    | Wait for all 100 rows to load                                |
| 7    | Extract every row and yield a `StockItem`                    |

The spider also includes a safety-net paginator in case fewer than 100 rows
are shown and a "Next" button is still active.

## Fields Extracted

| Field           | Description                  |
| --------------- | ---------------------------- |
| `symbol`        | Stock ticker (e.g. ENGRO)    |
| `company_name`  | Full listed company name     |
| `sector`        | PSX sector classification    |
| `ldcp`          | Last Day Closing Price (PKR) |
| `open_price`    | Today's opening price        |
| `high`          | Intraday high                |
| `low`           | Intraday low                 |
| `current_price` | Latest traded price          |
| `change`        | Absolute price change        |
| `change_pct`    | Percentage price change      |
| `volume`        | Shares traded today          |
| `scraped_at`    | UTC timestamp of the scrape  |
