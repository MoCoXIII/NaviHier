import { json } from "@sveltejs/kit";
import { readFileSync } from "fs";

import { facilities } from "$lib/server/facilities.js";
const facilityNameList = Object.keys(facilities);

export async function POST({ request }) {
  const { mapName, locationName, facilityName } = request.json();

  if (facilityNameList.length === 1) {
    facilityName = facilityNameList[0];
  }
  if (!facilities[facilityName]) {
    error(
      404,
      `Facility ${facilityName} not found. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`,
    );
  }
  facilityData = facilities[facilityName];

  if (!facilityData.locations[locationName]) {
    error(
      404,
      `Location ${locationName} not found in facility ${facilityName}.`,
    );
  }
  locationData = facilityData.locations[locationName];

  if (!locationData.maps[mapName]) {
    error(404, `Map ${mapName} not found in location ${locationName}.`);
  }
  mapData = locationData.maps[mapName];

  const mapPath = mapData.pathToHere + mapData.images.png;

  // sende base64 encoded PNG-Datei als String
  const base64Map = readFileSync(mapPath, "base64");
  return json({ map: base64Map });
}
