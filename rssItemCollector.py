#!/usr/bin/python3

import feedparser
import urllib.request
import hashlib

import fileinput

import asyncio

from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId

from more_itertools import *

from datetime import datetime

from os import environ

def make_hash(*values):
    # TODO: make "hash" algorithme configurable
    return hashlib.sha1(''.join(values).encode()).hexdigest()


def make_kv(post, field):
    # TODO: make default field value configurable
    return (field, post.get(field, ''))


def make_item(source, post):
    # TODO: make rss item fields configurable
    rss_item_kv = [make_kv(post, field) for field in [
        'published', 'title', 'description', 'link', 'language']]
    if source.get('subjects') and len(source['subjects']):
        rss_item_kv.append(('subject', source['subjects'][0]))
    # Here we add extra data to uniquely identify each rss_item
    return dict([*rss_item_kv, ('hash', make_hash(source['link'], *[t[1] for t in rss_item_kv])), ('source', source['link'])])


async def attack(doc):
    try:
        rss_feed.update_one({'_id':doc['_id']},{'$set':{'lastCheck':datetime.utcnow()}})
        feed = feedparser.parse(doc['link'])
        rss_items = [make_item(doc, post) for post in feed.entries]

        # TODO: check that connection actually append
        for item in rss_items:
            bulk.append(item)
            # rss_item.update_one({'hash': item['hash']}, {"$set": item}, upsert=True)
        print("done",doc['link'])
    except:
        print("timeout",doc['link'])
bulk = []
# As HTTP(s) can take time or even never respond, each input url has to treated asynchronously


async def main():
    ids = [ line.rstrip('\n') for line in fileinput.input() ]
    print("initial query sent")
    docs = list(rss_feed.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))
    print("initial query done")
    for batch in chunked(docs,15):
        try:
            await asyncio.gather(*[asyncio.wait_for(attack(doc),timeout=10) for doc in batch])
        except:
            pass
client = MongoClient(environ['MONGO_URI'] , 27017)
rss_feed = client.rss.rss_feed
rss_item = client.rss.rss_item


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
print("bulk writing")
rss_item.bulk_write([UpdateOne({'hash': item['hash']}, {"$set": item}, upsert=True) for item in bulk])

client.close()
