#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId


from sklearn.feature_extraction.text import CountVectorizer

import nltk
try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords

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
docs = list( rss_item.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}) )
docsFR = list(filter(lambda doc : doc['detectLanguage']['detected'] == 'fr',docs))
docsEN = list(filter(lambda doc : doc['detectLanguage']['detected'] == 'en',docs))

Xfr = CountVectorizer(" ".join(docsFR),stop_words=stopwords.words('french'))
Xen = CountVectorizer(" ".join(docsEN),stop_words=stopwords.words('english'))

count_vectorizer.insert_one({'Xfr':Xfr,'Xen':Xen,'hash':make_hash(*ids),'date':datetime.utcnow()})

client.close()
