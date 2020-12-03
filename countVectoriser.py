#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
import hashlib


from os import environ 

def make_hash(*values):
    return hashlib.sha1(''.join(values).encode()).hexdigest()

def attack(doc):
    rss_item.update_one({'_id': doc['_id']}, {'$set':{'lastCheck':datetime.utcnow()}}, upsert=True)
    return doc['contentCleaner']['cleanContent']

client = MongoClient(environ['MONGO_URI'] , 27017)

rss_item = client.rss.rss_item
count_vectorizer = client.rss.count_vectorizer

ids = [ line.rstrip('\n') for line in fileinput.input() ]
docs = list( rss_item.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))

X = CountVectorizer().fit_transform( ( attack(doc) for doc in docs) )
count_vectorizer.insert_one({'X':X,'hash':make_hash(*ids),'date':datetime.utcnow()})

client.close()
