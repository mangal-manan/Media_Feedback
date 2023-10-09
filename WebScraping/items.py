# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MongoDbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    Date = scrapy.Field()
    Metadata = scrapy.Field()
    URL = scrapy.Field()
    Website = scrapy.Field()
    Language = scrapy.Field()
    Time = scrapy.Field()
