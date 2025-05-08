#!/usr/bin/env python3
import os
import feedparser
import sqlite3
from datetime import datetime
from openai import OpenAI

print("🚀 Running News Fetcher with Archiving 🚀")

# ——— Configuration ———
DB_PATH = '/Users/aidinbina/Real Estate Agent Project/real_estate_news.db'
CRON_LOG_PATH = '/Users/aidinbina/Real Estate Agent Project/cron_log.txt'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Please set your OPENAI_API_KEY environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)

FEEDS = [
    ("CNBC Real Estate",  "https://www.cnbc.com/id/10000115/device/rss/rss.html"),
    ("The Real Deal",      "https://therealdeal.com/feed/"),
    ("Curbed",             "https://www.curbed.com/rss/index.xml"),
    ("Bisnow NYC",         "https://www.bisnow.com/rss/nyc"),
    ("HousingWire",        "https://www.housingwire.com/rss/"),
    ("Redfin News",        "https://www.redfin.com/news/feed/"),
    ("Inman",              "https://www.inman.com/feed/"),
    ("GlobeSt",            "https://www.globest.com/rss/"),
    ("Mortgage News Daily","https://www.mortgagenewsdaily.com/rss"),
]

# ——— Ensure DB & table exist ———
with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT,
            title       TEXT,
            link        TEXT,
            ai_summary  TEXT,
            timestamp   TEXT
        )
    """)
    conn.commit()

# ——— Fetch, summarize & store ———
for name, url in FEEDS:
    print(f"\n🔗 Fetching from: {name}")
    feed = feedparser.parse(url)
    entries = feed.entries
    print(f"Number of entries found: {len(entries)}")
    if not entries:
        print("⚠️ No entries found—skipping.")
        continue

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        for entry in entries[:5]:  # adjust limit as you like
            title   = entry.get("title", "No title")
            link    = entry.get("link", "")
            summary = entry.get("summary", "No summary available.")
            print(f"\nTitle: {title}\nLink: {link}\nOriginal Summary: {summary}")

            prompt = (
                "Summarize the following real estate news article in 1-2 sentences:\n\n"
                f"Title: {title}\n"
                f"Summary: {summary}"
            )

            try:
                resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )
                ai_summary = resp.choices[0].message.content.strip()
                print("AI Summary:", ai_summary)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO summaries (source, title, link, ai_summary, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, title, link, ai_summary, timestamp))

            except Exception as e:
                print(f"❌ Error summarizing entry: {e}")

        conn.commit()  # one commit per feed

# ——— Write cron log ———
with open(CRON_LOG_PATH, "a") as f:
    f.write(f"{datetime.now().isoformat()}: Ran News Fetcher\n")


