# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def get_price(price_str):
    price = price_str.replace(' ', '')
    if price.isdigit():
        return int(price)
    return price

class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(get_price))
    pictures = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    parameters = scrapy.Field()
    id = scrapy.Field()
