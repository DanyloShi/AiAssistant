from assistant_core import init_db, get_cached_response, save_response, search_similar_chunks, build_prompt
import ollama

def main():
    init_db()

    while True:
        query = input("🧑 Запит: ").strip()
        if query.lower() in ['exit', 'вихід']:
            break

        cached = get_cached_response(query)
        if cached:
            print("\n🧠 З кешу:\n" + cached + "\n")
            continue

        chunks = search_similar_chunks(query)
        if not chunks:
            from google_fallback import search_duckduckgo
            response = search_duckduckgo(query)
            save_response(query, response)
            print("\n🌐 DuckDuckGo:\n" + response + "\n")
            continue

        prompt = build_prompt([chunk for chunk, _ in chunks], query)
        response = ollama.chat(
            model='llama3',
            messages=[{"role": "user", "content": prompt}]
        )['message']['content']

        save_response(query, response)
        print("\n🤖 Відповідь:\n" + response + "\n")

if __name__ == "__main__":
    main()