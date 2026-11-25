# Website Uptime Monitor

Check one or more websites, record HTTP status and response time, and append results to a CSV log.

## Requirements
- Python 3.10+
- requests

## Install and run
```bash
pip install -r requirements.txt
python main.py https://example.com https://github.com
```

Results are appended to `uptime.csv`. A successful HTTP response is considered reachable even when its status is 4xx/5xx; inspect the recorded status code for application-level health. The tool makes one check per URL per run; schedule it with cron or Task Scheduler for recurring monitoring.

## Responsible use
Only monitor websites you are authorized to check. Use reasonable intervals and avoid aggressive polling.
