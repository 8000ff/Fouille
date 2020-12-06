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
    for task in db.rss_task.find({'enable':True}):
        p = task['query']['filter']
        if interval := task.get('interval'):
            p['$or'] = [
                    {'lastCheck':None},
                    {'lastCheck':{'$lt': datetime.utcnow() - timedelta(**interval)}}
            ]
        docs = db[task['query']['collection']].find(p,{'_id':1})
        ids = list(map(get('_id'),docs))
        shuffle(ids)
        if len(ids) > 0:
            yield defaultdict(None,{**task, 'ids': ids[:task.get('batchsize')]})
    

def executeJob(job):
    return run(job['command'], stdout=PIPE,input='\n'.join(map(str,job['ids'])), encoding='utf8')

def optimizeBatches(jobs):
    pred = lambda job : job.get('batchsize') and job['batchsize'] < len(job['ids'])
    merge = lambda i,j : {**i, 'ids': list( set(i['ids']) | set(j['ids']) ) }
    balance = lambda merged : [{**merged,'ids':xs} for xs in chunked(merged['ids'],merged['batchsize'])]

    optimised,optimiseable = list(filter(lambda x : not pred(x),jobs)),list(filter(pred,jobs))
    
    grouped = [ list(v) for k,v in groupby( optimiseable , get('_id') )]
    merged = [ reduce(merge,job) for job in grouped ]
    balanced = map(balance,merged)

    return [*optimised,*flatten(balanced)]

# plan a lot
print('planning initial jobs')
jobs = [next(planJobs())]
while True:
    # do a little
    try:
        job = jobs.pop()
        print('working', job['description'],len(job['ids']))
        executeJob(job)
    except IndexError:
        print('no more jobs in queue')
        pass

    # check what's new
    print('planning jobs',end=' ')
    jobs = [next(planJobs())]

    # print(len(jobs),end=' -> ')
    # jobs = optimizeBatches(jobs)
    # print(len(jobs))
    if len(jobs) == 0 :
        print('nothing to do')
        sleep(10)
    
client.close()