import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse

visited = set()
max_pages = 100

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def save_text(url, text, base_dir):
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_") or "index"
    filename = f"{base_dir}/{path}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def parse_page(url, base_url, base_dir):
    if url in visited or len(visited) > max_pages:
        return
    visited.add(url)

    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'a'])
        text = "\n".join([clean_text(tag.get_text()) for tag in tags if clean_text(tag.get_text())])
        save_text(url, text, base_dir)

        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if next_url.startswith(base_url):
                parse_page(next_url, base_url, base_dir)
    except Exception as e:
        print(f"[!] Помилка: {url} — {e}")

if __name__ == "__main__":
    targets = {
        "ikni": "https://lpnu.ua/ikni",
        "sshi": "https://aidept.com.ua"
    }

    for name, url in targets.items():
        print(f"=== Починаємо обхід: {url} ===")
        parse_page(url, url, f"data/raw/{name}")