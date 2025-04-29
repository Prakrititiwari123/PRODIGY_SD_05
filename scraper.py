import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Website ka URL
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Step 2: Data store karne ke liye list banayein
all_products = []

# Step 3: Loop through multiple pages
for page_num in range(1, 6):  # pehle 5 pages scrape karein
    url = base_url.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 4: Har product ka container dhundhein
    products = soup.find_all('article', class_='product_pod')

    for product in products:
        name = product.h3.a['title']  # product name
        price = product.find('p', class_='price_color').text.strip()  # price
        rating_class = product.p['class'][1]  # star rating (string: One, Two, etc.)

        # Rating string ko number mein convert karo
        rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_dict.get(rating_class, 0)

        # Step 5: Data ko dictionary mein store karo
        all_products.append({
            'Name': name,
            'Price': price,
            'Rating': rating
        })

# Step 6: Pandas se CSV file banaayein
df = pd.DataFrame(all_products)
df.to_csv('products.csv', index=False, encoding='utf-8')

print("✅ Data CSV file mein save ho gaya: products.csv")
