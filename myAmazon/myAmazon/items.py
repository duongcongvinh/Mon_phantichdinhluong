# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyamazonItem(scrapy.Item):
    productURL = scrapy.Field()
    productName = scrapy.Field()
    price = scrapy.Field()
    fabricType = scrapy.Field()
    closureType = scrapy.Field()
    countryOfOrigin = scrapy.Field()
    describe = scrapy.Field()
    productDescription = scrapy.Field()
    ratings = scrapy.Field()
    rate = scrapy.Field()
    customersSay = scrapy.Field()