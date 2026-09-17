export async function load({ url, fetch }) {
    const s = url.searchParams.get("s");
    const d = url.searchParams.get("d");
    const f = url.searchParams.get("f");

    const route = await fetch("/path", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ start: s, destination: d, facility: f }),
    });

    const path = await route.json();
    return { path };
}