const express = require("express");
const app = express();

const pug = require("pug");

const { Client } = require('@elastic/elasticsearch')
const client = new Client({

  node: "http://51.83.70.93:9200"
  
})

function searchNews(query) {

    let ret = [
        {

            title: "test1",
            description: "test1test1test1test1test1",
            link: "/test1"

        },
        {

            title: "test2",
            description: "test2test2test2test2test2",
            link: "/test2"

        },
        {

            title: "test3",
            description: "test3test3test3test3test3",
            link: "/test3"

        },
        {

            title: "test4",
            description: "test4test4test4test4test4",
            link: "/test4"

        }

    ];

    return ret;

}

app
    .set("views", "./views")

    .set("view engine", "pug")

    .use(express.static("public"))

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
                
                }
            
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