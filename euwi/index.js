const pug = require('pug');
const express = require('express');
const app = express()

const elstic_uri = 'http://localhost:9200'
const { Client } = require('@elastic/elasticsearch')
const elastic = new Client({ node: elstic_uri })


const { MongoClient } = require("mongodb");

const mongo_uri = "mongodb://localhost/rss"
const collectionName = "elastic_client";

async function register() {
    const mongo = new MongoClient(mongo_uri)
    try {
        await mongo.connect()
        collection = await mongo.db().collection(collectionName)
        registered = await collection.find({ elstic_uri }).count() > 0
        if (!registered) {
            await collection.insertOne({ elstic_uri })
        }
        mongo.close();
    } catch (e) {
        console.warn('Elastic instance did not manage to contact backend, backend is probably offline')
    }
}
register()

app.set('view engine', 'pug')

app.get('/', function(req, res) {
    console.log('req')
    const params = Object.keys(req.query)
    if (params.length == 0) {
        res.render('search')
    } else {
        elastic.search({
            index: 'my-index',
            body: {
                query: {
                    match: { hello: 'world' }
                }
            }
        }, (err, result) => {
            if (err) console.log(err)
            else res.render('result', result)
        })
    }
})

app.use(express.static(__dirname + "/public"));
app.listen(3000, (x) => console.log('listening', x))