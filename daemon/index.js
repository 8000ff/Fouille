const { env } = require('process')
const { spawn } = require('child_process');

const { MongoClient, ObjectID } = require("mongodb");

function merge(a, b) {
    m = newx M
    const hist = (acc, x) => acc.set(x, acc.get(x) ? acc.get(x) + 1 : 1) /*needs a new Map([]) to work as intended*/


}

(async() => {
    const uri = env.MONGO_URI
    const dbName = "rss"

    const mongoClient = await new MongoClient(uri, { useUnifiedTopology: true })
    await mongoClient.connect()
    const config = await (await mongoClient.db(dbName).collection("config")).findOne({ name: "daemon" })
    jobs = []
    async function planJobs() {
        const rss_task = await mongoClient.db(dbName).collection("rss_task")
        const tasks = await rss_task.find({ enable: true }).toArray()

        return tasks.map(async task => {
            const collection = await mongoClient.db(dbName).collection(task['collection'])
            const filter = JSON.parse(task['filter'])
            const items = await collection.find(filter).toArray()
            jobs.push([task.command, items.map(x => x['_id'])])
            jobs = jobs.hist() // Merge same jobs

        })
    }


    //const rss_item = await mongoClient.db(dbName).collection("rss_item")

    // console.log(tasks)

    await Promise.all(await planJobs())
    console.log(jobs)
        // const simJob = 5
        // const idleTime = 3000

    // const queueJob = (job) => {
    //     if (t = tasks.pop()) {
    //         return t().then(queueJob)
    //     } else {
    //         return new Promise((resolve, reject) => setTimeout(resolve, idleTime)).then(queueJob)
    //     }
    // }
    await mongoClient.close()
})()