# practice.py
# ─────────────────────────────────────────────
# Practice scraper on books.toscrape.com
# This is a safe site built for scraping practice
# Delete this file before handing to client
# ─────────────────────────────────────────────

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def practice_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False so you can WATCH it
        page = browser.new_page()

        print("[Practice] Opening browser...")
        page.goto("http://books.toscrape.com", wait_until="networkidle")
        page.wait_for_timeout(2000)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        books = []
        items = soup.select("article.product_pod")

        for item in items:
            book = {
                "title": item.select_one("h3 a")["title"],
                "price": item.select_one(".price_color").get_text(strip=True),
                "rating": item.select_one("p.star-rating")["class"][1],
            }
            books.append(book)

        print(f"\n[Practice] Found {len(books)} books\n")
        for b in books:
            print(f"  {b['title']} | {b['price']} | {b['rating']} stars")

        browser.close()

if __name__ == "__main__":
    practice_scrape()