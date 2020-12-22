#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

from os import environ 

def attack(id):
    doc = rss_item.find_one({"_id": ObjectId(id)})
    cleanContent = doc["contentCleaner"]["cleanContent"]
    words = cleanContent.split(' ')
    middle = lambda s,t : " ".join(words[ int(s * len(words)) : int( t * len(words)) ])
    rss_item.update_one({"_id": ObjectId(id)}, {"$set": { "middle": {"10":middle(.45,.55),"25":middle(.375,.625),"50":middle(.25,.75)}}})

client = MongoClient(environ['MONGO_URI'])
rss_item = client.rss.rss_item

ids = [line.rstrip('\n') for line in fileinput.input()]

for id in ids:
    attack(id)