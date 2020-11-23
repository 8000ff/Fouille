const express = require("express");
const app = express();

const pug = require("pug");

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

        let results = searchNews(query);

        res.status(200);
        res.render("result", { query: query, results: results });
        res.end();

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