import ollama

EMBEDDING_MODEL = "bge-m3:latest"
LANGUAGE_MODEL = "llama3.2:latest"

# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]
VECTOR_DB = []


def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)["embeddings"][0]
    VECTOR_DB.append((chunk, embedding))


if __name__ == "__main__":
    sample = "九死一生"
    add_chunk_to_database(sample)
    print(VECTOR_DB)
