"""
psx_kse100_spider.py — KSE-100 constituent scraper via Zyte API browser actions
"""

from datetime import datetime, timezone
import scrapy


class StockItem(scrapy.Item):
    symbol        = scrapy.Field()
    company_name  = scrapy.Field()
    sector        = scrapy.Field()
    ldcp          = scrapy.Field()
    open_price    = scrapy.Field()
    high          = scrapy.Field()
    low           = scrapy.Field()
    current_price = scrapy.Field()
    change        = scrapy.Field()
    change_pct    = scrapy.Field()
    volume        = scrapy.Field()
    scraped_at    = scrapy.Field()


class Kse100Spider(scrapy.Spider):
    name            = "kse100"
    allowed_domains = ["dps.psx.com.pk"]

    _BROWSER_ACTIONS = [
        # 1. Wait for index table links to appear
        {
            "action":   "waitForSelector",
            "selector": {"type": "css", "value": "table tbody tr td a"},
        },
        # 2. Click the KSE100 link
        {
            "action":   "click",
            "selector": {"type": "xpath", "value": "//table//a[normalize-space()='KSE100']"},
        },
        # 3. Wait for the constituent DataTable to render
        {
            "action":   "waitForSelector",
            "selector": {"type": "css", "value": "div.dataTables_wrapper"},
        },
        # 4. Set the length dropdown to 100 — values must be a LIST per Zyte API spec
        {
            "action":   "select",
            "selector": {"type": "css", "value": "div.dataTables_length select"},
            "values":   ["100"],
        },
        # 5. Wait for rows to reload
        {
            "action":   "waitForSelector",
            "selector": {"type": "css", "value": "div.dataTables_wrapper tbody tr"},
        },
    ]

    async def start(self):
        yield scrapy.Request(
            url="https://dps.psx.com.pk/indices",
            callback=self.parse_constituents,
            meta={
                # zyte_api_automap is the correct key per official scrapy-zyte-api docs
                "zyte_api_automap": {
                    "browserHtml": True,
                    "actions":     self._BROWSER_ACTIONS,
                },
            },
        )

    def parse_constituents(self, response):
        scraped_at = datetime.now(timezone.utc).isoformat()

        wrapper = response.css("div.dataTables_wrapper")
        if not wrapper:
            self.logger.error("DataTable wrapper not found. Browser actions may have failed.")
            return

        rows = wrapper.css("tbody tr")
        self.logger.info(f"Found {len(rows)} rows in KSE100 constituent table.")

        for row in rows:
            cols = row.css("td")
            if not cols:
                continue

            def cell(idx):
                return cols[idx].css("::text").get("").strip() if idx < len(cols) else ""

            item = StockItem(
                symbol        = cell(0),
                company_name  = cell(1),
                sector        = cell(2),
                ldcp          = self._to_float(cell(3)),
                open_price    = self._to_float(cell(4)),
                high          = self._to_float(cell(5)),
                low           = self._to_float(cell(6)),
                current_price = self._to_float(cell(7)),
                change        = self._to_float(cell(8)),
                change_pct    = self._clean_pct(cell(9)),
                volume        = self._to_int(cell(10)),
                scraped_at    = scraped_at,
            )

            if item["symbol"]:
                yield item

        next_btn = response.css("div.dataTables_wrapper a.paginate_button.next:not(.disabled)")
        if next_btn:
            self.logger.info("Next page button active — following...")
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_constituents,
                dont_filter=True,
                meta={"zyte_api_automap": {"browserHtml": True}},
            )

    @staticmethod
    def _to_float(value: str):
        try:
            return float(value.replace(",", "").replace("\u2212", "-"))
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _to_int(value: str):
        try:
            return int(value.replace(",", ""))
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _clean_pct(value: str):
        try:
            return float(value.replace("%", "").replace(",", "").replace("\u2212", "-"))
        except (ValueError, AttributeError):
            return None