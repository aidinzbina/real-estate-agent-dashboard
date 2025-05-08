#!/usr/bin/env bash
# Load your env vars (API key, Gmail pw)
source ~/.zshrc

# Timestamp for debugging
echo "===== send_digest START $(date) =====" >> cron_send_digest.log

# Run the Python digest script, capturing both stdout and stderr
python3 ~/Real\ Estate\ Agent\ Project/send\ digest.py \
  >> cron_send_digest.log 2>&1

echo "===== send_digest END   $(date) =====" >> cron_send_digest.log
