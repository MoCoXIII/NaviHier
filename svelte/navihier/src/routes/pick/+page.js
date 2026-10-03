import { base } from "$app/paths";

export async function load({ fetch }) {
  const response = await fetch(`${base}/poi`);
  const allPOI = await response.json();
  return { allPOI };
}
