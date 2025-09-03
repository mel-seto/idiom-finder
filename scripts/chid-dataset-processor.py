# Code generated with ChatGPT

import json
from pypinyin import pinyin, Style
from datasets import load_dataset

# --- Load ChID dataset ---
dataset = load_dataset("thu-coai/chid")

# --- Helper to extract ground truth idioms ---
def get_ground_truth(example):
    data = json.loads(example["text"])
    # Take the first candidate for each content passage
    return [c[0] for c in data["candidates"][:len(data["content"])]]

# --- Collect all ground truth idioms ---
ground_truths = []
for example in dataset["train"]:
    ground_truths.extend(get_ground_truth(example))

# --- Filter only 4-character idioms ---
idiom_set = {idiom for idiom in ground_truths if len(idiom) == 4}

print(f"Filtered 4-character idioms: {len(idiom_set)}")

# --- Generate pinyin for each idiom ---
def generate_pinyin(idiom):
    pinyin_list = pinyin(idiom, style=Style.TONE)
    return " ".join([s[0] for s in pinyin_list])

# --- Build reference dataset ---
reference_data = []
for idiom in idiom_set:
    reference_data.append({
        "idiom": idiom,
        "pinyin": generate_pinyin(idiom)
    })

# --- Save to JSON ---
with open("chid_idiom_reference_with_pinyin.json", "w", encoding="utf-8") as f:
    json.dump(reference_data, f, ensure_ascii=False, indent=2)

print("Reference dataset saved as 'chid_idiom_reference_with_pinyin.json'")
