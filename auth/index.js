const express = require('express')
const app = express()
const port = 3050

app.use(express.json())

app.get('/validate-request', (req, res) => {
    res.status(200).json({"x-hasura-role": "admin", "x-hasura-user-id": "1"});
})

app.post('/validate-request', (req, res) => {
    console.log("INCOMING REQUEST");
    let response = {};
    const headers = Object.fromEntries(Array.from(req.body["headers"]));
     for (const key in req.body["headers"]) {
         response[key] = String(req.body["headers"][key]);
    }
    if (response["x-hasura-role"] === undefined){
        // Validate all requests as admin for dev
        response["x-hasura-role"] = "admin";
    }
    console.log(response);
    res.status(200).json(response);
})

app.listen(port, () => {
    console.log(`Dev webhook authentication listening at http://localhost:${port}`)
}
)