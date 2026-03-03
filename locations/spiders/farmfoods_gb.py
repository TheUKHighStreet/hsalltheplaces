from chompjs import parse_js_object

from locations.json_blob_spider import JSONBlobSpider
from locations.pipelines.address_clean_up import clean_address


class FarmfoodsGBSpider(JSONBlobSpider):
    name = "farmfoods_gb"
    item_attributes = {"brand": "Farm Foods", "brand_wikidata": "Q5435841"}
    start_urls = ["https://www.farmfoods.co.uk/store-finder.php"]


    def extract_json(self, response):
        js_blob = "[" + response.text.split('"locations": [', 1)[1].split("],", 1)[0] + "]"
        return parse_js_object(js_blob)

    def post_process_item(self, item, response, location):
        item["addr_full"] = clean_address([location["address1"], location["address2"]])
        item["extras"]["ref:google:place_id"] = location.get("placeId")
        item["lat"] = location["coords"]["lat"]
        item["lon"] = location["coords"]["lng"]
        yield item
