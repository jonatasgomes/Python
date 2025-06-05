max_load = 15
packs = [
    { "color": "green", "value": 4, "weight": 12 },
    { "color": "blue", "value": 2, "weight": 2 },
    { "color": "gray", "value": 2, "weight": 1 },
    { "color": "red", "value": 1, "weight": 1 },
    { "color": "yellow", "value": 10, "weight": 4 }
]

def v1():
    print("Greedy approach to load packs:")
    loaded = []
    loaded_weight = 0
    loaded_value = 0
    sorted_packs = sorted(packs, key=lambda x: x["weight"], reverse=True)

    for pack in sorted_packs:
        if loaded_weight + pack["weight"] <= max_load:
            loaded.append(pack)
            loaded_weight += pack["weight"]
            loaded_value += pack["value"]
            print(f"Adding {pack['color']} pack with weight {pack['weight']}. Total loaded: {loaded_weight}.")
        else:
            print(f"Cannot add {pack['color']} pack with weight {pack['weight']}. {pack['weight'] + loaded_weight} would exceed max load.")

    print(f"Loaded value: {loaded_value}")
    print(f"Loaded weight: {loaded_weight}")

def v2():
    print("\nDynamic programming approach to load packs:")
    max_weight = 15
    packs = [
        { "color": "green", "value": 4, "weight": 12 },
        { "color": "blue", "value": 2, "weight": 2 },
        { "color": "gray", "value": 2, "weight": 1 },
        { "color": "red", "value": 1, "weight": 1 },
        { "color": "yellow", "value": 10, "weight": 4 }
    ]

    n = len(packs)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if packs[i-1]["weight"] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w - packs[i-1]["weight"]] + packs[i-1]["value"]
                )
            else:
                dp[i][w] = dp[i-1][w]

    # Backtrack to find which items were used
    w = max_weight
    used_items = []
    loaded_value = 0
    loaded_weight = 0

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            item = packs[i-1]
            used_items.append(item)
            loaded_value += item["value"]
            loaded_weight += item["weight"]
            w -= item["weight"]

    # Output results
    # print("Maximum value:", dp[n][max_weight])
    # print("Items used:")
    # for item in used_items:
    #     print(f"{item['color']} (value: {item['value']}, weight: {item['weight']})")

    print(f"Loaded value: {loaded_value}")
    print(f"Loaded weight: {loaded_weight}")


v1()
v2()
