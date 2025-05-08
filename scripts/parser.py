from bs4 import BeautifulSoup
import requests
import os
import re

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_site_bs4(url, output_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'a'])
    texts = [clean_text(tag.get_text()) for tag in tags if clean_text(tag.get_text())]

    full_text = '\n'.join(texts)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"[✓] BS4 збережено: {output_path}")

def parse_site_selenium(url, output_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'a'])
    texts = [clean_text(tag.get_text()) for tag in tags if clean_text(tag.get_text())]

    full_text = '\n'.join(texts)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"[✓] Selenium збережено: {output_path}")

if __name__ == "__main__":
    parse_site_bs4("https://lpnu.ua/ikni", "data/raw/ikni.txt")
    parse_site_selenium("https://aidept.com.ua/", "data/raw/sshi.txt")