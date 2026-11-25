"""One-shot website availability checker with CSV history."""
import argparse, csv, time
from datetime import datetime, timezone
from pathlib import Path
import requests

LOG = Path(__file__).with_name("uptime.csv")

def check(url, timeout=10):
    started = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True,
                                headers={"User-Agent": "PortfolioUptimeMonitor/1.0"})
        return response.status_code, round((time.perf_counter()-started)*1000, 2), ""
    except requests.RequestException as exc:
        return "", round((time.perf_counter()-started)*1000, 2), str(exc)

def record(url, status, latency, error):
    new_file = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(["checked_at_utc", "url", "status_code", "latency_ms", "error"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), url, status, latency, error])

def main():
    parser = argparse.ArgumentParser(description="Check website reachability and log results.")
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    for url in args.urls:
        if not url.startswith(("http://", "https://")):
            parser.error(f"URL must start with http:// or https://: {url}")
        status, latency, error = check(url, args.timeout)
        record(url, status, latency, error)
        result = f"HTTP {status}" if status != "" else f"ERROR {error}"
        print(f"{url}: {result} ({latency} ms)")
    print(f"History saved to {LOG}")

if __name__ == "__main__":
    main()
