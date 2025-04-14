# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonVacancy(scrapy.Item):
    name = scrapy.Field()
    company = scrapy.Field()
    technologies = scrapy.Field()
    posted_date = scrapy.Field()
