import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import fitz

CHUNK_SIZE = 500
DATASET_DIR = "data/datasets"
DB_DIR = "embeddings"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="ikni_rag")

def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i+size] for i in range(0, len(text), size)]

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return "\n".join([" | ".join(map(str, row)) for row in df.values])

def parse_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

def parse_xlsx(file_path):
    df = pd.read_excel(file_path)
    return "\n".join([" | ".join(map(str, row)) for row in df.values])

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_file(file_path):
    if file_path.endswith(".txt"):
        content = parse_txt(file_path)
    elif file_path.endswith(".csv"):
        content = parse_csv(file_path)
    elif file_path.endswith(".json"):
        content = parse_json(file_path)
    elif file_path.endswith(".xlsx"):
        content = parse_xlsx(file_path)
    elif file_path.endswith(".pdf"):
        content = parse_pdf(file_path)
    else:
        print(f"❌ Unsupported format: {file_path}")
        return

    chunks = chunk_text(content)
    embeddings = model.encode(chunks).tolist()
    source_name = os.path.basename(file_path)

    existing_ids = set()
    try:
        existing = collection.get(include=["ids"])
        existing_ids = set(existing["ids"])
    except Exception:
        pass  # if empty or not indexed yet

    added = 0
    for i, chunk in enumerate(chunks):
        doc_id = f"{source_name}_{i}"
        if doc_id in existing_ids:
            continue

        collection.add(
            documents=[chunk],
            ids=[doc_id],
            embeddings=[embeddings[i]],
            metadatas=[{"source": source_name}]
        )
        added += 1

    print(f"✅ Indexed {source_name}: {added} new chunks added.")

def main():
    for file in os.listdir(DATASET_DIR):
        path = os.path.join(DATASET_DIR, file)
        if os.path.isfile(path):
            process_file(path)

if __name__ == "__main__":
    main()