# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exporters import CsvItemExporter


class CsvWriterPipeline:
    def __init__(self) -> None:
        self.file = None
        self.exporter = None

    def open_spider(self, spider: scrapy.Spider) -> None:
        self.file = open("jobs.csv", "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        self.exporter.export_item(item)
        return item
