#!/usr/bin/python3

from bs4 import BeautifulSoup

import fileinput

import asyncio

from pymongo import MongoClient
from bson.objectid import ObjectId

def getHtml(id):
	return rss_item.find_one({"_id": ObjectId(id)}).html

def htmlToTxt(html):
	return BeautifulSoup(html, 'html.parser')

async def clean(id):
    html = getHtml(id)
    cleanContent = htmlToTxt(html)
    rss_item.update_one({"_id": ObjectId(id)}, { "$set": { "cleanContent": cleanContent } } )

async def main():
    ids = [line.rstrip('\n') for line in fileinput.input()]
    await asyncio.gather(*[clean(id) for id in ids])

client = MongoClient("176.166.49.201", 27017)
rss_item = client.rss.rss_item

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
client.close()