#!/usr/bin/env python3
"""Fetch World Bank annual GDP growth and real GDP levels; write JSON/CSV snapshots."""
import csv, json, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_annual_percent",
    "NY.GDP.MKTP.KD": "real_gdp_constant_usd",
}
def fetch(code):
    page, pages, rows = 1, 1, []
    while page <= pages:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000&page={page}"
        req = Request(url, headers={"User-Agent": "WB-GDP-Monitor/1.0"})
        with urlopen(req, timeout=60) as response:
            payload = json.load(response)
        if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
            break
        pages = int(payload[0].get("pages", 1))
        for r in payload[1]:
            if r.get("countryiso3code") and r.get("date") and r.get("value") is not None:
                rows.append({
                    "country_code": r["countryiso3code"],
                    "country": (r.get("country") or {}).get("value", ""),
                    "year": int(r["date"]),
                    "indicator": code,
                    "indicator_name": INDICATORS[code],
                    "value": r["value"],
                    "source_updated_at": r.get("date") or "",
                })
        page += 1
        time.sleep(0.15)
    return rows

def main():
    records = []
    for code in INDICATORS:
        print("Fetching", code)
        records.extend(fetch(code))
    snapshot = {
        "source": "World Bank Indicators API v2 / World Development Indicators",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "indicators": INDICATORS,
        "records": records,
    }
    (OUT / "gdp_growth.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "gdp_growth.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["country_code","country","year","indicator","indicator_name","value","source_updated_at"])
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} observations.")
if __name__ == "__main__":
    main()
