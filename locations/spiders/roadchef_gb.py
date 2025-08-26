import json
from typing import Iterable

from scrapy.http import Response, Request

from locations.categories import Categories, apply_category
from locations.hours import OpeningHours
from locations.items import Feature
from locations.json_blob_spider import JSONBlobSpider
from locations.pipelines.address_clean_up import merge_address_lines


class RoadchefGBSpider(JSONBlobSpider):
    name = "roadchef_gb"
    item_attributes = {
        "brand_wikidata": "Q7339582",
        "brand": "Roadchef",
    }
    start_urls = ["https://www.roadchef.com/motorway-services"]

    def extract_json(self, response: Response) -> dict | list[dict]:
        data_raw = response.xpath("//div[@id='app']/wrapper/@*[name()=':template']").get()
        features_dict = json.loads(data_raw)
        return features_dict["value"]["items"]

    def pre_process_data(self, feature: dict) -> None:
        feature["name"]=feature.pop("title")
        feature["id"]=feature["url"].replace("/motorway-services/","")

    def post_process_item(self, item: Feature, response: Response, feature: dict) -> Iterable[Feature]:
        item["branch"] = item.pop("name")
        item["website"] = "https://www.roadchef.com" + feature["url"]
        item.pop("email", None)
        item.pop("facebook", None)
        item.pop("twitter", None)
        item["lat"],item["lon"]=feature["position"]["lat"],feature["position"]["lng"]
        yield Request(url=item["website"], meta={"item": item}, callback=self.parse_details)

    def parse_details(self, response: Response) -> Iterable[Feature]:
        item = response.meta["item"]
        details = json.loads(response.xpath("//div[@id='app']/wrapper/@*[name()=':page-builder']").get())
        features = json.loads(response.xpath("//div[@id='app']/wrapper/@*[name()=':template']").get())
        item["street_address"] = details[0]["value"]["address"]
        item["phone"] = details[0]["value"]["telephone"]
        apply_category(Categories.FUEL_STATION, item)
        yield item
