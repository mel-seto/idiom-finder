"""
This script needs to be re-run each time EMBEDDING_MODEL is updated.
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer

from constants import EMBEDDING_MODEL


INPUT_FILE = "data/idioms-and-definitions.json"
EMBED_FILE = "data/idiom_embeddings.npy"

embedder = SentenceTransformer(EMBEDDING_MODEL)

# Load idioms
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# E5 models expect "passage:" for documents and "query:" for user inputs
prefixed_corpus = [f"passage: {text}" for text in corpus]

embeddings = embedder.encode(
    prefixed_corpus,
    convert_to_tensor=False,
    show_progress_bar=True,
    normalize_embeddings=True  # important for cosine similarity
)

np.save(EMBED_FILE, embeddings)
print(f"✅ Saved {len(embeddings)} embeddings to {EMBED_FILE}")