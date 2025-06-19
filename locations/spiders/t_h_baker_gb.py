#this give 403 errors for the stores page

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from locations.structured_data_spider import StructuredDataSpider


class THBakerGBSpider(StructuredDataSpider):
    name = "t_h_baker_gb"
    item_attributes = {"brand": "T H Baker", "brand_wikidata": "Q28406430"}
    start_urls = [
        "https://www.thbaker.co.uk/stores/",
    ]
    rules = [
        Rule(LinkExtractor(r"https://www.thbaker.co.uk/stores/([-\w]+)$"), "parse"),
    ]

