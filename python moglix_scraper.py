# Moglix 50 Products Reviews Scraper
# Scrapes category → 50 products → all reviews → CSV export
# Usage: Change CATEGORY_URL below and run

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

def scrape_moglix_category_products(category_url, max_products=50):
    """Step 1: Get 50 product URLs from category"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("🔍 Extracting product links from category...")
    response = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Common Moglix product link selectors
    product_links = []
    product_elems = soup.find_all(['a', 'div'], class_=re.compile(r'product|prod|item|card'))
    
    for elem in product_elems[:max_products*2]:  # Extra buffer
        link = elem.get('href') or elem.find('a', href=True)
        if link and 'mp/' in str(link):
            full_url = urljoin(category_url, link)
            product_links.append(full_url)
    
    return product_links[:max_products]

def scrape_all_moglix_reviews(category_url, max_products=50):
    """Complete pipeline: Category → Products → Reviews"""
    all_reviews = []
    
    # Get product URLs
    product_urls = scrape_moglix_category_products(category_url, max_products)
    print(f"✅ Found {len(product_urls)} product URLs")
    
    for i, product_url in enumerate(product_urls, 1):
        print(f"\n🚀 Processing Product {i}/{len(product_urls)}: {product_url}")
        
        try:
            # Get reviews from this product (using previous function)
            product_reviews = scrape_moglix_reviews(product_url, max_pages=3)
            all_reviews.extend(product_reviews)
            print(f"   → Got {len(product_reviews)} reviews")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(3)  # Longer delay between products
    
    return all_reviews

# USAGE - PUT CATEGORY URL HERE!
CATEGORY_URL = "https://www.moglix.com/power-tools"  

if __name__ == "__main__":
    print("🎯 Moglix 50 Products Reviews Scraper Starting...")
    reviews_data = scrape_all_moglix_reviews(CATEGORY_URL, max_products=50)
    
    if reviews_data:
        df = pd.DataFrame(reviews_data)
        filename = f"moglix_50products_reviews_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n🎉 SUCCESS! Saved {len(reviews_data)} reviews from 50 products!")
        print(f"📁 File: {filename}")
        print("\n📊 Summary:")
        print(df.groupby('product_name').size().head())
    else:
        print("❌ No data found")
