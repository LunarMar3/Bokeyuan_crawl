# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BokeyuanItem(scrapy.Item):
    title = scrapy.Field()
    title_url=scrapy.Field()
    author=scrapy.Field()
    pubtime=scrapy.Field()
    support=scrapy.Field()
    comments=scrapy.Field()
    view=scrapy.Field()
