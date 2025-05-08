import os, smtplib

user = "aidinzbina@gmail.com"
pwd  = os.getenv("GMAIL_APP_PASSWORD")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(user, pwd)
    print("✅ SMTP login successful!")
except Exception as e:
    print("❌ SMTP login failed:", e)