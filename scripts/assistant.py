import chromadb
from sentence_transformers import SentenceTransformer
import ollama
from cache import init_db, get_cached_response, save_response
from google_fallback import search_duckduckgo
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DB_DIR = "embeddings"
TOP_K = 3
SIM_THRESHOLD = 0.4

def search_similar_chunks(query, collection, model, top_k=TOP_K):
    query_emb = model.encode([query])
    results = collection.query(
        query_embeddings=query_emb.tolist(),
        n_results=top_k,
        include=['documents', 'embeddings']
    )

    documents = results.get('documents', [[]])[0]
    embeddings = results.get('embeddings', [[]])[0]

    if not documents or len(embeddings) == 0:
        return []

    sims = cosine_similarity(query_emb, embeddings)[0]
    return list(zip(documents, sims))

def build_prompt(context_chunks, user_query):
    context = "\n---\n".join(context_chunks)
    prompt = f"""
Ти — асистент ІКНІ НУЛП. Відповідай українською мовою. Використовуй лише дані з контексту нижче.

Контекст:
{context}

Питання:
{user_query}

Відповідь:
"""
    return prompt.strip()

def main():
    init_db()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name="ikni_rag")

    while True:
        query = input("🧑 Запит: ").strip()
        if query.lower() in ['exit', 'вихід']:
            break

        cached = get_cached_response(query)
        if cached:
            print("\n🧠 З кешу:\n" + cached + "\n")
            continue

        chunks_with_scores = search_similar_chunks(query, collection, model)
        relevant_chunks = [chunk for chunk, score in chunks_with_scores if score >= SIM_THRESHOLD]

        if not relevant_chunks:
            print("🔍 Немає достатньо релевантного контексту. Шукаю в інтернеті...")
            response = search_duckduckgo(query)
            save_response(query, response)
            print("\n🌐 DuckDuckGo:\n" + response + "\n")
            continue

        prompt = build_prompt(relevant_chunks, query)
        response = ollama.chat(
            model='llama3',
            messages=[{"role": "user", "content": prompt}]
        )['message']['content']

        save_response(query, response)
        print("\n🤖 Відповідь:\n" + response + "\n")

if __name__ == "__main__":
    main()