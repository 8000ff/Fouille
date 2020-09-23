const puppeteer = require('puppeteer');
const readline = require('readline');
const { stdin } = require('process');
const devices = puppeteer.devices;

const { MongoClient,ObjectID } = require("mongodb");


const uri = "mongodb://localhost/rss";
const collectionName = "rss_item";

//TODO: Make device emulation configurable :
// await page.emulate(devices['iPhone X'])


//TODO: make image screenshot configurable
// if (false) {
//     const screenshots = Promise.all(
//         pages.map(async page => {
//             //TODO: refine image storage
//             const path = page.url().replace(/\.|\/|\:/g, '') + ".png"
//             console.log(path)
//             await page.screenshot({ path })
//         })
//     )
//     await screenshots
// }

(async () => {
    hashes = []
    for await (const line of readline.createInterface({ input: stdin })) {
        hashes.push(line)
    }
//    hashes = [hashes[0]]
    console.log(hashes.length)



    try {
        const browser = await puppeteer.launch()
        const getUrlsSession = new MongoClient(uri)

        console.log("Try")

        await getUrlsSession.connect();
        collection = await getUrlsSession.db().collection(collectionName)
        docs = await collection
            .find({ 'hash': { '$in': hashes } })
            .project({ 'hash':1,'link': 1 })
            .toArray()
        console.log(docs[0].hash)


        // for await (const doc of docs) {
        //     const page = await browser.newPage()
        //     console.log(doc.link)
        //     await page.goto(doc.link, { waitUntil: 'load' })
        //     htmlContent = await page.content()
        //     console.log(htmlContent)
        // }

        await Promise.all(
            docs.map(async doc => {
                const page = await browser.newPage()
                console.log(doc.link)
                await page.goto(doc.link, { waitUntil: 'load' })
                htmlContent = await page.content()
                await collection.updateOne({hash:doc.hash},{'$set' : {htmlContent}})
                //                return Object.assign(doc, { htmlContent })
                return;
        }))

        await browser.close()
        await getUrlsSession.close()

    } catch (e) {
        console.log("Catch")
        console.log(e)
    } finally {
        console.log("Finally")
    }
})()

