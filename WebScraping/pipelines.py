import pymongo
import sys
from .items import MongoDbItem

class MongoDBPipeline:

    collection = 'Data'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = "mongodb://localhost:27017/"
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('mongodb://localhost:27017/'),
            mongodb_db=crawler.settings.get('SIH_Scraped', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(MongoDbItem(item))
        self.db[self.collection].insert_one(data)
        return item