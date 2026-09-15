import { readFileSync } from "fs";

export const facilities = setupFacilities();


// Auslesen aller Details aller Einrichtungen (facilities)
// dabei Zusammenstellen einer Standort-Räume-Beziehung für jede Einrichtung
function setupFacilities() {
  // Liste aller lokal gespeicherten Einrichtungen
  const pathToFacilities = "../../facilities/";
  // Geladene Dateien als Read-Only markieren (mit const als Verpflichtung und ro_ als Erinnerung)
  const ro_facilities = JSON.parse(
    readFileSync(pathToFacilities + "facilities.json", "utf-8"),
  );
  let facilities = {};

  for (const facility in ro_facilities) {
    let facilityPath = ro_facilities[facility];

    // Liste aller Standorte dieser Einrichtung ("Adresse": "Pfad zur Kartenliste dieses Standorts")
    const ro_locations = JSON.parse(
      readFileSync(pathToFacilities + facilityPath.join(""), "utf-8"),
    );
    const pathToFacility = pathToFacilities + facilityPath[0];

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
      const ro_maps = JSON.parse(
        readFileSync(pathToFacility + ro_locationdata.maps.join(""), "utf-8"),
      );
      const pathToLocation = pathToFacility + ro_locationdata.maps[0];

      locationdata.maps = ro_maps; // speichere die Liste der Karten des Standorts

      for (const map in ro_maps) {
        const path = ro_maps[map];

        // alle Inhalte der Karte
        const ro_mapdata = JSON.parse(
          readFileSync(pathToLocation + path.join(""), "utf-8"),
        );
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

  class Waypoint {
    constructor(id, x, y, poi, connections, map, isExit) {
      this.id = id;
      this.x = x;
      this.y = y;
      this.poi = poi;
      this.connections = connections;
      this.map = map;
      this.isExit = isExit;
      this.pathToHere = [];
      this.distanceToHere = undefined;
    }
  }
  for (let [facilityName, facilityData] of Object.entries(facilities)) {
    for (let [locationName, locationData] of Object.entries(
      facilityData.locations,
    )) {
      locationData.waypoints = {};
      for (let [mapName, mapData] of Object.entries(locationData.maps)) {
        for (let [waypointID, waypointData] of Object.entries(
          mapData.waypoints,
        )) {
          const waypoint = new Waypoint(
            waypointID,
            waypointData.x,
            waypointData.y,
            waypointData.poi,
            mapData.connections.filter(
              (connection) =>
                connection.start === waypointID ||
                connection.end === waypointID,
            ),
            mapName,
            waypointData.isExit,
          );
          locationData.waypoints[waypointID] = waypoint;
        }
      }

      // nun, da alle Wegpunkte dieses Standorts gesammelt sind, ist es sinnvoll zu prüfen,
      // ob wirklich alle ihre Verbindungen auch auf existierende Wegpunkte zeigen.
      // Eine fehlerhafte Verbindung kann das Pathfinding (aktuell, TODO: zu beheben) abstürzen lassen,
      // indem es den angezielten Wegpunkt nicht findet und doch versucht auf ihn zuzugreifen.
      // Diese Überprüfung dient zudem als Hinweis, falls in der Erstellung Fehler aufgetreten sind.
      for (let [waypointID, waypoint] of Object.entries(
        locationData.waypoints,
      )) {
        for (let connection of waypoint.connections) {
          let otherWaypoint = null;
          let supposedName = null;
          if (locationData.waypoints[connection.start].id === waypointID) {
            otherWaypoint = locationData.waypoints[connection.end];
            supposedName = connection.end;
          } else {
            otherWaypoint = locationData.waypoints[connection.start];
            supposedName = connection.start;
          }
          if (!otherWaypoint) {
            console.warn(`WARNUNG: Wegpunkt '${supposedName}' existiert nicht im Standort '${locationName}' von Einrichtung '${facilityName}'.
Er wird jedoch in folgender Verbindung erwähnt:
            "start": "${connection.start}",
            "end": "${connection.end}"
`);
          }
        }
      }
    }
  }

  return facilities;
}
