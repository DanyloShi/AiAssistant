from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
from cache import init_db, get_cached_response, save_response

DB_DIR = "embeddings"
TOP_K = 3
SIM_THRESHOLD = 0.4

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="ikni_rag")

def search_similar_chunks(query, top_k=TOP_K):
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
    return [(doc, score) for doc, score in zip(documents, sims) if score >= SIM_THRESHOLD]

def build_prompt(context_chunks, user_query):
    context = "\n---\n".join(context_chunks)
    return f"""
You are an AI assistant for IKNI (Institute of Computer Sciences and Information Technologies) of Lviv Polytechnic.
Answer in Ukrainian using only the information in the context below.

Context:
{context}

Question:
{user_query}

Answer:
""".strip()