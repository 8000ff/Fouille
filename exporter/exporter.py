#!/usr/bin/python3

from bs4 import BeautifulSoup

import fileinput

import asyncio

from pymongo import MongoClient
from bson.objectid import ObjectId

def hasCleanContent(id):
    return rss_item.count_documents({"_id": ObjectId(id), "browserContentCollector.htmlContent": {"$exists": "true"}}) == 1

def getCleanContent(id):
    return rss_item.find_one({"_id": ObjectId(id)})["browserContentCollector"]["htmlContent"]

def export(id):
    html = getCleanContent(id)
    cleanContent = htmlToTxt(html)
    rss_item.update_one({"_id": ObjectId(id)}, {"$set": {"cleanContent": cleanContent}})

client = MongoClient('mongodb://rss_user:rssproject1@51.83.70.93:27017/?authSource=rss')
rss_item = client.rss.rss_item

ids = filter(lambda id: hasCleanContent(id), [line.rstrip('\n') for line in fileinput.input()]) 

for id in ids:
    export(id)