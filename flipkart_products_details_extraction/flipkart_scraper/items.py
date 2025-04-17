import scrapy

class FlipkartScraperItem(scrapy.Item):
    title = scrapy.Field()  # Product title
    price = scrapy.Field()  # Product price
    rating = scrapy.Field()  # Product rating
    ratings_count = scrapy.Field()  # Number of ratings
    reviews_count = scrapy.Field()  # Number of reviews
    image_link = scrapy.Field()  # Link to the product image
    features = scrapy.Field()  # List of product features
    product_url = scrapy.Field()  # URL of the product page