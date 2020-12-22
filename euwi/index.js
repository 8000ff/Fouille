const express = require("express");
const app = express();

const pug = require("pug");

const { stdin, env } = require('process');

const { Client } = require('@elastic/elasticsearch')
const client = new Client({

  node: env.ELASTIC_URI
  
})

app
    .set("views", "euwi/views")

    .set("view engine", "pug")

    .use(express.static("euwi/public"))

    .get("/", (_, res) => {

        res.status(200);
        res.render("index");
        res.end();

    })

    .get("/search/:query", (req, res) => {

        let query = req.params.query;

        client.search({

            index: "rss",
            body: {
                
                query: {
                    
                    "query_string": {

                        "query": query

                    }
                
                },
                "filter": {

                    "bool": {

                        "must_not": { "missing": { "field": "cleanDate" } }

                    }

                },
                
                "sort": { "cleanDate" : "desc" }
            
            }
        
        }, (err, result) => {

            if(err) { 

                console.log(err)

                res.status(500);
                res.send("Error server");
                res.end();

            } else {

                console.log(result.body.hits.hits)

                result = result.body.hits.hits.map(e => e._source)

                res.status(200);
                res.render("result", { query: query, results: result });
                res.end();

            }
        
        })  

        

    })

    .use(function(_, res){

        res.setHeader("Content-Type", "text/plain");
        res.status(404);
        res.send("Page introuvable");
        res.end();

    })

    .listen(8080, () => {

        console.log(`Server started at port 8080`);

    });