# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider

from locations.hours import OpeningHours
from locations.structured_data_spider import StructuredDataSpider


class KFCCASpider(SitemapSpider, StructuredDataSpider):
    name = "kfc_ca"
    item_attributes = {"brand": "KFC", "brand_wikidata": "Q524757", "country": "CA"}
    allowed_domains = ["kfc.ca"]
    sitemap_urls = ["https://www.kfc.ca/sitemap.xml"]
    sitemap_rules = [("/store/", "parse_sd")]
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
    )

    def pre_process_data(self, ld_data, **kwargs):
        oh = OpeningHours()

        for rule in ld_data.get("openingHours", []):
            day, times = rule.split(" ", maxsplit=1)
            start_time, end_time = times.split("-")
            oh.add_range(day, start_time, end_time, time_format="%I:%M %p")

        ld_data["openingHours"] = oh.as_opening_hours()

    def post_process_item(self, item, response, ld_data, **kwargs):
        item["street_address"] = item["addr_full"]
        item["addr_full"] += (
            ", " + response.xpath('//span[@class="postal-code"]/text()').get()
        )

        yield item
