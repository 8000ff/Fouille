#!/usr/bin/python3

from pymongo import MongoClient
from bson.objectid import ObjectId
from os import environ 

from subprocess import run, PIPE
from collections import defaultdict
from operator import itemgetter as get
from more_itertools import map_reduce,chunked,flatten
from itertools import groupby
from functools import reduce

from time import sleep
from datetime import datetime,timedelta

from random import shuffle

client = MongoClient(environ['MONGO_URI'])
db = client.rss



def planJobs():
    tasks = list(db.rss_task.find({'enable':True}))
    shuffle(tasks)
    for task in tasks:
        p = task['query']['filter']
        if interval := task.get('interval'):
            p['$or'] = [
                    {'lastCheck':None},
                    {'lastCheck':{'$lt': datetime.utcnow() - timedelta(**interval)}}
            ]
        defbatchsize = db[task['query']['collection']].estimated_document_count()
        docs = db[task['query']['collection']].find(p,{'_id':1}).limit(task.get('batchsize',defbatchsize))
        ids = list(map(get('_id'),docs))
        if len(ids) > 0:
            shuffle(ids)
            return defaultdict(None,{**task, 'ids': ids[:task.get('batchsize')]})
    

def executeJob(job):
    return run(job['command'], stdout=PIPE,input='\n'.join(map(str,job['ids'])), encoding='utf8')

# plan a lot
while True:
    print('planning')
    job = planJobs()
    # do a little
    if job:
        print('working', job['description'],len(job['ids']))
        executeJob(job)
        print('done')        
    else:
        print('nothing to do')
        sleep(5)
    
client.close()