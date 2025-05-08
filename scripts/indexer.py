from sentence_transformers import SentenceTransformer
import chromadb
import os

CHUNK_SIZE = 500
DATA_DIR = "data/raw"
DB_DIR = "embeddings"

def chunk_text(text, size):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

def index_file(file_path, collection, model):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    chunks = chunk_text(text, CHUNK_SIZE)
    embeddings = model.encode(chunks).tolist()

    for i, chunk in enumerate(chunks):
        chunk_id = f"{os.path.relpath(file_path, DATA_DIR)}_{i}"
        collection.add(
            documents=[chunk],
            ids=[chunk_id],
            embeddings=[embeddings[i]],
            metadatas=[{"source": file_path}]
        )

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name="ikni_rag")

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                index_file(file_path, collection, model)

    print("[✓] Індексація завершена!")

if __name__ == "__main__":
    main()