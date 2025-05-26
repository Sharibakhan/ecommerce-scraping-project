
#Required Libraries:
!pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
book_list = []

for page in range(1, 51):  # 50 pages total
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    books = soup.select(".product_pod")
    
    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        availability = book.select_one(".availability").text.strip()
        rating = book.p.get("class")[1]  # Example: 'One', 'Two', etc.
        product_link = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]
        image_url = "https://books.toscrape.com/" + book.img["src"].replace("../", "")
        
        book_list.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "Product Link": product_link,
            "Image URL": image_url
        })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(book_list)
df.to_csv("books_data.csv", index=False)
print(" Data scraped and saved as books_data.csv")


