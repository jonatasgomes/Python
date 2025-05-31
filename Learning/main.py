max_load = 15
packs = [
    { "color": "green", "value": 4, "load": 12 },
    { "color": "blue", "value": 2, "load": 2 },
    { "color": "gray", "value": 2, "load": 1 },
    { "color": "red", "value": 1, "load": 1 },
    { "color": "yellow", "value": 10, "load": 4 }
]
for pack in packs:
    pack["multiplier"] = (max_load / pack["load"]) * pack["value"]
    pack["available"] = max_load // pack["load"]

sorted_packs = sorted(packs, key=lambda x: x["multiplier"], reverse=True)
for pack in sorted_packs:
    print(pack["color"], pack["value"], pack["load"], pack["multiplier"], pack["available"])
