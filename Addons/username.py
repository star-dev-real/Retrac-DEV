import os
import json
from mitmproxy import http

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(BASE_DIR, "config.json")

class Username:
    def __init__(self):
        self.username = "Player"
        self.display_name_suffix = "(Freetrac)"
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(CONFIG):
                with open(CONFIG, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.username = config.get("username", "Player")
                self.display_name_suffix = config.get("display_name_suffix", "(Freetrac)")
        except:
            pass

    def request(self, flow: http.HTTPFlow) -> None:
        pass

    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url
        method = flow.request.method
        
        if "account/api/oauth/token" in url:
            try:
                original_data = json.loads(flow.response.text)
                
                
                modified_data = {
                    "access_token": original_data.get("access_token", "eg1~eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6ZmFsc2UsImFtIjoicmVmcmVzaF90b2tlbiIsImNyZWF0aW9uX2RhdGUiOiIyMDI1LTExLTIzVDE2OjE2OjUzLjA4MVoiLCJleHAiOjE3NjY1ODk0MTMsInVpZCI6InlvOXYxeXdma2QzdndzbDFjbzhlZnljMiIsInVzZXJuYW1lIjoidGRkdDk5OSIsInV1aWQiOiJ5bzl2MXl3ZmtkM3Z3c2wxY284ZWZ5YzIifQ.9orXToY4k-kJGPqe0PANPdW_v05hwKM4_5_m09WXfYQ"),
                    "account_id": original_data.get("account_id", "yox9v1ywfkd3vws1co8efyc2"),
                    "app": original_data.get("app", "fortnite"),
                    "client_id": original_data.get("client_id", "ec6846f24d1b4b4083e204f36d8c9f20"),
                    "client_service": original_data.get("client_service", "fortnite"),
                    "device_id": original_data.get("device_id", "5f5bb973-8e1f-4d17-8a6b-4dcb3f3f2f5c"),
                    "display_name": f"{self.username} {self.display_name_suffix}",
                    "expires_at": original_data.get("expires_at", "2025-11-24T16:16:57.009Z"),
                    "expires_in": original_data.get("expires_in", 86200),
                    "internal_client": original_data.get("internal_client", True),
                    "product_id": original_data.get("product_id", "fn"),
                    "refresh_expires": original_data.get("refresh_expires", 1209600),
                    "refresh_expires_at": original_data.get("refresh_expires_at", "2025-11-24T16:16:57.009Z"),
                    "refresh_token": original_data.get("refresh_token", "eg1~eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6ZmFsc2UsImFtIjoicmVmcmVzaF90b2tlbiIsImNyZWF0aW9uX2RhdGUiOiIyMDI1LTExLTIzVDE2OjE2OjUzLjA4MVoiLCJleHAiOjE3NjY1ODk0MTMsInVpZCI6InlvOXYxeXdma2QzdndzbDFjbzhlZnljMiIsInVzZXJuYW1lIjoidGRkdDk5OSIsInV1aWQiOiJ5bzl2MXl3ZmtkM3Z3c2wxY284ZWZ5YzIifQ.9orXToY4k-kJGPqe0PANPdW_v05hwKM4_5_m09WXfYQ"),
                    "sandbox_id": original_data.get("sandbox_id", "fn"),
                    "token_type": original_data.get("token_type", "bearer")
                }
                
                flow.response = http.Response.make(
                    200,
                    json.dumps(modified_data).encode('utf-8'),
                    {"Content-Type": "application/json"}
                )
                print(f"Modified username to: {self.username} {self.display_name_suffix}")
                
            except Exception as e:
                print(f"Error parsing response for username (oauth/token): {e}")

        elif "account/api/public/account" in url:
            try:
                
                response_data = json.loads(flow.response.text)
                
                if isinstance(response_data, list):
                    
                    for account in response_data:
                        if "displayName" in account:
                            account["displayName"] = f"{self.username} {self.display_name_suffix}"
                else:
                    
                    if "displayName" in response_data:
                        response_data["displayName"] = f"{self.username} {self.display_name_suffix}"
                
                flow.response = http.Response.make(
                    200,
                    json.dumps(response_data).encode('utf-8'),
                    {"Content-Type": "application/json"}
                )
                print(f"Modified public account display name to: {self.username} {self.display_name_suffix}")
                
            except Exception as e:
                print(f"Error parsing response for username (public/account): {e}")