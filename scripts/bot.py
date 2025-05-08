import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from assistant_core import init_db, get_cached_response, save_response, search_similar_chunks, build_prompt
import ollama

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to AiAssistant! Ask me anything about IKNI or the Department of AI.")

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    cached = get_cached_response(query)
    if cached:
        await update.message.reply_text(f"🧠 From cache:\n\n{cached}")
        return

    chunks = search_similar_chunks(query)
    if not chunks:
        from google_fallback import search_duckduckgo
        response = search_duckduckgo(query)
        save_response(query, response)
        await update.message.reply_text(f"🌐 DuckDuckGo:\n\n{response}")
        return

    prompt = build_prompt([chunk for chunk, _ in chunks], query)
    response = ollama.chat(
        model='llama3',
        messages=[{"role": "user", "content": prompt}]
    )['message']['content']

    save_response(query, response)
    await update.message.reply_text(f"🤖 {response}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))
    app.run_polling()

if __name__ == "__main__":
    main()