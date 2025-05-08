import sqlite3
import os

DB_PATH = "cache/assistant_cache.db"

def init_db():
    os.makedirs("cache", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            query TEXT PRIMARY KEY,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_cached_response(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT response FROM cache WHERE query = ?', (query,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def save_response(query, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO cache (query, response) VALUES (?, ?)', (query, response))
    conn.commit()
    conn.close()