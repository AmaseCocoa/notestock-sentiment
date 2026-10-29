import json

with open("./posts_preprocessed.json", "r") as f:
    data = json.load(f)

result = []

for month, categories in data.items():
    for category, items in categories.items():
        count = 0
        for item in items:
            if count >= 5:
                break
            if isinstance(item, dict) and "content" in item:
                result.append(item["content"])
                count += 1

with open("to_process.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
