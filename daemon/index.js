const { env } = require('process')

const { MongoClient, ObjectID } = require("mongodb")

const uri = env.MONGO_URI
const dbName = "rss"
const collectionName = "rss_task"

(async() => {
    const client = await new MongoClient(uri, { useUnifiedTopology: true })
    await client.connect()

    tasks = await client.db(dbName).collection(collectionName)



})