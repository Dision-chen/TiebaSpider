# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class TiebaspiderPipeline:
    def open_spider(self, spider):
        client = MongoClient(host='127.0.0.1', port=27017)
        self.collection = client["spider"]["tieba"]

    def process_item(self, item, spider):
        item["title"] = self.process_content(item["title"])
        print(item)
        self.collection.insert(dict(item))
        return item

    def process_content(self, title):
        title = "".join(title.split())
        return title
