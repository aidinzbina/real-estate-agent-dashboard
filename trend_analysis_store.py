import sqlite3
from collections import Counter
from datetime import datetime, timedelta

# Database path
DB_PATH = 'real_estate_news.db'

# Keywords to track
KEYWORDS = [
    # Macro & residential
    "mortgage rate", "interest rate", "rate hike", "rate cut", "inflation",
    "housing demand", "housing supply", "foreclosure", "eviction", "delinquency",
    "price correction", "new construction", "refinance", "NYC market",
    "housing boom", "housing slowdown", "housing crash", "housing recovery",
    "housing bubble", "multifamily", "apartment rents", "rental market",
    "affordable housing", "rent stabilization",

    # Office/commercial
    "office vacancy", "return to office", "remote work", "hybrid work",
    "office lease", "sublease", "office absorption", "coworking", "office conversion",

    # CRE + retail/industrial
    "CRE market", "cap rate", "net lease", "rent growth", "retail vacancy",
    "warehouse demand", "e-commerce boom", "distressed assets", "capital markets",
    "commercial mortgage-backed securities", "real estate fund", "REIT"
]

def fetch_summaries_in_range(cursor, since_date):
    cursor.execute("""
        SELECT ai_summary FROM summaries
        WHERE DATE(timestamp) >= DATE(?)
    """, (since_date,))
    return [row[0].lower() for row in cursor.fetchall()]

def count_keywords(summaries, keywords):
    counts = Counter()
    for summary in summaries:
        for keyword in keywords:
            if keyword.lower() in summary:
                counts[keyword] += 1
    return counts

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📊 Storing trend snapshot for: {today}\n")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Define date ranges
    date_today = today
    date_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    date_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    date_year = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    # Fetch summaries in each range
    print("🔄 Fetching data...")
    daily_summaries = fetch_summaries_in_range(cursor, date_today)
    weekly_summaries = fetch_summaries_in_range(cursor, date_week)
    monthly_summaries = fetch_summaries_in_range(cursor, date_month)
    yearly_summaries = fetch_summaries_in_range(cursor, date_year)

    # Count trends
    print("📈 Analyzing trends...")
    daily_counts = count_keywords(daily_summaries, KEYWORDS)
    weekly_counts = count_keywords(weekly_summaries, KEYWORDS)
    monthly_counts = count_keywords(monthly_summaries, KEYWORDS)
    yearly_counts = count_keywords(yearly_summaries, KEYWORDS)

    # Store results
    print("💾 Storing snapshot in the database...")
    for keyword in KEYWORDS:
        day_count = daily_counts.get(keyword, 0)
        week_count = weekly_counts.get(keyword, 0)
        month_count = monthly_counts.get(keyword, 0)
        year_count = yearly_counts.get(keyword, 0)

        cursor.execute("""
            INSERT INTO trend_snapshots (keyword, date, day_count, week_count, month_count, year_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (keyword, today, day_count, week_count, month_count, year_count))

    conn.commit()
    conn.close()
    print("\n✅ Trend snapshot stored successfully.\n")

if __name__ == "__main__":
    main()

with open("cron_log.txt", "a") as f:
    f.write(f"{datetime.now()}: Ran News Fetcher\n")
