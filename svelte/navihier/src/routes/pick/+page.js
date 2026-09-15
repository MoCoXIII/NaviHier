export async function load({ fetch }) {
  const response = await fetch("/poi");
  const allPOI = await response.json();
  return { allPOI };
}
