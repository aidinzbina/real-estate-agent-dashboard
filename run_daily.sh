#!/usr/bin/env bash
# ─── run_daily.sh ──────────────────────────────────────────────────────────────
# Load your env vars (OPENAI_API_KEY, GMAIL_APP_PASSWORD)
source ~/.zshrc

# Ensure we use the same python3 you installed modules under:
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"

LOG="/Users/aidinbina/Real Estate Agent Project/cron_daily.log"

echo "===== DAILY START $(date) =====" >> "$LOG"

echo "--- Fetch & Archive ---" >> "$LOG"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "/Users/aidinbina/Real Estate Agent Project/News Fetcher.py" \
  >> "$LOG" 2>&1

echo "--- Store Trend Snapshot ---" >> "$LOG"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "/Users/aidinbina/Real Estate Agent Project/trend_analysis_store.py" \
  >> "$LOG" 2>&1

echo "--- Send Digest Email ---" >> "$LOG"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "/Users/aidinbina/Real Estate Agent Project/send digest.py" \
  >> "$LOG" 2>&1

echo "===== DAILY END   $(date) =====" >> "$LOG"
