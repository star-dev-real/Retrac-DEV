import os
import json
from mitmproxy import http
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMON_CORE = os.path.join(BASE_DIR, "Profiles", "common_core.json")
CONFIG = os.path.join(BASE_DIR, "config.json")

class CommonCore:
    def __init__(self):
        self.vbucks = 0
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(CONFIG):
                with open(CONFIG, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.vbucks = config.get("vbucks", 0)
        except:
            pass

    def request(self, flow: http.HTTPFlow) -> None:
        pass

    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url.lower()
        method = flow.request.method

        if "common_core" in url:
            print(f"CommonCore request: {flow.request.method} {flow.request.url}")
            try:
                data = json.loads(flow.response.text)

                with open(COMMON_CORE, "r", encoding="utf-8") as f:
                    common = json.load(f)
                
                
                vbucks = self.vbucks

                if "profileChanges" in data:
                    item_data = {
                        "attributes": {
                            "favorite": False,
                            "item_seen": False,
                            "level": 1,
                            "max_level_bonus": 0,
                            "platform": "Shared",
                            "variants": [],
                            "xp": 0
                        },
                        "quantity": vbucks,
                        "templateId": "Currency:MtxPurchased"
                    }

                    profileChanges = data["profileChanges"]
                    
                    if isinstance(profileChanges, list):
                        profile = profileChanges[0]["profile"]
                    else:
                        profile = profileChanges["profile"]
                    
                    items = profile["items"]

                    for item_id, item_value in items.items():
                        if item_id == "Currency:MtxPurchased" or item_value.get("templateId") == "Currency:MtxPurchased":
                            items[item_id] = item_data
                            break
                    else:
                        new_item_id = str(uuid.uuid4())
                        items[new_item_id] = item_data

                    flow.response = http.Response.make(
                        200,
                        json.dumps(data),
                        {"Content-Type": "application/json"}
                    )

                    with open(COMMON_CORE, "w") as f:
                        json.dump(data, f, indent=4)

                else:
                    print("No profileChanges found in response")
                    
            except Exception as e:
                print(f"Error processing CommonCore response: {e}")