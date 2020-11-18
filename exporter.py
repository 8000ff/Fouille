#!/usr/bin/python3

import fileinput

from pymongo import MongoClient
from bson.objectid import ObjectId

import requests
import json

from functools import reduce

from os import environ


def deepGet(dic, keys, default = None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dic)

def deepSet(dic, keys, value):
    keys = keys.split(".")
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

def hasField(id, field):
    return rss_item.count_documents({"_id": ObjectId(id), field: {"$exists": "true"}}) == 1

def getField(id, field):
    return deepGet(rss_item.find_one({"_id": ObjectId(id)}, {'_id': 1, field: 1}), field)

def isAlreadyExported(id):
    query = {
        "query": {
            "term": {
                "mongo_id": {
                    "value": id
                }
            }
        }
    }
    res = requests.get(environ['ELASTIC_URI']+"/rss/rss_item/_search/", data=json.dumps(query)).json()
    if res["hits"]["total"] == 1:
        return res["hits"]["hits"][0]["_id"]
    else:
        return None

def export(id, fields):
    data = { "mongo_id": id }
    for field in fields:
        if hasField(id, field):
            deepSet(data, field, getField(id, field))
    elastic_id = isAlreadyExported(id)
    if(elastic_id):
        data = { "doc": data }
        requests.post(url = environ['ELASTIC_URI']+"/rss/rss_item/" + str(elastic_id) + "/_update/", data = json.dumps(data))
    else:
        requests.post(url = environ['ELASTIC_URI']+"/rss/rss_item/", data = json.dumps(data))
    
client = MongoClient(environ['MONGO_URI'] , 27017)
rss_item = client.rss.rss_item

ids = [line.rstrip('\n') for line in fileinput.input()]

fields = ["title", "contentCleaner.cleanContent"]

for id in ids:
    export(id, fields)