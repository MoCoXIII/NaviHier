// WICHTIG:
// Damit relative Pfade richtig erkannt werden, bitte aus dem Projektordner ausführen:
// NaviHier$ node ./server/index.js

const express = require("express");
const app = express();
const port = 8080;

// Serving der Client-Seite über den Server
// wird direkt unter "/" geladen, also später nicht versuchen, noch etwas auf app.get("/", ...) anzubieten
app.use(express.static('client'));


// Auslesen aller Details aller Einrichtungen (facilities)
// dabei Zusammenstellen einer Standort-Räume-Beziehung für jede Einrichtung

// Liste aller lokal gespeicherten Einrichtungen
const pathToFacilities = "../facilities/";
// Geladene Dateien als Read-Only markieren (mit const als Verpflichtung und ro_ als Erinnerung)
const ro_facilities = require(pathToFacilities + "facilities.json");
let facilities = {};

for (const facility in ro_facilities) {
  let facilityPath = ro_facilities[facility];

  // Liste aller Standorte dieser Einrichtung ("Adresse": "Pfad zur Kartenliste dieses Standorts")
  const ro_locations = require(pathToFacilities + facilityPath.join(""));
  const pathToFacility = "../facilities/" + facilityPath[0];

  let facilityContent = {};
  facilities[facility] = facilityContent; // speichere die Liste der Standorte dieser Einrichtung
  let facility_poi = {};
  facilityContent["poi"] = facility_poi; // initialisiere Points Of Interest Zusammenfassung für diese Einrichtung

  facilityContent.locations = {};

  for (const locationShortName in ro_locations) {
    const ro_locationdata = ro_locations[locationShortName];
    let locationdata = ro_locationdata;
    facilityContent.locations[locationShortName] = locationdata;

    let location_poi = { poi: {} };
    location_poi.location = ro_locationdata.location;
    facility_poi[locationShortName] = location_poi; // erweitere Points Of Interest Zusammenfassung um diesen Standort

    // Liste aller Karten des Standorts
    const ro_maps = require(pathToFacility + ro_locationdata.maps.join(""));
    const pathToLocation = pathToFacility + ro_locationdata.maps[0];

    locationdata.maps = ro_maps; // speichere die Liste der Karten des Standorts

    for (const map in ro_maps) {
      const path = ro_maps[map];

      // alle Inhalte der Karte
      const ro_mapdata = require(pathToLocation + path.join(""));
      let mapdata = ro_mapdata;
      const pathToMap = pathToLocation + path[0];
      mapdata["pathToHere"] = pathToMap;

      locationdata.maps[map] = mapdata; // speichere Kartendaten

      // um eine schnell absendbare Zusammenfassung der Points Of Interest zu erhalten,
      // werden Points Of Interest ihren Gebäuden zugeordnet in einer Übersicht versammelt
      const waypoints = ro_mapdata.waypoints;
      for (let waypointID in waypoints) {
        const waypoint = waypoints[waypointID];
        const poiName = waypoint["poi"];
        if (poiName) {
          const altNames = ro_mapdata.poi[poiName].names;
          location_poi.poi[poiName] = altNames || poiName;
        }
      }
    }
  }
}
const facilityNameList = Object.keys(facilities);

class Waypoint {
  constructor(id, poi, connections, map) {
    this.id = id;
    this.poi = poi;
    this.connections = connections;
    this.map = map;
    this.pathToHere = [];
    this.distanceToHere = undefined;
    this.isExit = false;
  }
}
for (let [facilityName, facilityData] of Object.entries(facilities)) {
  for (let [locationName, locationData] of Object.entries(facilityData.locations)) {
    locationData.waypoints = {};
    for (let [mapName, mapData] of Object.entries(locationData.maps)) {
      for (let [waypointID, waypointData] of Object.entries(mapData.waypoints)) {
        const waypoint = new Waypoint(
          waypointID,
          waypointData.poi,
          mapData.connections.filter(connection => connection.start === waypointID || connection.end === waypointID),
          mapName
        );
        locationData.waypoints[waypointID] = waypoint;
      }
    }
  }
}


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

  let location = poi[building].location;

  res.json({ building, location, room });

});

app.get("/poi/{:facility{/:verification}}", (req, res) => {
  const facility = req.params.facility;

  // parameter "verification" dient momentan als Notiz:
  // falls in Zukunft der Zugriff auf die Daten einer Einrichtung verifiziert werden soll,
  // könnte ein solcher Parameter genutzt werden (derzeit ungenutzt)
  const verification = req.params.verification;

  if (facilityNameList.length === 1) {
    res.json(JSON.stringify(facilities[facilityNameList[0]].poi));
  } else if (facility) {
    if (facilities[facility]) {
      res.json(JSON.stringify(facilities[facility].poi));
    } else {
      res.status(404).send(`Facility ${facility} not found. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`);
    }
  } else {
    res.status(400).send(`Expected facility identifier. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`);
  }
});

