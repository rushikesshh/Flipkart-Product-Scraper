# Flipkart Product Scraper 🛒

This repository contains two implementations to scrape product details from Flipkart based on search query URLs:

1. **Script 1 (Scrapy-based)**  
2. **Script 2 (Multithreaded requests using `concurrent.futures`)**

Both approaches extract product name, price, ratings, reviews, features, and image links.

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/rushikesshh/Flipkart-Product-Scraper.git

cd Flipkart-Product-Scraper

python -m venv venv

venv\Scripts\activate   # On Windows

# source venv/bin/activate   # On Unix/macOS

pip install -r requirements.txt

```

---

2. **Run Scrapy Spider**

```bash
cd flipkart_products_details_extraction

cd flipkart_scraper

scrapy crawl flipkart_product
```


✅ Output:

Extracted product data : output/products.json

HTML Pages : output/html_pages/

Logs : output/flipkart_spider.log

---

3. **Run Multithreaded Scraper**

```bash

cd flipkart_products_details_extraction

cd beautiful_soup

python multithreaded_scraper.py

```


✅ Output:

Extracted product data : output/products.json

HTML Pages : output/html_pages/

Logs : output/flipkart_spider.log

---

## Performance Comparison


### Scrapy-based Scraper:

**Speed** : Moderate; Scrapy’s asynchronous nature ensures it can handle multiple pages concurrently, but it is more CPU-intensive and slower for a small number of requests compared to multithreading.

**Reliability** : High; Scrapy handles retries and error logging well, ensuring higher reliability when scraping multiple pages.

**Rate-Limiting** : Scrapy is built with rate-limiting in mind and can be easily configured for delays and retries.


### Multithreaded Scraper:

**Speed** : Faster for smaller sets of requests, as multiple threads can work simultaneously. However, it may be slower or inefficient for large-scale scraping due to GIL (Global Interpreter Lock) in Python.

**Reliability** : Moderate; handling of retries and failures is manual and requires custom logic to ensure proper handling.

**Rate-Limiting** : Can be harder to configure to respect rate limits without external tools or manual delays.

---

# Notes


## Error Handling:


Both scrapers implement retries for failed requests. Scrapy’s retry mechanism is built-in, while the multithreaded approach uses custom retry logic.

Logs are generated for both scrapers to track failures and issues during the scraping process.


## Respecting Flipkart’s Rate-Limits:


Both approaches ensure rate-limiting by adding delays between requests (DOWNLOAD_DELAY for Scrapy, manual sleep for multithreading).

The use of proper user-agent headers helps in mimicking real user traffic, reducing the chance of IP blocking.


## Scaling Considerations:


Scrapy is better suited for larger-scale scraping due to its asynchronous nature and more efficient resource handling.

For small-scale scraping or a few pages, the multithreaded approach might be sufficient and simpler to implement.

