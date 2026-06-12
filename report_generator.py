import requests
from bs4 import BeautifulSoup
import pandas as pd

print("Starting multi-page report generation...")

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

data = []

total_pages = int(input("Enter number of pages to scrape: "))
for page in range(1, total_pages + 1):
    print(f"Scraping page {page}...")
    
    url = base_url.format(page)
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]

        price_text = book.find("p", class_="price_color").text
        price_clean = ''.join(c for c in price_text if c.isdigit() or c == '.')
        price = float(price_clean)

        data.append({
            "Title": title,
            "Price": price,
            "Page": page
        })

df = pd.DataFrame(data)

total_books = len(df)
average_price = round(df["Price"].mean(), 2)
max_price = df["Price"].max()
min_price = df["Price"].min()

summary = {
    "Total Books": total_books,
    "Average Price": average_price,
    "Highest Price": max_price,
    "Lowest Price": min_price
}

df.to_csv("report_data.csv", index=False)
pd.DataFrame([summary]).to_csv("summary_report.csv", index=False)

print("Multi-page report generated successfully.")
print("\nReport Summary")
print("----------------------")
for key, value in summary.items():
    print(f"{key}: {value}")