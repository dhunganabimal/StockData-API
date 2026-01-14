import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .database import sessionLocal
from .models import StockData


def to_float(value: str):

    if not value:
        return None

    value = value.replace(",", "").replace("+", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


def scrape_website():
    url = "https://merolagani.com/latestmarket.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    extracted_data = []

    table = soup.find("table", class_="table table-hover live-trading sortable")
    if not table:
        raise Exception("Market table not found")

    rows = table.tbody.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        stock_name = cols[0].get_text(strip=True)
        ltp = to_float(cols[1].get_text(strip=True))
        change = to_float(cols[2].get_text(strip=True))

        extracted_data.append({
            "stock_name": stock_name,
            "ltp": ltp,
            "change": change
        })

    return extracted_data


def scrape_and_save_task():
    print("Starting scheduled scrape...")

    try:
        data = scrape_website()
    except Exception as e:
        print(f"Scraping failed: {e}")
        return

    db: Session = sessionLocal()

    try:
        db.query(StockData).delete()

        for item in data:
            db_item = StockData(
                stock_name=item["stock_name"],
                ltp=item["ltp"],
                change=item["change"]
            )
            db.add(db_item)

        db.commit()
        print(f" Successfully saved {len(data)} records")

    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")

    finally:
        db.close()
