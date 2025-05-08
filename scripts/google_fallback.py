import requests

def search_duckduckgo(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("Abstract"):
            return data["Abstract"]
        elif data.get("Answer"):
            return data["Answer"]
        elif data.get("RelatedTopics"):
            related = data["RelatedTopics"]
            if related and "Text" in related[0]:
                return related[0]["Text"]

        return "DuckDuckGo не знайшов чіткої відповіді, але можеш спробувати вручну: https://duckduckgo.com/?q=" + query.replace(" ", "+")
    except Exception as e:
        return f"[!] Помилка пошуку: {e}"