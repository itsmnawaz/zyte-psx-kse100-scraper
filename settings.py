import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "zyte-psx-kse100-scraper"

SPIDER_MODULES = ["spiders"]
NEWSPIDER_MODULE = "spiders"

# ---------------------------------------------------------------------------
# Zyte API settings
# ---------------------------------------------------------------------------
# Set your Zyte API key here or via environment variable ZYTE_API_KEY
ZYTE_API_KEY = os.environ.get("ZYTE_API_KEY", "")

DOWNLOAD_HANDLERS = {
    "http":  "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
    "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
}

SPIDER_MIDDLEWARES = {
    "scrapy_zyte_api.ScrapyZyteAPISpiderMiddleware": 100,
}

REQUEST_FINGERPRINTER_CLASS = "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# ---------------------------------------------------------------------------
# Polite crawl settings
# ---------------------------------------------------------------------------
ROBOTSTXT_OBEY   = False          # PSX blocks robots.txt; data is public
DOWNLOAD_DELAY   = 2
AUTOTHROTTLE_ENABLED    = True
AUTOTHROTTLE_MAX_DELAY  = 10
CONCURRENT_REQUESTS     = 1       # sequential – one index page

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
FEEDS = {
    "kse100_stocks.json": {
        "format":   "json",
        "encoding": "utf8",
        "indent":   2,
        "overwrite": True,
    }
}

LOG_LEVEL = "INFO"