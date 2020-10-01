#!/usr/bin/python3

import feedparser
import urllib.request
import hashlib

import fileinput

import asyncio

from pymongo import MongoClient
from bson.objectid import ObjectId

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
    # Here we add extra data to uniquely identify each rss_item
    return dict([*rss_item_kv, ('hash', make_hash(source, *[t[1] for t in rss_item_kv])), ('source', source)])


async def attack(doc):
    url = doc['link']
    feed = feedparser.parse(url)
    rss_items = [make_item(url, post) for post in feed.entries]
    # TODO: check that connection actually append
    for item in rss_items:
        rss_item.update_one({'hash': item['hash']}, {
                              "$set": item}, upsert=True)


# As HTTP(s) can take time or even never respond, each input url has to treated asynchronously


async def main():
    ids = [ line.rstrip('\n') for line in fileinput.input() ]
    docs = list( rss_feed.find({ "_id": { "$in" : [ObjectId(i) for i in ids]}}))
    await asyncio.gather(*[attack(doc) for doc in docs])

client = MongoClient(environ['MONGO_URI'] , 27017)
rss_feed = client.rss.rss_feed
rss_item = client.rss.rss_item


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
client.close()
