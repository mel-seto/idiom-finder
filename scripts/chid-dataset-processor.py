"""
Source data from: https://huggingface.co/datasets/thu-coai/chid
"""

import json

from datasets import load_dataset
from pypinyin import Style, pinyin


dataset = load_dataset("thu-coai/chid")

candidate_idioms = {
    c
    for example in dataset["train"]
    for candidate in json.loads(example["text"])["candidates"]
    for c in (candidate if isinstance(candidate, list) else [candidate])
}
# based on the published paper, the ChID dataset includes exactly 3848 idioms
assert len(candidate_idioms) == 3848

reference_data = []
for idiom in candidate_idioms:
    reference_data.append(idiom)

with open("../idiom_dataset/chid_idiom_reference.json", "w", encoding="utf-8") as f:
    json.dump(reference_data, f, ensure_ascii=False, indent=2)
