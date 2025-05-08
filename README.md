# 🤖 AiAssistant — RAG-Based LLM Assistant for University Websites

A local AI assistant built for the visitors of the [Institute of Computer Sciences and Information Technologies](https://lpnu.ua/ikni) and [Department of Artificial Intelligence Systems](https://aidept.com.ua) (Lviv Polytechnic National University).  

This project uses **RAG (Retrieval-Augmented Generation)** and a local **LLaMA 3** model to provide accurate, contextual, and real-time answers based on public university website data and uploaded datasets.

---

## 🚀 Features

- 🧠 **RAG pipeline** (semantic search + LLM answers)
- 📚 Extracts and indexes data from university websites and uploaded datasets
- 📂 Supports `.txt`, `.csv`, `.json`, `.xlsx`, `.pdf`
- ⚡ Fast answers using **cached** responses (SQLite)
- 🌐 **Web fallback**: uses DuckDuckGo search when internal context fails
- 💬 **Telegram bot** with real-time chat interface
- 💾 Works entirely offline with local Ollama models

---

## 🧱 Tech Stack

| Area        | Technology                          |
|-------------|-------------------------------------|
| Model       | [`llama3`](https://ollama.com) via Ollama |
| Embeddings  | [`sentence-transformers`](https://www.sbert.net/) |
| Vector DB   | [`ChromaDB`](https://www.trychroma.com) |
| Web Search  | [`DuckDuckGo Instant API`](https://duckduckgo.com/api) |
| Telegram Bot| [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) |
| Dataset Support | `pandas`, `PyMuPDF`, `json` |
| Caching     | SQLite3                             |
| Language    | Python 3.10+                        |

---

## ⚙️ Installation

```bash
git clone https://github.com/DanyloShi/AiAssistant.git
cd AiAssistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠️ Setup & Usage

### 🔹 1. Run Ollama

Download Ollama: https://ollama.com  
Then run:

```bash
ollama run llama3
```

### 🔹 2. Crawl university websites

```bash
python scripts/parser_recursive.py
```

### 🔹 3. Create vector database

```bash
python scripts/indexer.py
```

### 🔹 4. Add custom datasets

Put your `.txt`, `.csv`, `.json`, `.xlsx`, or `.pdf` files into:

```
data/datasets/
```

Then run:

```bash
python scripts/dataset_loader.py
```

✅ Only new chunks will be indexed (duplicate-safe).

### 🔹 5. Launch assistant in terminal

```bash
python scripts/assistant.py
```

---

## 💬 Telegram Bot

### ✅ Prerequisites

1. Create a bot with [@BotFather](https://t.me/BotFather)
2. Save the token in `.env` file:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### ▶️ Run the bot

```bash
python scripts/bot.py
```

Ask questions directly in Telegram! Replies are generated via RAG and LLaMA 3.

---

## 💡 Example Queries

| Input                              | Behavior                          |
|-----------------------------------|-----------------------------------|
| `Who is the dean of IKNI?`        | Uses RAG or DuckDuckGo fallback   |
| `Where to apply for AI systems?`  | Semantic match from official docs |
| `Weather in Lviv tomorrow`        | Triggers web fallback             |
| `exit`                            | Ends the assistant                |

---

## 📁 Project Structure

```
AiAssistant/
├── scripts/
│   ├── assistant_core.py
│   ├── assistant.py
│   ├── bot.py
│   ├── cache.py
│   ├── google_fallback.py
│   ├── parser_recursive.py
│   ├── indexer.py
│   ├── dataset_loader.py
├── data/
│   ├── raw/
│   └── datasets/           # 📂 Your datasets go here
├── embeddings/
├── cache/
├── .env
├── requirements.txt
└── README.md
```

---

## 📌 Roadmap

- [x] Core: Semantic search + LLM generation
- [x] DuckDuckGo fallback for unseen queries
- [x] Caching system to avoid repetition
- [x] Telegram bot support
- [x] Dataset support: CSV, TXT, PDF, JSON, XLSX
- [ ] 🧾 Admin feedback loop (teach assistant)
- [ ] 🌐 Streamlit / web interface

---

## 👨‍💻 Author

**Danylo Khomyshyn**  
Lviv Polytechnic, Institute of Computer Science and Information Technologies  
GitHub: [@DanyloShi](https://github.com/DanyloShi)

---

## 🧠 Inspired by

- Llama 3 by Meta
- LangChain & Haystack
- Ollama & ChromaDB

---

Feel free to ⭐ star the project or fork it for your own university assistant!