import re
import json
import scrapy
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from scrapy.downloadermiddlewares.retry import get_retry_request
from flipkart_scraper.items import FlipkartScraperItem


class FlipkartProductSpider(scrapy.Spider):
    name = 'flipkart_product'
    allowed_domains = ['flipkart.com']
    all_products = []
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Adjust delay to avoid being blocked
        'RETRY_TIMES': 3,  # Retry 3 times
        'CONCURRENT_REQUESTS': 1,  # Limit concurrent requests to respect rate limits
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'output/flipkart_spider.log',  # Set the log file
    }

    def start_requests(self):
        with open('urls.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_failure)

    def parse(self, response):
        url_params = re.search(r'q=([^&]+)&page=(\d+)', response.url)
        if url_params:
            query_param = url_params.group(0)  # e.g., "q=iphone&page=4"
            save_dir = Path("output/html_pages")
            save_dir.mkdir(parents=True, exist_ok=True)
            filename = save_dir / f"flipkartproduct_{query_param}.html"
            filename.write_bytes(response.body)
            self.log(f"Saved file {filename}")

        cards = response.css(".cPHDOP.col-12-12")  # Check current selector
        self.log(f"Extracted {len(cards)} products from {response.url}")

        for card in cards:
            title = card.css("div.KzDlHZ::text").get()
            image = card.css(".DByuf4::attr(src)").get()
            rating = card.css(".XQDdHH::text").get()
            price = card.css(".Nx9bqj._4b5DiR::text").get()
            features = card.css("ul.G4BRas > li::text").getall()
            ratings_reviews = card.css('span.Wphh3N span span::text').getall()
            if len(ratings_reviews) >= 3:
                ratings_count = ratings_reviews[0].strip()
                reviews_count = ratings_reviews[2].strip()
            else:
                ratings_count, reviews_count = None, None

            product_info = {
                'product_name': title,
                'image_link': image,
                'rating': rating,
                'ratings_count': ratings_count,
                'reviews_count': reviews_count,
                'features': [f.strip() for f in features],
                'price': price
            }
            self.all_products.append(product_info)

        item = FlipkartScraperItem()

        # Extract and assign values to item fields
        item['title'] = card.css("div.KzDlHZ::text").get()
        item['price'] = card.css(".Nx9bqj._4b5DiR::text").get()
        item['rating'] = card.css(".XQDdHH::text").get()
        item['ratings_count'] = card.css('span.Wphh3N span span::text').getall()[0].strip()  # Assuming this exists
        item['reviews_count'] = card.css('span.Wphh3N span span::text').getall()[2].strip()  # Assuming this exists
        item['image_link'] = card.css(".DByuf4::attr(src)").get()
        item['features'] = card.css("ul.G4BRas > li::text").getall()
        item['product_url'] = response.url  # Add the current page URL as product URL

        yield item

    def handle_failure(self, failure):
        """Log failed URLs and retry requests if needed."""
        url = failure.request.url
        self.log(f"Request failed for {url}. Reason: {failure.value}")
        
        # Retry the request up to RETRY_TIMES times in case of failure
        retry_request = get_retry_request(failure.request, failure, spider=self)
        if retry_request:
            self.log(f"Retrying {url}...")
            return retry_request
        else:
            self.log(f"Skipping {url} after retries.")

    def closed(self, reason):
        Path("output").mkdir(exist_ok=True)
        file_path = 'output/products.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.all_products, f, ensure_ascii=False, indent=4)
        self.log(f"Saved combined product data to {file_path}")
