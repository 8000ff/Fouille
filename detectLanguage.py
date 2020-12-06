#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from langdetect import detect

from os import environ 

def attack(doc):
    # TODO: this field could be configurable
    try:
        language = detect(' '.join(doc['wordCount'].keys()))
        rss_item.update_one({'_id': doc['_id']}, {"$set": {'detectLanguage':{'detected':language}}}, upsert=True)
    except:
        raise Exception(len(list(doc['wordCount'].keys())))

    # rss_items = [make_item(url, post) for post in feed.entries]
    # TODO: check that connection actually append
    



client = MongoClient(environ['MONGO_URI'] , 27017)

rss_item = client.rss.rss_item

ids = [ line.rstrip('\n') for line in fileinput.input() ]
docs = list( rss_item.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))
for doc in docs :
    attack(doc)

client.close()
