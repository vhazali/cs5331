# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class URLItem(scrapy.Item):
    url = scrapy.Field()
    protocol = scrapy.Field()
    domain = scrapy.Field()
    path = scrapy.Field()
    page = scrapy.Field()
    get_params = scrapy.Field()

class FormItem(scrapy.Item):
    url = scrapy.Field()
    id_attr = scrapy.Field()
    # complete = scrapy.Field()
    # name = scrapy.Field()

class InputItem(scrapy.Item):
    url = scrapy.Field()
    form_id = scrapy.Field()
    complete = scrapy.Field()
    type_attr = scrapy.Field()
    # id_attr = scrapy.Field()
    # name = scrapy.Field()
    # placeholder = scrapy.Field()
