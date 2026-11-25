"""Check HTTP(S) endpoints and optionally save a JSON report."""
import argparse, json, time
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen

def check(url: str, timeout: float = 8.0) -> dict:
    started = time.perf_counter()
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={"User-Agent": "UptimeMonitor/1.0"})
        with urlopen(request, timeout=timeout) as response:
            result.update(status=response.status, online=200 <= response.status < 400)
    except Exception as exc:
        result.update(status=None, online=False, error=str(exc))
    result["response_time_ms"] = round((time.perf_counter() - started) * 1000, 2)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="URLs to check (include https://)")
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--json", dest="output")
    args = parser.parse_args()
    results = [check(url, args.timeout) for url in args.urls]
    for item in results:
        status = item.get("status") or "ERROR"
        print(f'{item["url"]}: {"UP" if item["online"] else "DOWN"} ({status}) - {item["response_time_ms"]} ms')
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle: json.dump(results, handle, indent=2)

if __name__ == "__main__": main()
