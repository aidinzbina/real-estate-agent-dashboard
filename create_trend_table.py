import sqlite3

# Connect to the database
conn = sqlite3.connect('real_estate_news.db')
cursor = conn.cursor()

# Create the trend_snapshots table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trend_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        date TEXT,
        day_count INTEGER,
        week_count INTEGER,
        month_count INTEGER,
        year_count INTEGER
    )
''')

conn.commit()
conn.close()

print("✅ trend_snapshots table created successfully.")