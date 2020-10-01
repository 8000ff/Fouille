const pug = require('pug');
const express = require('express');
const app = express();

const readline = require('readline');
const { stdin, env } = require('process');

const { MongoClient, ObjectID } = require("mongodb");

const uri = env.MONGO_URI + "/rss";

app.set('view engine', 'pug')
app.use(express.static(__dirname + "/public"));

app.get('/', (req, res) => {
    res.render('base')
})

app.listen(3000, () => console.log('listening on 3000'))