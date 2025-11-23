import json
import os
from mitmproxy import http

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RETRAC = os.path.join(BASE_DIR, "Profiles", "retrac.json")
CONFIG = os.path.join(BASE_DIR, "config.json")
DEBUG = False  

class Athena:
    def __init__(self):
        self.level = 1
        self.load_config()

    def load_config(self):
        try:
            if os.path.exists(CONFIG):
                with open(CONFIG, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.level = config.get("level", 1)
        except:
            pass

    def request(self, flow: http.HTTPFlow) -> None:
        pass
    
    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url.lower()
        method = flow.request.method

        if ("athena" in url or "profileid=athena" in url):
            if "client/queryprofile" in url and method == "POST":
                print(f"Retrac request: {flow.request.method} {flow.request.url}")
                try:
                    with open(RETRAC, "r", encoding="utf-8") as fp:
                        custom_data = json.load(fp)
                    
                    
                    if custom_data and "profileChanges" in custom_data:
                        for change in custom_data["profileChanges"]:
                            if change.get("changeType") == "fullProfileUpdate":
                                profile = change.get("profile", {})
                                stats = profile.get("stats", {})
                                attributes = stats.get("attributes", {})
                                
                                
                                level_fields = ["book_level", "book_xp", "level", "accountLevel"]
                                for field in level_fields:
                                    if field in attributes:
                                        attributes[field] = self.level
                    
                    if custom_data:
                        flow.response = http.Response.make(
                            200,
                            json.dumps(custom_data).encode('utf-8'),
                            {"Content-Type": "application/json"}
                        )
                        print("Applied custom Athena profile data")
                except Exception as e:
                    print(f"Error loading retrac.json: {e}")
                    
            elif "client/setcosmeticlockerslot" in url and method == "POST":
                print(f"Retrac request: {flow.request.method} {flow.request.url}")
                try:
                    request_data = json.loads(flow.request.get_text())
                    response_data = json.loads(flow.response.get_text())
                    
                    if DEBUG:
                        debug_dir = os.path.join(BASE_DIR, "debug_logs")
                        os.makedirs(debug_dir, exist_ok=True)
                    
                    import time
                    timestamp = int(time.time())
                    
                    def process_variant_updates(variant_updates):
                        processed_variants = []
                        if isinstance(variant_updates, list) and len(variant_updates) > 0:
                            print(f"Processing {len(variant_updates)} variant updates")
                            for variant_update in variant_updates:
                                if isinstance(variant_update, dict):
                                    active = variant_update.get("active", "")
                                    active_without_numbers = ''.join([char for char in active if not char.isdigit()])
                                    
                                    owned_variants = []
                                    for i in range(1, 50):
                                        numbered_variant = f"{active_without_numbers}{i}"
                                        owned_variants.append(numbered_variant)
                                    
                                    processed_variants.append({
                                        "channel": variant_update.get("channel", ""),
                                        "active": variant_update.get("active", ""),
                                        "owned": owned_variants
                                    })
                                    print(f"Processed variant: {active} -> owned: {len(owned_variants)} variants")
                        return processed_variants
                    
                    processed_variant_updates = []
                    variant_updates = request_data.get("variantUpdates", {})
                    if variant_updates:
                        processed_variant_updates = process_variant_updates(variant_updates)
                    
                    if DEBUG:
                        debug_data = {
                            "timestamp": timestamp,
                            "url": flow.request.url,
                            "request": request_data,
                            "original_response": response_data,
                            "category": request_data.get("category", ""),
                            "item_to_slot": request_data.get("itemToSlot", ""),
                            "slot_index": request_data.get("slotIndex", 0),
                            "variant_updates": processed_variant_updates if processed_variant_updates else variant_updates
                        }
                    
                    if "errorCode" in response_data:
                        print(f"Server returned error: {response_data.get('errorMessage', 'Unknown error')}")
                        
                        try:
                            with open(RETRAC, "r", encoding="utf-8") as fp:
                                profile_data = json.load(fp)
                            
                            locker_item = request_data.get("lockerItem", "")
                            category = request_data.get("category", "")
                            item_to_slot = request_data.get("itemToSlot", "")
                            slot_index = request_data.get("slotIndex", 0)
                            
                            if "profileChanges" in profile_data and len(profile_data["profileChanges"]) > 0:
                                profile = profile_data["profileChanges"][0].get("profile", {})
                                items = profile.get("items", {})
                                
                                if locker_item in items:
                                    locker_data = items[locker_item]
                                    attributes = locker_data.get("attributes", {})
                                    locker_slots = attributes.get("locker_slots_data", {}).get("slots", {})
                                    
                                    if category in locker_slots:
                                        if slot_index < len(locker_slots[category]["items"]):
                                            locker_slots[category]["items"][slot_index] = item_to_slot
                                        else:
                                            locker_slots[category]["items"] = [item_to_slot]
                                        
                                        if variant_updates and "activeVariants" in locker_slots[category]:
                                            if processed_variant_updates:
                                                locker_slots[category]["activeVariants"] = processed_variant_updates
                                                print(f"Applied {len(processed_variant_updates)} processed variants to locker")
                                        
                                        with open(RETRAC, "w", encoding="utf-8") as fp:
                                            json.dump(profile_data, fp, indent=2)
                                        
                                        success_response = {
                                            "multiUpdate": [],
                                            "notifications": [],
                                            "profileChanges": [
                                                {
                                                    "attributeName": "locker_slots_data",
                                                    "attributeValue": attributes["locker_slots_data"],
                                                    "changeType": "itemAttrChanged",
                                                    "itemId": locker_item
                                                }
                                            ],
                                            "profileChangesBaseRevision": profile_data.get("profileChanges", [{}])[0].get("profile", {}).get("rvn", 0) + 1,
                                            "profileCommandRevision": profile_data.get("profileChanges", [{}])[0].get("profile", {}).get("rvn", 0) + 2,
                                            "profileId": "athena",
                                            "profileRevision": profile_data.get("profileChanges", [{}])[0].get("profile", {}).get("rvn", 0) + 2,
                                            "responseVersion": 1,
                                            "serverTime": "2025-11-21T19:07:36.908Z"
                                        }
                                        
                                        flow.response = http.Response.make(
                                            200,
                                            json.dumps(success_response).encode('utf-8'),
                                            {"Content-Type": "application/json"}
                                        )
                                        print(f"Force-updated locker slot: {category} -> {item_to_slot}")
                                        
                                        if DEBUG:
                                            debug_data["modified_response"] = success_response
                                    else:
                                        print(f"Category {category} not found in locker")
                                else:
                                    print(f"Locker item {locker_item} not found in profile")
                        
                        except Exception as e:
                            print(f"Error force-updating locker: {e}")
                    
                    else:
                        locker_item = request_data.get("lockerItem", "")
                        category = request_data.get("category", "")
                        item_to_slot = request_data.get("itemToSlot", "")
                        slot_index = request_data.get("slotIndex", 0)
                        
                        if "profileChanges" in response_data and len(response_data["profileChanges"]) > 0:
                            profile_change = response_data["profileChanges"][0]
                            
                            if "attributeValue" in profile_change and "slots" in profile_change["attributeValue"]:
                                slots = profile_change["attributeValue"]["slots"]
                                
                                if category in slots:
                                    slots[category]["items"][slot_index] = item_to_slot
                                    
                                    if variant_updates and "activeVariants" in slots[category]:
                                        if processed_variant_updates:
                                            slots[category]["activeVariants"] = processed_variant_updates
                                            print(f"Applied {len(processed_variant_updates)} processed variants to response")
                                    
                                    flow.response = http.Response.make(
                                        200,
                                        json.dumps(response_data).encode('utf-8'),
                                        {"Content-Type": "application/json"}
                                    )
                                    print(f"Updated locker slot: {category} -> {item_to_slot}")
                                    
                                    if DEBUG:
                                        debug_data["modified_response"] = response_data
                    
                    if DEBUG:
                        debug_file = os.path.join(debug_dir, f"setcosmeticlockerslot_{timestamp}.json")
                        with open(debug_file, "w", encoding="utf-8") as debug_fp:
                            json.dump(debug_data, debug_fp, indent=4)
                        
                        print(f"Saved SetCosmeticLockerSlot debug data to: {debug_file}")
                            
                except Exception as e:
                    print(f"Error processing SetCosmeticLockerSlot: {e}")