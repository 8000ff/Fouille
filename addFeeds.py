import fileinput
from pymongo import MongoClient
from os import environ 

collection = MongoClient(environ['MONGO_URI']).rss.rss_feed
links = [link.rstrip('\n').split(' ') for link in fileinput.input()]
for link,*subjects in links:
    collection.update_one({"link":link}, {"$set": {'link':link,'subjects':subjects}}, upsert=True)