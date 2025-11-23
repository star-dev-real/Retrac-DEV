import os
import json
import re

def process_cosmetic_files():
    directory = input("Enter the directory path containing cosmetic files: ").strip()
    
    directory = directory.strip('"')
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist!")
        return
    
    profile_path = r"C:\Users\Ralph\Downloads\LawinServer-main\LawinServer-main\profiles\athena.json"
    
    if not os.path.exists(profile_path):
        print(f"Error: Profile file '{profile_path}' does not exist!")
        return
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
    except Exception as e:
        print(f"Error reading profile file: {e}")
        return
    
    # Detect profile type
    profile_type = detect_profile_type(profile_data)
    print(f"Detected profile type: {profile_type}")
    
    cosmetic_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.json'):
                full_path = os.path.join(root, filename)
                cosmetic_files.append((filename, full_path))
    
    if not cosmetic_files:
        print("No JSON files found in the directory!")
        return
    
    print(f"Found {len(cosmetic_files)} JSON files (scanning recursively)")
    
    valid_prefixes = [
        'CID_', 'Character_',
        'BID_', 'Backpack_',
        'PID_', 'Pickaxe_',
        'GID_', 'Glider_',
        'Contrail_', 'Trail_',
        'EID_', 'Dance_', 'Emote_', 'Emoji_',
        'MPID_', 'MusicPack_',
        'LSID_', 'LoadingScreen_',
        'WID_', 'Wrap_',
        'SprayID_', 'Spray_',
        'ToyID_', 'Toy_',
        'PetCarrier_', 'Pet_'
    ]
    
    stats = {
        'added': 0,
        'updated': 0,
        'skipped_no_prefix': 0,
        'total_processed': 0
    }
    
    for filename, full_path in cosmetic_files:
        stats['total_processed'] += 1
        
        has_valid_prefix = any(filename.startswith(prefix) for prefix in valid_prefixes)
        
        if not has_valid_prefix:
            print(f"Skipped (no valid prefix): {filename}")
            stats['skipped_no_prefix'] += 1
            continue
        
        cosmetic_type, cosmetic_id = detect_cosmetic_type(filename)
        
        if cosmetic_type and cosmetic_id:
            # Convert types for compatibility
            original_type = cosmetic_type
            if cosmetic_type in ["AthenaEmoji", "AthenaSpray", "AthenaToy"]:
                cosmetic_type = "AthenaDance"
            elif cosmetic_type in ["AthenaPet", "AthenaPetCarrier"]:
                cosmetic_type = "AthenaBackpack"
            
            template_id = f"{cosmetic_type}:{cosmetic_id}"
            
            if profile_type == "retrac":
                # Original retrac format
                if template_id in profile_data["profileChanges"][0]["profile"]["items"]:
                    print(f"Already exists: {template_id}")
                    stats['updated'] += 1
                else:
                    new_cosmetic = create_cosmetic_entry(cosmetic_type, template_id, cosmetic_id, profile_type)
                    if new_cosmetic:
                        profile_data["profileChanges"][0]["profile"]["items"][template_id] = new_cosmetic
                        print(f"Added: {template_id}")
                        stats['added'] += 1
            elif profile_type == "lawin_athena":
                # Lawin athena format
                if template_id in profile_data["items"]:
                    print(f"Already exists: {template_id}")
                    stats['updated'] += 1
                else:
                    new_cosmetic = create_cosmetic_entry(cosmetic_type, template_id, cosmetic_id, profile_type)
                    if new_cosmetic:
                        profile_data["items"][template_id] = new_cosmetic
                        print(f"Added: {template_id}")
                        stats['added'] += 1
        else:
            print(f"Unknown cosmetic type: {filename}")
            stats['skipped_no_prefix'] += 1
    
    try:
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2)
        
        print(f"\n=== SUMMARY ===")
        print(f"Profile type: {profile_type}")
        print(f"Total files scanned: {stats['total_processed']}")
        print(f"Added: {stats['added']}")
        print(f"Already existed: {stats['updated']}")
        print(f"Skipped (no valid prefix): {stats['skipped_no_prefix']}")
        print(f"Successfully processed: {stats['added'] + stats['updated']}")
        
        if profile_type == "retrac":
            print(f"Total items in profile: {len(profile_data['profileChanges'][0]['profile']['items'])}")
        elif profile_type == "lawin_athena":
            print(f"Total items in profile: {len(profile_data['items'])}")
        
    except Exception as e:
        print(f"Error writing profile file: {e}")

