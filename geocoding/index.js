const express = require('express');
const { normalize } = require('@geolonia/normalize-japanese-addresses')
const bodyParser = require('body-parser')

const app = express();
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.post('/api/v1/address', (req, res) => {
    const request_body = req.body;
    const raw_address = request_body.address;
    normalize(raw_address).then(result => {
        res.send(result)
      })    
});

// ポート5050でサーバを立てる
app.listen(5050, () => console.log('Listening on port 5050'));
