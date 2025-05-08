#!/usr/bin/env python3
import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from openai import OpenAI

import os
print("DEBUG: OPENAI_API_KEY:", repr(os.getenv("OPENAI_API_KEY")))

# ——— Load secrets from environment ———
OPENAI_API_KEY     = os.getenv('OPENAI_API_KEY')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")
if not GMAIL_APP_PASSWORD:
    raise RuntimeError("Missing GMAIL_APP_PASSWORD environment variable")

# ——— Initialize OpenAI client ———
client = OpenAI(api_key=OPENAI_API_KEY)

# ——— Configuration ———
DB_PATH    = '/Users/aidinbina/Real Estate Agent Project/real_estate_news.db'
GMAIL_USER = 'aidinzbina@gmail.com'
TO_EMAILS  = ['aidinzbina@gmail.com', 'cooperp2024@gmail.com', 'cfp7437@nyu.edu']


if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY environment variable")
if not GMAIL_APP_PASSWORD:
    raise RuntimeError("Missing GMAIL_APP_PASSWORD environment variable")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ——— Helpers ———
def fetch_trend_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT keyword, week_count
        FROM trend_snapshots
        WHERE date = ?
        ORDER BY week_count DESC
        LIMIT 10
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "<p>No trend data available yet.</p>"

    html = ["<h2>📊 Weekly Trend Highlights:</h2><ul>"]
    for keyword, count in rows:
        if count > 0:
            html.append(f"<li><strong>{keyword}</strong>: {count} mentions this week</li>")
    html.append("</ul>")
    return "\n".join(html)

def generate_synthesis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT ai_summary
        FROM summaries
        WHERE date(timestamp) = ?
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "<p>No articles to synthesize today.</p>"

    combined = "\n\n".join(r[0] for r in rows)
    prompt = (
        "Based on the following real estate news summaries, "
        "provide a 3–5 sentence synthesis highlighting the main themes, trends, or takeaways:\n\n"
        f"{combined}"
    )

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300
    )
    synthesis = resp.choices[0].message.content.strip()
    return f"<h2>🧠 News Synthesis:</h2><p>{synthesis}</p>"

# ——— Build the email ———
# Fetch today's articles
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
today_date = datetime.now().strftime("%Y-%m-%d")

cursor.execute('''
    SELECT source, title, link, ai_summary
    FROM summaries
    WHERE date(timestamp) = ?
    ORDER BY timestamp DESC
''', (today_date,))
rows = cursor.fetchall()
conn.close()

# Construct HTML body
if not rows:
    body = f"<h2>📰 Real Estate Digest for {today_date}</h2><p>No new articles found today.</p>"
else:
    body = f"<h2>📰 Real Estate Digest for {today_date}</h2>"
    for source, title, link, summary in rows:
        body += f"""
        <div style='margin-bottom:20px; padding:10px; border-bottom:1px solid #ccc;'>
            <strong>Source:</strong> {source}<br>
            <strong>Title:</strong> {title}<br>
            <strong>Link:</strong> <a href='{link}'>{link}</a><br>
            <strong>AI Summary:</strong> {summary}
        </div>
        """

# Add synthesis + trends
body += generate_synthesis()
body += fetch_trend_summary()
body += "<p>✅ End of digest.</p>"

# Prepare and send the email
msg = MIMEText(body, 'html')
msg['Subject'] = f"📰 Real Estate News Digest 📅 {today_date}"
msg['From']    = GMAIL_USER
msg['To']      = ', '.join(TO_EMAILS)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAILS, msg.as_string())
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")


