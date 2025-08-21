import json
import uuid
import os
import time
import asyncio
import importlib
import requests
from mitmproxy import http, proxy, options
from mitmproxy.tools.dump import DumpMaster
import sys
from pypresence import Presence
import threading
import hashlib
from colorama import Fore, Style,  init
import subprocess
import ssl
import certifi
from pathlib import Path
import shutil

init(autoreset=True)

class Retrac:
    def __init__(self):
        self.title = """.______       _______ .___________..______          ___       ______     _______   ___________    ____ 
|   _  \     |   ____||           ||   _  \        /   \     /      |   |       \ |   ____\   \  /   / 
|  |_)  |    |  |__   `---|  |----`|  |_)  |      /  ^  \   |  ,----'   |  .--.  ||  |__   \   \/   /  
|      /     |   __|      |  |     |      /      /  /_\  \  |  |        |  |  |  ||   __|   \      /   
|  |\  \----.|  |____     |  |     |  |\  \----./  _____  \ |  `----.   |  '--'  ||  |____   \    /    
| _| `._____||_______|    |__|     | _| `._____/__/     \__\ \______|   |_______/ |_______|   \__/     
                                                                                                       
"""
        self.name = "Retrac"
        self.author = "Star"
        self.version = "1.0.0"
        self.discord = "https://discord.gg/retrac"
        self.vbucks = 0
        self.level = 0
        self.all_cosmetics = False
        self.custom_shop = False
        self.custom_name
        self.cosmetics = []
        self.accountID = None
        self.seasons = [
                {"chapter": "1", "season": "1"},
                {"chapter": "1", "season": "2"},
                {"chapter": "1", "season": "3"},
                {"chapter": "1", "season": "4"},
                {"chapter": "1", "season": "5"},
                {"chapter": "1", "season": "6"},
                {"chapter": "1", "season": "7"},
                {"chapter": "1", "season": "8"},
                {"chapter": "1", "season": "9"},
                {"chapter": "1", "season": "10"},
                {"chapter": "2", "season": "1"},
                {"chapter": "2", "season": "2"},
                {"chapter": "2", "season": "3"},
                {"chapter": "2", "season": "4"},
            ]
        self.clientId = 1408050308134862952
        self.logo_name = "logo"
        self.mitm_cert_location = None

    def get_cosmetics(self):
        r = requests.get('https://fortnite-api.com/v2/cosmetics/br')
        return r.json()

    def install_mitm_cert(self):
        if os.name == "nt": 
            cert_path = os.path.join(os.getenv('APPDATA'), 'mitmproxy', 'mitmproxy-ca-cert.cer')
            
            if not os.path.exists(cert_path):
                print("MITM certificate not found. Please start mitmproxy first to generate the certificate.")
                return False
            
            try:
                temp_cert = os.path.join(os.environ['TEMP'], 'mitmproxy-ca-cert.cer')
                shutil.copy2(cert_path, temp_cert)
                
                command = [
                    'certutil', '-addstore', '-f', 'root', temp_cert
                ]
                
                if os.system('net session >nul 2>&1') == 0:
                    result = subprocess.run(command, capture_output=True, text=True)
                else:
                    import ctypes
                    if ctypes.windll.shell32.IsUserAnAdmin():
                        result = subprocess.run(command, capture_output=True, text=True)
                    else:
                        params = ' '.join(['"' + x + '"' for x in command])
                        result = subprocess.run(
                            f'powershell -Command "Start-Process cmd -ArgumentList \'/c {params}\' -Verb RunAs -Wait"',
                            shell=True, capture_output=True, text=True
                        )
                
                try:
                    os.remove(temp_cert)
                except:
                    pass
                    
                if result.returncode == 0:
                    print("MITM certificate successfully installed to Windows Trusted Root Store")
                    return True
                else:
                    print(f"Failed to install certificate: {result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"Error installing certificate: {e}")
                return False
        


    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def show_title(self):
        self.clear()
        print(Fore.CYAN + self.title)
        print(Style.RESET_ALL + f" {self.name} | {self.version} | {self.author}")
        print(f" Discord: {self.discord}")
        print("=" * 40)

    def config_menu(self):

        while True:
            self.show_title()
            print(f" Current Config:\n"
                f"  → Level: {self.level}\n"
                f"  → V-Bucks: {self.vbucks}\n"
                f"  → Dev Locker: {'Enabled' if self.all_cosmetics else 'Disabled'}\n"
                f"  → Account ID: {self.accountID if self.accountID else 'Not set'}\n"
                f"  → Account Items: {len(self.cosmetics) if self.all_cosmetics else 'TBD'} item{'s' if len(self.cosmetics) > 1 else ''}\n"
                f"  → Custom Shop: {'Enabled' if self.custom_shop else 'Disabled'}\n"
                f"  → Custom Name: {self.custom_name if self.custom_name else 'Not set'}\n")
            
            print(" Options:")
            print(" 1. Set Level")
            print(" 2. Set V-Bucks")
            print(" 3. Enabled Dev Locker")
            print(" 4. Custom Shop")
            print(" 5. Set Custom Name")
            print(" 6. Start")
            print(" 7. Exit")

            try:
                choice = int(input(" Enter your choice: ").strip())
                if choice == 1:
                    level = input(" Enter the level you want to set: ").strip()
                    if level.isdigit():
                        self.level = int(level)
                        print(f" Level set to {self.level}.")
                    else:
                        print(" Invalid level. Please enter a number.")
                elif choice == 2:
                    vbucks = input(" Enter the amount of V-Bucks you want to set: ").strip()
                    if vbucks.isdigit():
                        self.vbucks = int(vbucks)
                        print(f" V-Bucks set to {self.vbucks}.")
                    else:
                        print(" Invalid V-Bucks amount. Please enter a number.")
                elif choice == 3:
                    if self.all_cosmetics:
                        self.all_cosmetics = False
                        print(" Dev Locker disabled.")
                    else:
                        self.all_cosmetics = True
                        print(" Dev Locker enabled. All cosmetics will be added.")
                elif choice == 4:
                    if self.custom_shop:
                        self.custom_shop = False
                        print(" Custom shop disabled.")
                    else:
                        self.custom_shop = True
                        print(" Custom shop enabled. Custom items will be added to the shop.")
                elif choice == 5:
                    custom_name = input(" Enter the custom name you want to set (No Filter): ").strip()
                    if custom_name:
                        self.custom_name = custom_name
                        print(f" Custom name set to {self.custom_name}.")
                    else:
                        print(" Invalid name. Please enter a valid name.")
                elif choice == 6:
                    print("Launching proxy...")
                    break
                elif choice == 7:
                    print("Exiting...")
                    exit()
            except ValueError:
                print("Invalid input.")
                time.sleep(1.5)


    def create_uuid(self):
        return str(uuid.uuid4())[:24]


    def edit_athena(self, flow: http.HTTPFlow):
        if "profileid=athena" in flow.request.url.lower():
            response_text = flow.response.content.decode('utf-8')
            try:
                data = json.loads(response_text)
            except:
                return

            if not data:
                return

            profile = data.get('profile', {})
            cosmetics = self.get_cosmetics()
            current_items = profile.get('items', {})

            for cosmetic in cosmetics.get('data', []):
                intro = cosmetic.get("introduction")
                if not intro:
                    continue

                chapter = str(intro.get("chapter", ""))
                season = str(intro.get("season", ""))

                if not any(s["chapter"] == chapter and s["season"] == season for s in self.seasons):
                    continue

                template_id = f"{cosmetic.get('backendValue')}:{cosmetic.get('id')}"
                if template_id in current_items:
                    continue

                item_uuid = self.create_uuid()

                variants = []
                if "variants" in cosmetic:
                    for v in cosmetic["variants"]:
                        variants.append({
                            "channel": v.get("channel"),
                            "owned": [opt.get("tag") for opt in v.get("options", [])]
                        })

                cosmetic_data = {
                    item_uuid: {
                        "attributes": {
                            "favorite": False,
                            "item_seen": True,
                            "level": 1,
                            "max_level_bonus": 0,
                            "variants": variants,
                            "xp": 0
                        },
                        "quantity": 1,
                        "templateId": template_id
                    }
                }

                current_items.update(cosmetic_data)

            
            profile['items'] = current_items

            # Boost level
            updates = ['accountLevel', 'book_level', 'book_xp', 'xp']
            for update in updates:
                profile['stats']['attributes'][update] = self.level

            data['profile'] = profile

            flow.response.status_code = 200
            flow.response.content = json.dumps(data).encode('utf-8')



    def edit_vbucks(self, flow: http.HTTPFlow):
        if "profileId=common_core" in flow.request.pretty_url:
            response_text = flow.response.content.decode('utf-8')
            try:
                data = json.loads(response_text)
            except:
                return
            
            profileChanges = data['profileChanges']
            items = profileChanges['items']

            if "gyattinohio" in items:
                items["gyattinohio"] = {
                    "attributes": {
                            "favorite": False,
                            "item_seen": False,
                            "level": 1,
                            "max_level_bonus": 0,
                            "platform": "Shared",
                            "variants": [],
                            "xp": 0
                        },
                        "quantity": self.vbucks,  # V-Bucks amount
                        "templateId": "Currency:MtxPurchased"
                }

                profileChanges['items'] = items
                data['profileChanges'] = profileChanges
            
            flow.response.status_code = 200
            flow.response.content = json.dumps(data).encode('utf-8')

    def edit_content(self, flow: http.HTTPFlow):
        if "https://retrac.site/content/api/pages/fortnite-game/" in flow.request.pretty_url:
            response_text = flow.response.content.decode('utf-8')
            try:
                data = json.loads(response_text)
            except:
                return
            
            br_news = data['battleroyalenewsv2']
            news = br_news['news']
            motds = news['motds']

            motds.append({
                "id": "news3",
                    "entryType": "Text",
                    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOPj_OFX6D25szdH0r2HBfH5xhYGpgRqOBBQ&s",
                    "tileImage": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOPj_OFX6D25szdH0r2HBfH5xhYGpgRqOBBQ&s",
                    "hidden": False,
                    "title": "Thanks for using Retrac Dev!",
                    "body": "I appreciate you using the Retrac Dev and hope you enjoy having unlimited V-Bucks, levels and a free dev locker! ",
                    "sortingPriority": 0,
                    "spotlight": False
            })
            br_news['news'] = news
            data['battleroyalenewsv2'] = br_news

            emergancyNotice = data['emergencynotice']

            emergancyNotice = {
            "_title": "emergencynoticev2",
            "_noIndex": False,
            "emergencynotices": {
            "_type": "Emergency Notices",
            "emergencynotices": [
                {
                    "hidden": False,
                    "_type": "CommonUI Emergency Notice Base",
                    "title": "Comet Hybrid",
                    "body": "☄ Welcome to Retrac Dev!\n\n✨ Made by Star\n\n❤ Discord: discord.gg/retrac"
                }
            ]
        }
    }
            dynamicBackgrounds = data['dynamicbackgrounds']
            dynamicBackgrounds = {
            "backgrounds": {
            "backgrounds": [
                {
                "backgroundimage": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOPj_OFX6D25szdH0r2HBfH5xhYGpgRqOBBQ&s",
                "stage": "defaultnotris",
                "_type": "DynamicBackground",
                "key": "lobby"
                }
            ],
            "_type": "DynamicBackgroundList"
            },
            "_title": "dynamicbackgrounds",
            "_noIndex": False,
            "_activeDate": "2023-11-03T07:30:00.000Z",
            "lastModified": "2025-06-07T21:52:49.754Z",
            "_locale": "en-US",
            "_templateName": "FortniteGameDynamicBackgrounds"
        }
            
            tournementInfo = data['tournamentinformation']
            tournement_info = tournementInfo['tournament_info']
            tournements = tournement_info['tournaments']

            tournements[3] = {
                    "tournament_display_id": "LG_ARENA_DUOS",
                    "title_line_1": "",
                    "title_line_2": "STARS LATEGAME",
                    "schedule_info": "",
                    "poster_front_image": "",
                    "poster_back_image": "",
                    "flavor_description": "",
                    "details_description": "",
                    "short_format_title": "",
                    "long_format_title": "",
                    "background_title": "",
                    "pin_score_requirement": 0,
                    "pin_earned_text": "",
                    "base_color": "",
                    "primary_color": "",
                    "secondary_color": "",
                    "highlight_color": "",
                    "title_color": "",
                    "shadow_color": "",
                    "background_left_color": "",
                    "background_right_color": "",
                    "background_text_color": "",
                    "poster_fade_color": "",
                    "playlist_tile_image": "https://convicts.us/Lyric_LateGame.png",
                    "loading_screen_image": "",
                    "style_info_id": ""
                }
            tournement_info['tournaments'] = tournements
            tournementInfo['tournament_info'] = tournement_info
            data['emergencynotice'] = emergancyNotice
            data['dynamicbackgrounds'] = dynamicBackgrounds
            data['tournamentinformation'] = tournementInfo
            flow.response.status_code = 200
            flow.response.content = json.dumps(data).encode('utf-8')

    def custom_shop(self, flow: http.HTTPFlow):
        if "https://retrac.site/fortnite/api/storefront" in flow.request.pretty_url or "catalog" in flow.request.pretty_url:
            try:
                response_text = flow.response.content.decode('utf-8')
                data = json.loads(response_text)
                
                custom_shop_items = {
                    "IKONIK": {
                        "id": "CID_313_Athena_Commando_M_KpopFashion",
                        "mtx": 1500,
                        "name": "IKONIK",
                        "athena": "AthenaCharacter",
                        "type": "Outfits"
                    },
                    "Floss": {
                        "id": "EID_Floss",
                        "mtx": 500,
                        "name": "Floss",
                        "athena": "AthenaDance",
                        "type": "Dance"
                    },
                    "Stellar Axe": {
                        "id": "Pickaxe_ID_116_Celestial",
                        "mtx": 1500,
                        "name": "Stellar Axe",
                        "athena": "AthenaPickaxe",
                        "type": "Pickaxe"
                    },
                    "Indigo Kuno": {
                        "id": "CID_660_Athena_Commando_F_BandageNinjaBlue",
                        "mtx": 1200,
                        "name": "Indigo Kuno",
                        "athena": "AthenaCharacter",
                        "type": "Outfits"
                    }
                }
                
                for storefront in data['storefronts']:
                    if storefront['name'] == 'BRWeeklyStorefront':
                        for item_name, item_data in custom_shop_items.items():
                            catalog_entry = {
                                "appStoreId": [],
                                "bannerOverride": "",
                                "catalogGroupPriority": 0,
                                "categories": ["0"], 
                                "dailyLimit": -1,
                                "description": "",
                                "devName": f"[MTX] 1× {item_data['id']} for {item_data['mtx']} V-Bucks",
                                "displayAssetPath": "",
                                "filterWeight": 0,
                                "fulfillmentIds": [],
                                "giftInfo": {
                                    "bIsEnabled": True,
                                    "forcedGiftBoxTemplateId": "",
                                    "giftRecordIds": [],
                                    "purchaseRequirements": [
                                        {
                                            "minQuantity": 1,
                                            "requiredId": f"{item_data['athena']}:{item_data['id']}",
                                            "requirementType": "DenyOnItemOwnership"
                                        }
                                    ]
                                },
                                "itemGrants": [
                                    {
                                        "quantity": 1,
                                        "templateId": f"{item_data['athena']}:{item_data['id']}"
                                    }
                                ],
                                "meta": {
                                    "Category": "0", 
                                    "SectionId": "Weekly",
                                    "TileSize": "Normal"
                                },
                                "metaInfo": [
                                    {
                                        "Key": "Category",
                                        "Value": "0"  
                                    },
                                    {
                                        "Key": "SectionId",
                                        "Value": "Weekly"
                                    },
                                    {
                                        "Key": "TileSize",
                                        "Value": "Normal"
                                    }
                                ],
                                "monthlyLimit": -1,
                                "offerId": f"custom_{item_data['id'].lower()}",
                                "offerType": "StaticPrice",
                                "prices": [
                                    {
                                        "basePrice": item_data['mtx'],
                                        "currencySubType": "",
                                        "currencyType": "MtxCurrency",
                                        "dynamicRegularPrice": -1,
                                        "finalPrice": item_data['mtx'],
                                        "regularPrice": item_data['mtx'],
                                        "saleExpiration": "9999-12-31T23:59:59.999Z"
                                    }
                                ],
                                "refundable": True,
                                "requirements": [
                                    {
                                        "minQuantity": 1,
                                        "requiredId": f"{item_data['athena']}:{item_data['id']}",
                                        "requirementType": "DenyOnItemOwnership"
                                    }
                                ],
                                "shortDescription": "",
                                "sortPriority": 0,
                                "title": "",
                                "weeklyLimit": -1
                            }

                            storefront['catalogEntries'].append(catalog_entry)
                
                flow.response.status_code = 200
                flow.response.content = json.dumps(data).encode('utf-8')
                
            except Exception as e:
                return

    def handle_equip(self, flow: http.HTTPFlow):
        if "SetCosmeticLockerSlot?profileId=athena" not in flow.request.pretty_url:
            return

        try:
            request_data = json.loads(flow.request.content.decode("utf-8"))
            response_data = json.loads(flow.response.content.decode("utf-8"))  
        except (json.JSONDecodeError, UnicodeDecodeError):
            return

        locker_item = request_data.get("lockerItem", "")
        category = request_data.get("category", "")
        item_to_slot = request_data.get("itemToSlot", "")
        slot_index = request_data.get("slotIndex", 0)
        variant_updates = request_data.get("variantUpdates", [])

        if not locker_item or not category or not item_to_slot:
            return

        profile_changes = response_data.get("profileChanges", [])
        if profile_changes and "attributeValue" in profile_changes[0]:
            slots = profile_changes[0]["attributeValue"].get("slots", {})
        else:
            slots = {}

        if category not in slots:
            slots[category] = {"activeVariants": [{"variants": []}], "items": []}

        items = slots[category]["items"]
        while len(items) <= slot_index:
            items.append("")

        items[slot_index] = item_to_slot
        slots[category]["items"] = items

        if variant_updates:
            if "activeVariants" not in slots[category] or not slots[category]["activeVariants"]:
                slots[category]["activeVariants"] = [{"variants": []}]
            slots[category]["activeVariants"][0]["variants"] = variant_updates

        response_data["profileChanges"][0]["attributeValue"]["slots"] = slots
        response_data["profileChanges"][0]["itemId"] = locker_item

        flow.response.status_code = 200
        flow.response.text = json.dumps(response_data)

    def custom_name(self, flow: http.HTTPFlow):
        if "https://retrac.site/account/api/oauth/verify" in flow.request.pretty_url:
            try:
                response_text = flow.response.content.decode('utf-8')
                data = json.loads(response_text)
            except json.JSONDecodeError:
                return
            
            if not self.custom_name:
                return
            
            if "displayName" in data:
                data['displayName'] = self.custom_name
            elif "display_name" in data:
                data['display_name'] = self.custom_name
            elif "name" in data:
                data['name'] = self.custom_name
            elif "username" in data:
                data['username'] = self.custom_name
            else:
                return
            
            flow.response.status_code = 200
            flow.response.content = json.dumps(data).encode('utf-8')


    def response(self, flow: http.HTTPFlow):
        if "SetCosmeticLockerSlot?profileId=athena" in flow.request.pretty_url:
            self.handle_equip(flow)
        elif "profileid=athena" in flow.request.url.lower() and self.all_cosmetics:
            self.edit_athena(flow)
        elif "profileId=common_core" in flow.request.pretty_url.lower() and self.vbucks > 0:
            self.edit_vbucks(flow)
        elif "https://retrac.site/content/api/pages/fortnite-game/" in flow.request.pretty_url:
            self.edit_content(flow)
        elif "https://retrac.site/fortnite/api/storefront" in flow.request.pretty_url or "catalog" in flow.request.pretty_url:
            if self.custom_shop:
                self.custom_shop(flow)
        elif "https://retrac.site/account/api/oauth/verify" in flow.request.pretty_url:
            if self.custom_name:
                self.custom_name(flow)
        
        




            
                








retrac = Retrac()


Addons = [
    retrac
]

async def start():
    opts = options.Options(listen_host='0.0.0.0', listen_port=8082)
    m = DumpMaster(opts)

    for addon in Addons:
        m.addons.add(addon)

    print(f"Starting proxy with {len(Addons)} addon{'s' if len(Addons) != 1 else ''}...")
    retrac.install_mitm_cert()

    try:
        await m.run()
    except KeyboardInterrupt:
        print("\n[!] Keyboard interrupt detected. Stopping proxy...")
        m.shutdown()


def run_presence():
    try:
        RPC = Presence(1408050308134862952)
        RPC.connect()
        RPC.update(
            state="Using dev locker for free!",
            details="Playing Retrac Dev",
            large_image="logo",
        )
        
        while True:
            time.sleep(15)
    except Exception as e:
        print(f"[!] Discord Rich Presence failed: {e}")

if __name__ == "__main__":
    presence_thread = threading.Thread(target=run_presence, daemon=True)
    presence_thread.start()
    retrac.config_menu()
    asyncio.run(start())



