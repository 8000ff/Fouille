#!/usr/bin/python3

import feedparser
import urllib.request
import hashlib

import fileinput

import threading
from pymongo import MongoClient


def make_hash(*values):
    # TODO: make "hash" algorythme configurable
    return hashlib.sha1(''.join(values).encode()).hexdigest()


def make_kv(post):
    # TODO: make default field value configurable
    return lambda field: (field, post.get(field, ''))


def make_item(source, post):
    # TODO: make rss item fields configurable
    rss_item_kv = [
        *map(make_kv(post), ['published', 'title', 'description', 'link', 'language'])]
    extra_kv = [('hash', make_hash(
        source, *map(lambda t: t[1], rss_item_kv))), ('source', source)]
    return dict([*rss_item_kv, *extra_kv])


def attack(url):
    rss_items = [*map(lambda post: make_item(url, post),
                      feedparser.parse(url).entries)]
    # TODO: make db connection configurable
    # TODO: check that connection actually append
    collection = MongoClient('192.168.1.69', 27017).rss.rss_item
    map(lambda item: collection.update_one(
        {'hash': item['hash']}, {"$set": item}, upsert=True), rss_items)


# As HTTP(s) can take time or even never respond
# each input url has to treated asynchronously
# TODO: benchmark python.threading vs asyncio
for line in fileinput.input():
    threading.Thread(target=attack, args=(line,)).start()
