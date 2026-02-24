import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

products = []

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

for page in range(1, 6):
    url = BASE_URL.format(page)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
      name = book.h3.a["title"]

    price_text = book.find("p", class_="price_color").text
    price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))

    rating_text = book.find("p", class_="star-rating")["class"][1]
    rating = rating_map.get(rating_text, 0)

    products.append({
        "Name": name,
        "Price": price,
        "Rating": rating
    })

df = pd.DataFrame(products)
df.to_csv("clean_books.csv", index=False)

print("Scraping complete. Data saved to clean_books.csv")