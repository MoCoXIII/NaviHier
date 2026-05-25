const express = require("express");
const app = express();
const port = 8080;

// https://expressjs.com/en/5x/api.html#express.json
// die Middleware erstellt den req.body Eintrag aus empfangenen JSON-Daten
// (sonst ist req.body undefined)
app.use(express.json());
// app.use() führt Middleware für alle Anfragen aus;
// next() lässt danach das nächste Callback die Anfrage verarbeiten
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

app.post("/server", (req, res) => {

  let data = req.body;
  console.log(data);
  res.json(JSON.stringify(data));

});

app.get("/rooms", (req, res) => {
  let rooms = require("./rooms.json");
  res.json(JSON.stringify(rooms));
});

app.listen(port, () => {

  console.log(port);

});

