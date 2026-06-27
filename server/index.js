const express = require("express");
const app = express();
const port = 8080;

// Sammeln aller Raumdaten zu einer 1:n Gebäude-Raum Zuordnung
// aktuell fertige Zuordnung in ./rooms.json
// später hier aus Ordnerstruktur erstellen
const roomList = require("./rooms.json");

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

  let building = data.building;
  let room = data.room;

  let location = roomList[building].location;

  res.json({ building, location, room });

});

app.get("/rooms", (req, res) => {
  res.json(JSON.stringify(roomList));
});

app.listen(port, () => {

  console.log(port);

});

