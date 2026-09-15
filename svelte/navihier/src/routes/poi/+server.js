import { json } from "@sveltejs/kit";

import { facilities } from "$lib/server/facilities.js";

export async function GET() {
  const allPOI = {};
  for (let [facilityName, facilityData] of Object.entries(facilities)) {
    allPOI[facilityName] = facilityData.poi;
  }
  return json(JSON.stringify(allPOI));
}
