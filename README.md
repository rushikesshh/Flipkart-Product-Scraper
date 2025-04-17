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


