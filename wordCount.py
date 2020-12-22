#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from os import environ

from itertools import *
from more_itertools import *
from functools import partial
from string import ascii_lowercase
from operator import *


from string import ascii_lowercase
from toolz.curried import map,reduce,filter
from toolz import pipe,compose,identity,flip

from unidecode import unidecode

stopsize = 25

from collections import Counter

wordcount = lambda words : map_reduce(words,lambda x:x ,lambda x : 1,sum)

def attack(doc):
    # TODO: this field could be configurable
    wc = Counter(pipe(
        doc['contentCleaner']['cleanContent'],
        str.lower,
        unidecode,
        flip(split_at)(lambda char : char not in ascii_lowercase),
        filter(len),
        map(''.join)
    ))
    
    # rss_items = [make_item(url, post) for post in feed.entries]
    # TODO: check that connection actually append
    
    rss_item.update_one({'_id': doc['_id']}, {"$set": {'wordCount':wc}}, upsert=True)



client = MongoClient(environ['MONGO_URI'] , 27017)

rss_item = client.rss.rss_item

ids = [ line.rstrip('\n') for line in fileinput.input() ]
docs = list( rss_item.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))
for doc in docs :
    attack(doc)

client.close()
