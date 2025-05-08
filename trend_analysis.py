import sqlite3
from collections import Counter

# Path to your database
DB_PATH = 'real_estate_news.db'

# 🔑 Keywords to track (macro + asset class specific)
KEYWORDS = [
    # Macro & residential
    "mortgage rate",
    "interest rate",
    "rate hike",
    "rate cut",
    "inflation",
    "housing demand",
    "housing supply",
    "foreclosure",
    "eviction",
    "delinquency",
    "price correction",
    "new construction",
    "refinance",
    "NYC market",
    "housing boom",
    "housing slowdown",
    "housing crash",
    "housing recovery",
    "housing bubble",
    "multifamily",
    "apartment rents",
    "rental market",
    "affordable housing",
    "rent stabilization",

    # Office/commercial
    "office vacancy",
    "return to office",
    "remote work",
    "hybrid work",
    "office lease",
    "sublease",
    "office absorption",
    "coworking",
    "office conversion",

    # CRE + retail/industrial
    "CRE market",
    "cap rate",
    "net lease",
    "rent growth",
    "retail vacancy",
    "warehouse demand",
    "e-commerce boom",
    "distressed assets",
    "capital markets",
    "commercial mortgage-backed securities",
    "real estate fund",
    "REIT"
]

def fetch_all_summaries(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ai_summary FROM summaries")
    rows = cursor.fetchall()
    conn.close()
    return [row[0].lower() for row in rows]

def analyze_trends(summaries, keywords):
    counts = Counter()
    for summary in summaries:
        for keyword in keywords:
            if keyword.lower() in summary:
                counts[keyword] += 1
    return counts

def main():
    print("\n📊 Real Estate Trend Analysis Report\n")
    summaries = fetch_all_summaries(DB_PATH)
    if not summaries:
        print("No data found in the database.\n")
        return

    trend_counts = analyze_trends(summaries, KEYWORDS)
    total_articles = len(summaries)
    print(f"Total articles analyzed: {total_articles}\n")

    # Organize output: show highest-count keywords first
    sorted_trends = sorted(trend_counts.items(), key=lambda x: x[1], reverse=True)

    for keyword, count in sorted_trends:
        print(f"- '{keyword}': {count} mentions")

    # Show keywords that had 0 mentions (optional)
    zero_mentions = [k for k in KEYWORDS if k not in trend_counts]
    if zero_mentions:
        print("\n🔎 Keywords with 0 mentions:")
        for keyword in zero_mentions:
            print(f"- '{keyword}'")

if __name__ == "__main__":
    main()