import fileinput
from pymongo import MongoClient

#config = { 'mongoUri' :'176.166.49.201'}
config = { 'mongoUri' :'localhost'}


collection = MongoClient(config['mongoUri'], 27017).rss.rss_feed
links = [link.rstrip('\n') for link in fileinput.input()]
for link in links:
    collection.update_one({"link":link}, {"$set": {'link':link}}, upsert=True)