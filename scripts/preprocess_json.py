import json
import re
from collections import defaultdict

patterns = [r'>\s*:(.*?):\s*\n(.*)']

def detect_with_regex(text) -> bool:
    for _, pattern in enumerate(patterns, start=1):
        match = re.search(pattern, text)

        if match:
            return True
    return False


with open("./posts.json", "r") as f:
    data_list = json.load(f)

grouped_data = defaultdict(lambda: defaultdict(list))

words = ["#shindanmaker", "#nowplaying", "https://misskey.io/play/"]

for item in data_list:
    year_month = item["published"][:7]

    visibility = item.get("visibility", "unknown")

    content = str(item["content"].lower())

    if (
        any(word in content for word in words)
        or len(content) < 3
        or (content.startswith(":") and content.endswith(":"))
        or detect_with_regex(content)
    ):
        pass
    else:
        grouped_data[year_month][visibility].append(item)

result = {
    ym: {vis: items for vis, items in vis_dict.items()}
    for ym, vis_dict in grouped_data.items()
}

with open("./posts_preprocessed.json", "w") as fp:
    json.dump(result, fp, ensure_ascii=False, indent=2)
