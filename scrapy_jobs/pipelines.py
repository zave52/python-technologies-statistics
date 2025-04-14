# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.exporters import CsvItemExporter


class CsvWriterPipeline:
    def __init__(self) -> None:
        self.files = {}
        self.exporters = {}

    def open_spider(self, spider: scrapy.Spider) -> None:
        os.makedirs('output', exist_ok=True)

        output_file = f"output/{spider.name}_vacancies.csv"
        self.files[spider.name] = open(output_file, "wb")
        self.exporters[spider.name] = CsvItemExporter(self.files[spider.name])
        self.exporters[spider.name].start_exporting()

    def close_spider(self, spider: scrapy.Spider) -> None:
        if spider.name in self.exporters:
            self.exporters[spider.name].finish_exporting()
            self.files[spider.name].close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        self.exporters[spider.name].export_item(item)
        return item
