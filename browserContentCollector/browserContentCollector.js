const puppeteer = require('puppeteer');
const readline = require('readline');
const { stdin, env } = require('process');

const { MongoClient, ObjectID } = require("mongodb");

const uri = env.MONGO_URI;
const dbName = "rss"
const collectionName = "rss_item";

(async() => {
    ids = []
    for await (const line of readline.createInterface({ input: stdin })) {
        ids.push(ObjectID(line))
    }

    //TODO: make batch size configurable

    try {
        const browser = await puppeteer.launch({ headless: true })
        const getUrlsSession = await new MongoClient(uri, { useUnifiedTopology: true })
        await getUrlsSession.connect();
        collection = await getUrlsSession.db(dbName).collection(collectionName)

        docs = await collection
            .find({ '_id': { '$in': ids } })
            .project({ 'hash': 1, 'link': 1 })
            .toArray()

        await Promise.all(
            docs.map(async doc => {
                try {
                    const page = await browser.newPage()
                    await page.goto(doc.link, { waitUntil: 'load' })
                    htmlContent = await page.content()
                    await collection.updateOne({ '_id': doc['_id'] }, { '$set': { 'browserContentCollector': { htmlContent } } })
                    page.close()
                    console.log(`${doc.link} hit`)
                } catch (e) {
                    console.log(`${doc.link} missed because ${e}`)
                }
            })
        )

        await browser.close()
        await getUrlsSession.close()
    } catch (e) {
        console.log(e)
    }
})()