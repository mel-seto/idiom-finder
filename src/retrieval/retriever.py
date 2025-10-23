import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


# from .constants import EMBEDDING_MODEL

EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
RERANKER_MODEL = "BAAI/bge-reranker-base"

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


embedder = SentenceTransformer(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large')
model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')
model.eval()

from sentence_transformers import CrossEncoder
model2 = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

def retrieve_idiom(situation: str, top_k=150):
    print(f"\n\n\n\n\nRetrieving {top_k} idioms for {situation}")
    query_emb = embedder.encode([f"query: {situation}"], normalize_embeddings=True)
    similarities = np.dot(corpus_embeddings, query_emb[0])
    top_idx = np.argsort(similarities)[::-1][:top_k]
    
    pairs = [({situation}, corpus[i]) for i in top_idx]
    
    with torch.no_grad():
        inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
        print(scores)

    # scores = model2.predict(pairs)

    assert len(scores) == len(pairs)
    assert len(scores) == top_k
    with_scores = [(pairs[i][1], scores[i]) for i in range(len(scores))]
    sorted_by_score = list(reversed(sorted(with_scores, key=lambda t: t[1])))

    for thing in sorted_by_score[:10]:
        print(thing)

    return [x[0] for x in sorted_by_score[:10]]


def main():
    retrieve_idiom("working with an old friend")
    retrieve_idiom("mother-in-law is annoying")
    retrieve_idiom("the king is not very nice")
    retrieve_idiom("studies are boring, but my crush cares about my grades")

if __name__ == "__main__":
    main()