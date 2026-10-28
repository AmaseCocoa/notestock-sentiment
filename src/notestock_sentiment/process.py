from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# モデルとトークナイザのロード
model_name = "neuralnaut/deberta-wrime-emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 感情ラベル（出力の順序に対応）
EMOTION_LABELS = ["joy", "sadness", "anticipation", "surprise", "anger", "fear", "disgust", "trust"]

# 推論
text = "今日はとても楽しい一日でした！"
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)

model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    predictions = outputs.logits.cpu().numpy()[0]

# デノーマライズとクリッピング
predictions = predictions * 3.0
predictions = np.clip(predictions, 0.0, 3.0)

# スコアの高い順にインデックスをソート（降順）
sorted_indices = np.argsort(predictions)[::-1]

# 1位と2位のインデックスとスコアを取得
first_idx = sorted_indices[0]
second_idx = sorted_indices[1]

first_score = float(predictions[first_idx])
second_score = float(predictions[second_idx])

DIFF_THRESHOLD = 0.3
if (first_score - second_score) < DIFF_THRESHOLD:
    result = "null"
else:
    result = {
        "emotion": EMOTION_LABELS[first_idx],
        "score": round(first_score, 2)
    }

print(f"テキスト: {text}")
print(f"結果: {result}")
