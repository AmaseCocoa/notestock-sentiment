import json
from typing import cast

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers.tokenization_utils_tokenizers import TokenizersBackend

model_name = "neuralnaut/deberta-wrime-emotions"
tokenizer: TokenizersBackend = cast(
    TokenizersBackend, AutoTokenizer.from_pretrained(model_name)
)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

EMOTION_LABELS = [
    "joy",
    "sadness",
    "anticipation",
    "surprise",
    "anger",
    "fear",
    "disgust",
    "trust",
]


model.eval()


def eval_text(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = outputs.logits.cpu().numpy()[0]

    predictions = predictions * 3.0
    predictions = np.clip(predictions, 0.0, 3.0)

    sorted_indices = np.argsort(predictions)[::-1]

    first_idx = sorted_indices[0]
    second_idx = sorted_indices[1]

    first_score = float(predictions[first_idx])
    second_score = float(predictions[second_idx])

    scores_list = predictions.tolist()
    raw_data = {
        EMOTION_LABELS[i]: round(score, 2) for i, score in enumerate(scores_list)
    }

    DIFF_THRESHOLD = 0.3
    if (first_score - second_score) < DIFF_THRESHOLD:
        return {"final": None, "raw": raw_data}
    else:
        return {
            "final": {
                "emotion": EMOTION_LABELS[first_idx],
                "score": round(first_score, 2),
            },
            "raw": raw_data,
        }

class PostData:
    published: datetime

with open("./posts_preprocessed.json", "r") as f:
    data:  = json.load(f)

results = []
for text in texts:
    result = eval_text(text)
    results.append({
        "text": text,
        "date": "",
        "visibility": "",
        "result": result
    })

with open("./result.json", "w") as fp:
    json.dump(results, fp, indent=2, ensure_ascii=False)