app.get("/path/:start/:destination/{:facility}", (req, res) => {
  const URIstart = decodeURIComponent(req.params.start);
  const URIdestination = decodeURIComponent(req.params.destination);
  let facilityName = decodeURIComponent(req.params.facility);

  if (facilityNameList.length === 1) {
    facilityName = facilityNameList[0];
  };
  if (!facilityName) {
    res.status(400).send(`Expected facility identifier. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`);
  } else if (!facilities[facilityName]) {
    res.status(404).send(`Facility ${facilityName} not found. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`);
  };

  if (!URIstart || !URIdestination) {
    res.status(400).send("Expected start and destination");
  };

  const [startLocation, startPOI] = URIstart.split(", ");
  const [destLocation, destPOI] = URIdestination.split(", ");

  let finalPath = [];

  // findPathInLocation findet den kürzesten Weg zwischen zwei POI
  // Eingaben:
  // - start: Information über den Punkt, von dem aus begonnen wird
  // - destination: Information über einen Punkt, zu dem der Weg gefunden werden soll
  // - location (Object): der Standort, der alle nötigen Wegpunkte, ihre Verbindungen und Attribute enthält
  function findPathInLocation(start, destination, location, requirements={}) {

    // zuerst sicherstellen, dass alle Wegpunkte in ihren Attributen zur Wegfindung unspezialisiert sind
    for (const waypoint of Object.values(location.waypoints)) {
      // diese beiden Werte sind vom Startpunkt abhängig, müssen also zurückgesetzt werden
      waypoint.pathToHere = [];
      waypoint.distanceToHere = undefined;
    }

    // wenn start { type: "exit" } ist, den nächstgelegenen Ausgang vom Ziel aus finden
    // also Start und Ziel tauschen, dann die erhaltene Liste umkehren
    let reversed = false;
    if (start.type === "exit") {
      reversed = true;
      [start, destination] = [destination, start];
    }
    
    // darauf achten, dass Start und Ziel folgendermaßen aussehen:
    // start oder ziel = { type: "POI", name: "..." } oder { type: "exit" }

    // ersten Wegpunkt finden, der zum start-POI gehört
    start = Object.values(location.waypoints).find(waypoint => waypoint.poi === start.name);
    // für destination ist dies nicht nötig, da die Wegfindung auf den frühstmöglich passenden Punkt optimieren kann

    let waypointsToCheck = [start];

    while (waypointsToCheck.length > 0) {
      // wählt den nächsten Wegpunkt, indem .shift() das erste Element der Liste wiedergibt und entfernt
      // for loop ist nicht möglich, da die Liste während des loops bearbeitet wird
      const currentWaypoint = waypointsToCheck.shift();

      if (currentWaypoint.poi === destination.name || (currentWaypoint.isExit && destination.type === "exit")) {
        let finalPath = [...currentWaypoint.pathToHere, currentWaypoint];
        if (reversed) finalPath.reverse();
        
        // finalPath ist nun eine Liste von Wegpunkt-Objekten, mit denen der Client nichts anfangen kann
        // daher muss er in eine Liste von maps zu Waypoint-IDs umgeformt werden
        let finalMapPath = [];
        let currentMap = undefined;
        let subMapPath = {};
        for (const waypoint of finalPath) {
          if (currentMap === undefined) {
            currentMap = waypoint.map;
            subMapPath[currentMap] = [];
          }
          if (waypoint.map !== currentMap) {
            finalMapPath.push(subMapPath);
            subMapPath = {};
            currentMap = waypoint.map;
            subMapPath[currentMap] = [];
          }
          subMapPath[currentMap].push(waypoint.id);
        }
        finalMapPath.push(subMapPath);
        
        return finalMapPath;
      }

      for (const connection of currentWaypoint.connections) {
        let nextWaypoint = null;
        if (connection.start === currentWaypoint.id) {
          nextWaypoint = location.waypoints[connection.end];
        } else {  // connection.end === currentWaypoint.id
          nextWaypoint = location.waypoints[connection.start];
        }

        let mayPass = true;
        // hier auf Barrierefreiheit und Zugangsberechtigung prüfen
        if (requirements.accessible && connection.inaccessible) {
          mayPass = false;
        } 

        if (mayPass) {
          const newDistance = currentWaypoint.distanceToHere + (connection.length || 0);
          if (nextWaypoint.distanceToHere === undefined || nextWaypoint.distanceToHere > newDistance) {
            nextWaypoint.distanceToHere = newDistance;
            nextWaypoint.pathToHere = [...currentWaypoint.pathToHere, currentWaypoint];
          } else {
            continue;  // der Wegpunkt ist bereits mit einer kürzeren Strecke erreicht worden, über diesen Weg also nicht weiter zu verfolgen
          }

          waypointsToCheck.push(nextWaypoint);
        }
      }
    }

    return;
  }

  if (startLocation !== destLocation) {
    // setze Ziel auf nächstgelegenen Standort-Ausgang
    let start = { type: "POI", name: startPOI };
    let destination = { type: "exit" };

    // Route aus Standort 1 heraus
    finalPath.push(findPathInLocation(start, destination, facilities[facilityName].locations[startLocation]));

    // Verweis auf Navigation zu Standort 2
    finalPath.push(facilities[facilityName].locations[destLocation].location);

    // Route von Ausgang Standort 2 zum Ziel
    start = { type: "exit" };
    destination = { type: "POI", name: destPOI };
    finalPath.push(findPathInLocation(start, destination, facilities[facilityName].locations[destLocation]));
  } else {
    let start = { type: "POI", name: startPOI };
    let destination = { type: "POI", name: destPOI };

    finalPath.push(findPathInLocation(start, destination, facilities[facilityName].locations[startLocation]));
  }

  res.json(finalPath);
});

app.listen(port, () => {

  console.log(port);

});

