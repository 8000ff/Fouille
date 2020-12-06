#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from nltk.stem.snowball import SnowballStemmer

from os import environ 

def attack(doc):
    language = {'en':'english','fr':'french'}[doc['detectLanguage']['detected']]
    content = doc['contentCleaner']['cleanContent']

    stemmed = SnowballStemmer(language).stem(content)
    rss_item.update_one({'_id': doc['_id']}, {"$set": {'stemmer':{'stemmed':stemmed}}}, upsert=True)

client = MongoClient(environ['MONGO_URI'] , 27017)

rss_item = client.rss.rss_item

ids = [ line.rstrip('\n') for line in fileinput.input() ]
docs = list( rss_item.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))
for doc in docs :
    attack(doc)

client.close()