def detect_profile_type(profile_data):
    """Detect the type of profile format"""
    if "profileChanges" in profile_data and len(profile_data["profileChanges"]) > 0:
        if "profile" in profile_data["profileChanges"][0] and "items" in profile_data["profileChanges"][0]["profile"]:
            return "retrac"
    
    if "items" in profile_data:
        return "lawin_athena"
    
    return "unknown"

def detect_cosmetic_type(filename):
    base_name = filename.replace('.json', '').replace('.JSON', '')
    
    type_mappings = {
        'CID_': 'AthenaCharacter',
        'Character_': 'AthenaCharacter',
        'BID_': 'AthenaBackpack', 
        'Backpack_': 'AthenaBackpack',
        'PID_': 'AthenaPickaxe',
        'Pickaxe_': 'AthenaPickaxe',
        'GID_': 'AthenaGlider',
        'Glider_': 'AthenaGlider',
        'Contrail_': 'AthenaContrail',
        'Trail_': 'AthenaContrail',
        'EID_': 'AthenaDance',
        'Dance_': 'AthenaDance',
        'Emote_': 'AthenaDance',
        'Emoji_': 'AthenaEmoji',
        'MPID_': 'AthenaMusicPack',
        'MusicPack_': 'AthenaMusicPack',
        'LSID_': 'AthenaLoadingScreen',
        'LoadingScreen_': 'AthenaLoadingScreen',
        'WID_': 'AthenaItemWrap',
        'Wrap_': 'AthenaItemWrap',
        'SprayID_': 'AthenaSpray',
        'Spray_': 'AthenaSpray',
        'ToyID_': 'AthenaToy',
        'Toy_': 'AthenaToy',
        'PetCarrier_': 'AthenaPetCarrier',
        'Pet_': 'AthenaPet'
    }
    
    for prefix, cosmetic_type in type_mappings.items():
        if base_name.startswith(prefix):
            return cosmetic_type, base_name
    
    return None, None

def create_cosmetic_entry(cosmetic_type, template_id, cosmetic_id, profile_type):
    """Create a cosmetic entry based on profile type"""
    
    # Convert types for compatibility
    if cosmetic_type in ["AthenaEmoji", "AthenaSpray", "AthenaToy"]:
        cosmetic_type = "AthenaDance"
    elif cosmetic_type in ["AthenaPet", "AthenaPetCarrier"]:
        cosmetic_type = "AthenaBackpack"
    
    if profile_type == "retrac":
        base_attributes = {
            "max_level_bonus": 0,
            "level": 1,
            "item_seen": True,
            "xp": 0,
            "variants": [],
            "favorite": False
        }
        
        if cosmetic_type in ['AthenaDance', 'AthenaLoadingScreen', 'AthenaItemWrap']:
            base_attributes = {
                "item_seen": True,
                "favorite": False
            }
        
        return {
            "templateId": template_id,
            "attributes": base_attributes,
            "quantity": 1
        }
    
    elif profile_type == "lawin_athena":
        # Lawin athena format uses simpler structure
        return {
            "templateId": template_id,
            "attributes": {
                "max_level_bonus": 0,
                "level": 1,
                "item_seen": True,
                "xp": 0,
                "variants": [],
                "favorite": False
            },
            "quantity": 1
        }

if __name__ == "__main__":
    print("Fortnite Cosmetic Profile Updater - RECURSIVE SCAN")
    print("=" * 55)
    print("This script will:")
    print("• Scan ALL subfolders recursively")
    print("• Detect profile format automatically (retrac/LawinServer)")
    print("• Only process files starting with known cosmetic prefixes")
    print("• Skip files without valid prefixes (EID_, CID_, BID_, etc.)")
    print("• Convert types: Emoji/Spray/Toy -> Dance, Pet/PetCarrier -> Backpack")
    print("")
    print("Supported prefixes:")
    print("Characters: CID_, Character_")
    print("Backpacks: BID_, Backpack_") 
    print("Pickaxes: PID_, Pickaxe_")
    print("Gliders: GID_, Glider_")
    print("Contrails: Contrail_, Trail_")
    print("Emotes: EID_, Dance_, Emote_, Emoji_")
    print("Music Packs: MPID_, MusicPack_")
    print("Loading Screens: LSID_, LoadingScreen_")
    print("Wraps: WID_, Wrap_")
    print("Sprays: SprayID_, Spray_ (converted to Dance)")
    print("Toys: ToyID_, Toy_ (converted to Dance)")
    print("Pets: PetCarrier_, Pet_ (converted to Backpack)")
    print("=" * 55)
    
    process_cosmetic_files()
    input("\nPress Enter to exit...")