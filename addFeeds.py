import fileinput
from pymongo import MongoClient

collection = MongoClient('localhost', 27017).rss.rss_feed
for feed in fileinput.input():
    collection.update_one({"feed":feed}, {"$set": {'feed':feed}}, upsert=True)