import json
import re
from collections import defaultdict

from text_cleaner import clean_text_optimized, preprocessing_rules

patterns = [r'>\s*:(.*?):\s*\n(.*)']

def detect_with_regex(text) -> bool:
    for _, pattern in enumerate(patterns, start=1):
        match = re.search(pattern, text)

        if match:
            return True
    return False

def check_text_length(text: str, min_length: int = 4) -> bool:
    replaced_text = text
    for val in preprocessing_rules.values():
        replaced_text: str = replaced_text.replace(val, "")
    return len(replaced_text) >= min_length

with open("./posts.json", "r") as f:
    data_list = json.load(f)

grouped_data = defaultdict(lambda: defaultdict(list))

words = ["#shindanmaker", "#nowplaying", "https://misskey.io/play/"]

for item in data_list:
    year_month = item["published"][:7]

    visibility = item.get("visibility", "unknown")

    content = str(item["content"].lower())

    if not (
        any(word in content for word in words)
        or (content.startswith(":") and content.endswith(":"))
        or detect_with_regex(content)
    ):
        processed_text = clean_text_optimized(str(item["content"])).replace("\n", " ")
        if processed_text not in preprocessing_rules.values() and check_text_length(processed_text):
            grouped_data[year_month][visibility].append({
                "published": item["published"],
                "content": processed_text
            })

result = {
    ym: {vis: items for vis, items in vis_dict.items()}
    for ym, vis_dict in grouped_data.items()
}

with open("./posts_preprocessed.json", "w") as fp:
    json.dump(result, fp, ensure_ascii=False, indent=2)
