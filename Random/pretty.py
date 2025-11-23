import json

with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("content.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)