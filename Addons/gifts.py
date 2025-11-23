import json
from mitmproxy import http

class Gifts:
    def request(self, flow: http.HTTPFlow) -> None:
        pass

    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url.lower()
        method = flow.request.method
        if "fortnite/api/storefront/v2/gift/check_eligibility/recipient/" in url:
            try:
                data = json.loads(flow.response.text)

                items = data["item"]
                price = data["price"]

                price[0] = {"basePrice": 0,
            "currencySubType": "",
            "currencyType": "MtxCurrency",
            "dynamicRegularPrice": -1,
            "finalPrice": 0,
            "regularPrice": 0,
            "saleExpiration": "9999-12-31T23:59:59.999Z"}
                
                print(f"Modified gift {items["templateId"]} price to 0 V-Bucks")

                flow.response = http.Response.make(
                    200,
                    json.dumps(data).encode('utf-8'),
                    {"Content-Type": "application/json"}
                )
                
            except Exception as e:
                print(f"Error parsing response for gift eligibility: {e}")