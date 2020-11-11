#!/usr/bin/python3

from pymongo import MongoClient
from bson.objectid import ObjectId
from os import environ 

from subprocess import run, PIPE
from collections import defaultdict
from operator import itemgetter as get
from more_itertools import map_reduce
from itertools import groupby

from time import sleep

client = MongoClient(environ['MONGO_URI'] , 27017)
db = client.rss

def planJobs():
    for task in db.rss_task.find({'enable':True}):
        docs = db[task['query']['collection']].find(task['query']['filter'],{'_id':1})
        ids = list(map(get('_id'),docs))
        if len(ids) > 0:
            yield defaultdict(None,{**task, 'ids': ids})

def executeJob(job):
    print('working')
    return run(job['command'], stdout=PIPE,input='\n'.join(map(str,job['ids'])), encoding='ascii')

# plan a lot
jobs = list(planJobs())
while True:
    # do a little
    try:
        job = jobs.pop()
        executeJob(job)
        print('job done')
    except IndexError:
        print('not more jobs')
        pass

    # check what's new
    jobs.extend(planJobs())

    if len(jobs) == 0 :
        print('nothing to do, sleeping')
        sleep(10)

    print('mandatory sleep')
    sleep(1)

client.close()