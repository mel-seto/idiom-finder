"""
This script needs to be re-run each time EMBEDDING_MODEL is updated.
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from constants import EMBEDDING_MODEL 

INPUT_FILE = "data/idiom-definition-context-short.json"
EMBED_FILE = "data/idiom_embeddings.npy"

embedder = SentenceTransformer(EMBEDDING_MODEL)


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_idioms = json.load(f)

idioms = [
    item for item in all_idioms
    if item.get("context") != "Context generation failed"
]

texts = [
    f"{item['idiom']}: {item['definition']} Context: {item['context']}"
    for item in idioms
]

embeddings = embedder.encode(
    texts,
    convert_to_tensor=False,
    show_progress_bar=True,
    normalize_embeddings=True
)

np.save(EMBED_FILE, embeddings)

print(f"✅ Saved {len(embeddings)} embeddings to {EMBED_FILE}")
