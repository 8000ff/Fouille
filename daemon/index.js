const { env } = require('process')
const { spawn } = require('child_process');

const { MongoClient, ObjectID } = require("mongodb");


(async() => {
    const uri = env.MONGO_URI
    const dbName = "rss"
    console.log(uri)
    const mongoClient = await new MongoClient(uri, { useUnifiedTopology: true })
    await mongoClient.connect()
    const config = await (await mongoClient.db(dbName).collection("config")).findOne({ name: "daemon" })
    jobs = []
    async function planJobs() {
        function removeRedundancy(array) {
            const joinByKey = (acc, x) => acc.set(x[0], [ ... (acc.get(x[0]) || []) , ... x[1] ])
            return [...array.reduce(joinByKey,new Map())].map(t => [t[0],[...new Set(t[1])]]);
        }

        const rss_task = await mongoClient.db(dbName).collection("rss_task")
        const tasks = await rss_task.find({ enable: true }).toArray()

        return tasks.map(async task => {
            const collection = await mongoClient.db(dbName).collection(task['collection'])
            const filter = JSON.parse(task['filter'])
            const items = await collection.find(filter).toArray()
            jobs.push([task.command, items.map(x => x['_id'].toString())])
            jobs = removeRedundancy(jobs)
        })
    }
    async function processJob(job){
        
    }
    const queueJob = (opts) => {
        if (t = jobs.pop()) {
            return t(opts).pl.then(() => queueJob(opts))
        }
    }

    await planJobs()
    await Promise.all(Array(batchSize).fill(queueJob).map((f, n) => f({ n })))
        
    await mongoClient.close()
})()