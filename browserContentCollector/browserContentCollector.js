const puppeteer = require('puppeteer');
const readline = require('readline');
const { stdin, env } = require('process');
const shuffle = require('shuffle-array')
const { MongoClient, ObjectID } = require("mongodb");

const dbName = "rss"
const collectionName = "rss_item";

(async() => {
    ids = []
    for await (const line of readline.createInterface({ input: stdin })) {
        ids.push(ObjectID(line))
    }

    try {
        const browser = await puppeteer.launch({ headless: true })
        const mongoClient = await new MongoClient(env.MONGO_URI, { useUnifiedTopology: true })
        await mongoClient.connect();
        const collection = await mongoClient.db(dbName).collection(collectionName)
        const docs = await collection.find({ '_id': { '$in': ids } }).project({ 'hash': 1, 'link': 1 }).toArray()

        const batchSize = 15
        let tasks = shuffle(docs).map(doc => async opts => {
            try {
                const page = await browser.newPage()
                await page.setRequestInterception(true)
                page.on('request', (req) => {
                    switch (req.resourceType) {
                        case 'stylesheet':
                        case 'image':
                            req.abort()
                            break;
                        default:
                            req.continue()
                            break;
                    }
                })

                await page.setDefaultNavigationTimeout(0)
                await page.goto(doc.link, { waitUntil: 'load' })
                const htmlContent = await page.content()

                const filter = { '_id': doc['_id'] }
                const addendum = { '$set': { 'browserContentCollector': { htmlContent } } }

                await collection.updateOne(filter, addendum)
                console.log(`${opts.n} ${doc.link} hit`)
                page.close()

            } catch (e) {
                console.log(`${opts.n} ${doc.link} missed because ${e}`)
            }
        })

        const queueTask = (opts) => {
            if (t = tasks.pop()) {
                return t(opts).then(() => queueTask(opts))
            }
        }
        await Promise.all(Array(batchSize).fill(queueTask).map((f, n) => f({ n })))
        await browser.close()
        await mongoClient.close()
    } catch (e) {
        console.log(e)
    }
})()