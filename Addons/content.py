import os
import json
from mitmproxy import http

class Content:
    def request(self, flow: http.HTTPFlow) -> None:
        pass

    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url.lower()
        method = flow.request.method
        if "content/api/pages/fortnite-game/" in url and method == "GET":
            try:
                data = json.loads(flow.response.text)

                if data.get("emergencynotice"):
                    data["emergencynotice"] = {
                        "_title": "emergencynotice",
                        "alwaysShow": True,
                        "lastModified": "0000-00-00T00:00:00.000Z",
                        "news": {
                            "_type": "Battle Royale News",
                            "messages": [
                                {
                                    "hidden": False,
                                    "_type": "CommonUI Emergency Notice Base",
                                    "title": "Welcome to Freetrac!",
                                    "body": "🔥 Made by Star\n🌟 Freetrac is Retrac, but everything is free!\n💎 Please join my Discord: https://discord.gg/AMzza7TXMs",
                                    "spotlight": ""
                                }
                            ]
                        }
                    }

                    flow.response = http.Response.make(
                        200,
                        json.dumps(data),
                        {"Content-Type": "application/json"}
                    )
            except Exception:
                pass