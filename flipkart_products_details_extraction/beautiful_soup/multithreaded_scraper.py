import requests
import re
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import sleep
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML

# Custom settings similar to Scrapy settings
DOWNLOAD_DELAY = 3  # Adjust delay to avoid being blocked
RETRY_TIMES = 3  # Retry 3 times
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
LOG_FILE = 'output/flipkart_spider.log'

# Log function to simulate Scrapy's logging
def log(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{message}\n")
    print(message)

# Function to fetch and save the page content
def fetch_and_save_page(url):
    retries = 0
    while retries < RETRY_TIMES:
        try:
            headers = {
                "User-Agent": USER_AGENT,
                "Referer": "https://www.flipkart.com/"
            }
            response = requests.get(url, headers=headers)

            # If response is not successful, log and retry
            if response.status_code != 200:
                log(f"Failed to retrieve {url} with status code {response.status_code}")
                retries += 1
                log(f"Retrying {url} ({retries}/{RETRY_TIMES})")
                sleep(DOWNLOAD_DELAY)
                continue

            # Extract query parameters from URL
            url_params = re.search(r'q=([^&]+)&page=(\d+)', url)
            if url_params:
                query_param = url_params.group(0)  # e.g., "q=iphone&page=4"
                save_dir = Path("output/html_pages")
                save_dir.mkdir(parents=True, exist_ok=True)
                filename = save_dir / f"flipkartproduct_{query_param}.html"

                # Save the page content to file
                with open(filename, 'wb') as f:
                    f.write(response.content)
                    log(f"Saved file {filename}")
            else:
                log(f"Failed to parse URL parameters for {url}")

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract product details
            product_cards = soup.find_all('div', class_='cPHDOP col-12-12')
            log(f"Extracted {len(product_cards)} products from {url}")

            for card in product_cards:
                title = card.select_one('div.KzDlHZ').get_text(strip=True) if card.select_one('div.KzDlHZ') else None
                image = card.select_one('.DByuf4')['src'] if card.select_one('.DByuf4') else None
                rating = card.select_one('.XQDdHH').get_text(strip=True) if card.select_one('.XQDdHH') else None
                price = card.select_one('.Nx9bqj._4b5DiR').get_text(strip=True) if card.select_one('.Nx9bqj._4b5DiR') else None
                features = [feature.get_text(strip=True) for feature in card.select('ul.G4BRas > li')]
                ratings_reviews = [span.get_text(strip=True) for span in card.select('span.Wphh3N span span')]
                
                if len(ratings_reviews) >= 3:
                    ratings_count = ratings_reviews[0]
                    reviews_count = ratings_reviews[2]
                else:
                    ratings_count, reviews_count = None, None

                # Prepare product data
                product_info = {
                    'product_name': title,
                    'image_link': image,
                    'rating': rating,
                    'ratings_count': ratings_count,
                    'reviews_count': reviews_count,
                    'features': features,
                    'price': price,
                    'product_url': url
                }

                # Save the product info
                all_products.append(product_info)

            break
        except Exception as e:
            retries += 1
            log(f"Error occurred while processing {url}: {str(e)}")
            if retries < RETRY_TIMES:
                log(f"Retrying {url} ({retries}/{RETRY_TIMES})")
                sleep(DOWNLOAD_DELAY)
            else:
                log(f"Skipping {url} after {RETRY_TIMES} retries")

# Function to handle the multithreaded processing and execute fetch_and_save_page for each URL
def process_urls(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch_and_save_page, urls)

# Main script
if __name__ == "__main__":
    all_products = []

    # Load URLs from file
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # Start multithreaded processing
    process_urls(urls)

    # After scraping, save the combined product data to JSON file
    Path("output").mkdir(exist_ok=True)
    file_path = 'output/products.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)
    log(f"Saved combined product data to {file_path}")
