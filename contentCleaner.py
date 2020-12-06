#!/usr/bin/python3

from html2text import HTML2Text 
import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from os import environ 

import re

h2t = HTML2Text()
h2t.ignore_links = True
h2t.ignore_tables = True
h2t.ignore_images = True
h2t.ignore_emphasis = True

def clean(id):
    html = rss_item.find_one({"_id": ObjectId(id)})["browserContentCollector"]["htmlContent"]
    cleanContent = h2t.handle(html).replace('*','').replace('\n',' ')
    cleanContent = re.sub(r"\W",' ',cleanContent)
    cleanContent = re.sub(r"\s+",' ',cleanContent)
    rss_item.update_one({"_id": ObjectId(id)}, {"$set": { "contentCleaner": { "cleanContent": cleanContent}}})

client = MongoClient(environ['MONGO_URI'])
rss_item = client.rss.rss_item

ids = [line.rstrip('\n') for line in fileinput.input()]

for id in ids:
    clean(id)