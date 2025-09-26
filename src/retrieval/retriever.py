import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
import os

from retrieval import EMBEDDING_MODEL


# HF Dataset URL for the embeddings
EMBED_URL = "https://huggingface.co/datasets/chinese-enthusiasts/idiom-embeddings/resolve/main/idiom_embeddings.npy"
JSON_URL = "https://huggingface.co/datasets/chinese-enthusiasts/idiom-definitions/resolve/main/idioms-and-definitions.json"

# Ensure 'data/' exists
os.makedirs("data", exist_ok=True)
EMBED_FILE = "data/idiom_embeddings.npy"
JSON_FILE = "data/idioms-and-definitions.json"

# Download embeddings if not present
if not os.path.exists(EMBED_FILE):
    print("Downloading embeddings...")
    r = requests.get(EMBED_URL)
    with open(EMBED_FILE, "wb") as f:
        f.write(r.content)
    print("Done.")

# Download idioms JSON if not present
if not os.path.exists(JSON_FILE):
    print("Downloading idioms JSON...")
    r = requests.get(JSON_URL)
    with open(JSON_FILE, "wb") as f:
        f.write(r.content)
    print("Done.")

# Load embeddings
corpus_embeddings = np.load(EMBED_FILE)

# Load idioms
with open(JSON_FILE, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# Initialize embedder
embedder = SentenceTransformer(EMBEDDING_MODEL)

def retrieve_idiom(situation: str, top_k=5):
    query_emb = embedder.encode([situation], convert_to_tensor=False)
    similarities = np.dot(corpus_embeddings, query_emb[0]) / (
        np.linalg.norm(corpus_embeddings, axis=1) * np.linalg.norm(query_emb[0])
    )
    top_idx = np.argsort(similarities)[::-1][:top_k]
    return [corpus[i] for i in top_idx]
