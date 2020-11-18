#!/usr/bin/python3

from bs4 import BeautifulSoup

import fileinput

import asyncio

from pymongo import MongoClient
from bson.objectid import ObjectId

from os import environ 


def getHtml(id):
    return rss_item.find_one({"_id": ObjectId(id)})["browserContentCollector"]["htmlContent"]

def htmlToTxt(html):
	return " ".join(BeautifulSoup(html, 'html.parser').get_text().split())

def clean(id):
    html = getHtml(id)
    cleanContent = htmlToTxt(html)
    rss_item.update_one({"_id": ObjectId(id)}, {"$set": { "contentCleaner": { "cleanContent": cleanContent}}})

client = MongoClient(environ['MONGO_URI'])
rss_item = client.rss.rss_item

ids = [line.rstrip('\n') for line in fileinput.input()]

for id in ids:
    clean(id)