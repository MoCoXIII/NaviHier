import { json, error } from "@sveltejs/kit";
import { readFileSync } from "fs";

import { facilities } from "$lib/server/facilities.js";
const facilityNameList = Object.keys(facilities);

export async function POST({ request }) {
  let { mapName, locationName, facilityName } = await request.json();

  if (facilityNameList.length === 1) {
    facilityName = facilityNameList[0];
  }
  if (!facilities[facilityName]) {
    error(
      404,
      `Facility ${facilityName} not found. This server hosts ${facilityNameList.length} facilities: ${facilityNameList}`,
    );
  }
  let facilityData = facilities[facilityName];

  if (!facilityData.locations[locationName]) {
    error(
      404,
      `Location ${locationName} not found in facility ${facilityName}.`,
    );
  }
  let locationData = facilityData.locations[locationName];

  if (!locationData.maps[mapName]) {
    error(404, `Map ${mapName} not found in location ${locationName}.`);
  }
  let mapData = locationData.maps[mapName];

  const mapPath = mapData.pathToHere + mapData.images.png;

  // sende base64 encoded PNG-Datei als String
  const base64Map = readFileSync(mapPath, "base64");
  return json({ b64: base64Map });
}
