from scrapy.spiders import SitemapSpider, CrawlSpider

from locations.items import Feature
from locations.structured_data_spider import StructuredDataSpider


class SmashburgerGBSpider(SitemapSpider, StructuredDataSpider):
    name = "smashburger_gb"
    item_attributes = {"brand": "Smashburger", "brand_wikidata": "Q17061332"}
    sitemap_urls = ["https://smashburger.co.uk/location-sitemap.xml"]
    sitemap_rules = [(r"/locations/[-\w]+", "parse")]
    wanted_types = ["Website"]
