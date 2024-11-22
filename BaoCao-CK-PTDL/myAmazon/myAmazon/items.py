# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyamazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productURL = scrapy.Field() # định nghĩa các thuộc tính của sản phẩm
    productName = scrapy.Field() # Những thuộc tính này sẽ được sử dụng để lưu trữ dữ liệu sản phẩm
    brand = scrapy.Field()
    price = scrapy.Field()
    fabricType = scrapy.Field()
    closureType = scrapy.Field()
    countryOfOrigin = scrapy.Field()
    customerssay=scrapy.Field()
    productDescription = scrapy.Field()
    ratings = scrapy.Field()
    rate = scrapy.Field()
    about = scrapy.Field()
