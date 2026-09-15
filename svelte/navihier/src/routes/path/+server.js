import { json } from "@sveltejs/kit";

import { facilities } from "$lib/server/facilities.js";
const facilityNameList = Object.keys(facilities);

export async function POST({ request }) {
  const { start, destination, facility } = request.json();

  console.log(
    `Angeforderter Link: ?s=${encodeURIComponent(
      decodeURIComponent(start),
    )}&d=${encodeURIComponent(
      decodeURIComponent(destination),
    )} in Einrichtung ${facility}`,
  );
  const URIstart = decodeURIComponent(start);
  const URIdestination = decodeURIComponent(destination);
  let facilityName = decodeURIComponent(facility);

  if (facilityNameList.length === 1) {
    facilityName = facilityNameList[0];
  }
  if (!facilityName) {
    error(
      400,
      `Expected facility identifier. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`,
    );
  } else if (!facilities[facilityName]) {
    error(
      404,
      `Facility ${facilityName} not found. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`,
    );
  }

  if (!URIstart || !URIdestination) {
    error(400, "Expected start and destination");
  }

  const [startLocation, startPOI] = URIstart.split(", ");
  const [destLocation, destPOI] = URIdestination.split(", ");

  let finalPath = [];

  // findPathInLocation findet den kürzesten Weg zwischen zwei POI
  // Eingaben:
  // - start: Information über den Punkt, von dem aus begonnen wird
  // - destination: Information über einen Punkt, zu dem der Weg gefunden werden soll
  // - location (Object): der Standort, der alle nötigen Wegpunkte, ihre Verbindungen und Attribute enthält
  function findPathInLocation(
    start,
    destination,
    location,
    locationName,
    requirements = {},
  ) {
    // location.waypoints ist global definiert
    // daher ändern sich die Attribute der Wegpunkte im globalen Register, wenn diese Wegfindung sie bearbeitet (Attribute pathToHere & distanceToHere)
    // es muss also eine lokale Kopie dieses Objekts erstellt werden
    let allWaypoints = {};
    for (const [waypointID, waypoint] of Object.entries(location.waypoints)) {
      allWaypoints[waypointID] = new Waypoint(
        waypoint.id,
        waypoint.x,
        waypoint.y,
        waypoint.poi,
        waypoint.connections,
        waypoint.map,
        waypoint.isExit,
      ); // klone jeden Wegpunkt
    }

    // zuerst sicherstellen, dass alle Wegpunkte in ihren Attributen zur Wegfindung unspezialisiert sind
    for (const waypoint of Object.values(allWaypoints)) {
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
    // für destination ist dies nicht nötig, da die Wegfindung auf den frühstmöglich passenden Punkt optimieren kann
    let starts = Object.values(allWaypoints).filter(
      (waypoint) => waypoint.poi === start.name,
    );
    starts.forEach((waypoint) => (waypoint.distanceToHere = 0));

    let waypointsToCheck = [...starts];

    while (waypointsToCheck.length > 0) {
      // wählt den nächsten Wegpunkt, indem .shift() das erste Element der Liste wiedergibt und entfernt
      // for loop ist nicht möglich, da die Liste während des loops bearbeitet wird
      const currentWaypoint = waypointsToCheck.shift();

      if (
        (destination.name && currentWaypoint.poi === destination.name) ||
        (currentWaypoint.isExit && destination.type === "exit")
      ) {
        let finalPath = [...currentWaypoint.pathToHere, currentWaypoint];
        if (reversed) finalPath.reverse();

        // finalPath ist nun eine Liste von Wegpunkt-Objekten, mit denen der Client nichts anfangen kann
        // daher muss er in eine Liste von maps zu Waypoint-IDs umgeformt werden
        let finalMapPath = {};
        finalMapPath[locationName] = [];
        let currentMap = undefined;
        let subMapPath = {};
        for (const waypoint of finalPath) {
          if (currentMap === undefined) {
            currentMap = waypoint.map;
            subMapPath[currentMap] = [];
          }
          if (waypoint.map !== currentMap) {
            finalMapPath[locationName].push(subMapPath);
            subMapPath = {};
            currentMap = waypoint.map;
            subMapPath[currentMap] = [];
          }
          const waypointInfo = {
            id: waypoint.id,
            x: waypoint.x,
            y: waypoint.y,
            poi: waypoint.poi,
            isExit: waypoint.isExit,
          };
          subMapPath[currentMap].push(waypointInfo);
        }
        finalMapPath[locationName].push(subMapPath);

        return finalMapPath;
      }

      for (const connection of currentWaypoint.connections) {
        let nextWaypoint = null;
        if (connection.start === currentWaypoint.id) {
          nextWaypoint = allWaypoints[connection.end];
        } else {
          // connection.end === currentWaypoint.id
          nextWaypoint = allWaypoints[connection.start];
        }

        let mayPass = true;
        // hier auf Barrierefreiheit und Zugangsberechtigung prüfen
        if (requirements.accessible && connection.inaccessible) {
          mayPass = false;
        }

        if (mayPass) {
          const newDistance =
            currentWaypoint.distanceToHere + (connection.length || 0);
          // Längenvergleich und Vorgehen auf Basis der Länge nach Dijkstra: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
          if (
            nextWaypoint.distanceToHere === undefined ||
            nextWaypoint.distanceToHere > newDistance
          ) {
            nextWaypoint.distanceToHere = newDistance;
            nextWaypoint.pathToHere = [
              ...currentWaypoint.pathToHere,
              currentWaypoint,
            ];
          } else {
            continue; // der Wegpunkt ist bereits mit einer kürzeren Strecke erreicht worden, über diesen Weg also nicht weiter zu verfolgen
          }

          waypointsToCheck.push(nextWaypoint);
        }
      }

      waypointsToCheck.sort((a, b) => a.distanceToHere - b.distanceToHere);
    }

    return;
  }

  if (startLocation !== destLocation) {
    // setze Ziel auf nächstgelegenen Standort-Ausgang
    let start = { type: "POI", name: startPOI };
    let destination = { type: "exit" };

    // Route aus Standort 1 heraus
    finalPath.push(
      findPathInLocation(
        start,
        destination,
        facilities[facilityName].locations[startLocation],
        startLocation,
      ),
    );

    // Verweis auf Navigation zu Standort 2
    finalPath.push(facilities[facilityName].locations[destLocation].location);

    // Route von Ausgang Standort 2 zum Ziel
    start = { type: "exit" };
    destination = { type: "POI", name: destPOI };
    finalPath.push(
      findPathInLocation(
        start,
        destination,
        facilities[facilityName].locations[destLocation],
        destLocation,
      ),
    );
  } else {
    let start = { type: "POI", name: startPOI };
    let destination = { type: "POI", name: destPOI };

    finalPath.push(
      findPathInLocation(
        start,
        destination,
        facilities[facilityName].locations[startLocation],
        startLocation,
      ),
    );
  }

  return json(finalPath);
}
