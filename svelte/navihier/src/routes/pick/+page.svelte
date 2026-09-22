<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import QrScanner from "qr-scanner";
  import Select from "./Select.svelte";

  let { data } = $props();
  let allPOI = $derived(JSON.parse(data.allPOI));
  // $inspect("allPOI", allPOI);

  let url = $derived($page.url);
  let facility = $derived(url.searchParams.get("f") || Object.keys(allPOI)[0]);
  // $inspect("facility", facility);
  let start = $derived(url.searchParams.get("s") || "");
  // $inspect("start", start);
  let destination = $derived(url.searchParams.get("d") || "");
  // $inspect("destination", destination);

  let options = $derived(
    JSON.parse(decodeURIComponent(url.searchParams.get("o"))) || {},
  );
  let oParam = $derived(encodeURIComponent(JSON.stringify(options)));

  function facpoi(facility) {
    let facpoi = {};
    const locations = allPOI[facility];
    for (const [locationName, locationData] of Object.entries(locations)) {
      let locpoi = {};
      facpoi[locationName] = locpoi;
      const locationGeo = locationData.location;
      for (const [id, properties] of Object.entries(locationData.poi)) {
        locpoi[id] = properties;
      }
    }
    return facpoi;
  }

  let poi = $derived(facpoi(facility));
  // $inspect("poi", poi);

  let qrVideo = $state();
  // $inspect(qrVideo);
  let scanner = $derived(createScanner(qrVideo));
  function createScanner(qrVideo) {
    if (!browser || !qrVideo) return;
    return new QrScanner(qrVideo, (result) => handleQRResult(result.data), {
      highlightScanRegion: true,
      highlightCodeOutline: true,
    });
  }
  let isScanning = $state(false);

  function toggleScanner() {
    if (!browser || !qrVideo) return;

    if (isScanning) {
      scanner?.stop();
      isScanning = false;
    } else {
      scanner.start();
      isScanning = true;
    }
  }

  function handleQRResult(resultString) {
    if (!resultString) return;

    scanner?.stop();
    isScanning = false;

    if (resultString.toLowerCase().startsWith("http")) {
      const url = new URL(resultString);
      const params = url.searchParams;

      if (params.get("s")) start = params.get("s");
      if (params.get("d")) destination = params.get("d");
      options = JSON.parse(decodeURIComponent(params.get("o")));

      // keine Parameter in URL: wahrscheinlich ein verkürzter Link
      // (Seite aufrufen um weitergeleitet zu werden)
      if (!params.get("s") && !params.get("d")) {
        window.location.href = resultString;
      }
    } else if (resultString.startsWith("?")) {
      const params = new URLSearchParams(resultString);
      if (params.get("s")) start = params.get("s");
      if (params.get("d")) destination = params.get("d");
    }
  }

  let locations = $derived((skip = "") => {
    let groups = {};
    for (const [locname, locpoi] of Object.entries(poi)) {
      let choices = [];
      for (const [poiid, properties] of Object.entries(locpoi)) {
        const value = `${locname}, ${poiid}`;
        if (value === skip) continue;
        let choice = {
          value,
          name: properties.names.join(" / "),
        };
        for (const [k, v] of Object.entries(properties)) {
          if (k === "names") continue;
          choice[k] = v;
        }
        choices.push(choice);
      }
      if (choices.length > 0) groups[locname] = choices;
    }
    return groups;
  });
  // $inspect("locations", locations());
</script>

<form action="/nav">
  <fieldset>
    <legend>Route</legend>
    {#if Object.keys(allPOI).length !== 1}
      <select id="f" name="f" bind:value={facility} required>
        {#each Object.keys(allPOI) as fac}
          <option value={fac}>{fac}</option>
        {/each}
      </select>
    {/if}

    <Select
      name="s"
      bind:value={start}
      placeholder="-- Bitte Startort auswählen --"
      required
      groups={locations(destination)}
    />

    <Select
      name="d"
      bind:value={destination}
      placeholder="-- Bitte Zielort auswahlen --"
      required
      groups={locations(start)}
    />

    <button
      type="button"
      onclick={toggleScanner}
      hidden={!QrScanner?.hasCamera()}
    >
      {isScanning ? "QR Scanner stoppen" : "QR Code scannen"}
    </button>

    <div id="qr-group" hidden={!isScanning}>
      <video bind:this={qrVideo} id="qr-video" playsinline autoplay></video>
    </div>
  </fieldset>

  <fieldset>
    <legend>Optionen</legend>
    <label>
      <input type="checkbox" bind:checked={options.accessible} />
      Barrierefreiheit
    </label>

    <input type="hidden" name="o" value={oParam} />
  </fieldset>

  <button type="submit" disabled={!start || !destination}> Navigieren </button>
</form>

<style>
  fieldset {
    border: 1px solid var(--border-muted);
    margin: 8px 0;
    padding: 8px;
    border-radius: 12px;
  }

  select {
    font-size: var(--font-size);
    width: 100%;
    margin: 0 0 12px;
    padding: 10px;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border-muted);
    border-radius: 8px;
  }

  button {
    font-size: var(--font-size);
    width: 100%;
    margin: 12px 0;
    padding: 10px;
    background: var(--primary);
    color: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
  }
  button:disabled {
    background: var(--bg);
    color: var(--text-muted);
    border: 1px solid var(--border-muted);
  }

  legend {
    font-size: var(--font-size-title);
  }

  label {
    display: block;
    margin: 6px;
  }

  /* Checkbox Styles Tutorial siehe */
  /* https://moderncss.dev/pure-css-custom-checkbox-style/ */
  input[type="checkbox"] {
    /* default appearance entfernen, dann eigene appearance hinzufügen */
    appearance: none;
    width: 1.25rem;
    height: 1.25rem;
    border: 2px solid var(--border);
    border-radius: 4px;
    background: var(--bg);
    display: inline-grid;
    place-content: center;
    margin: 0;
    cursor: pointer;
    transition: background 120ms ease-in-out;
  }
  input[type="checkbox"]:checked {
    background: var(--highlight);
  }
  input[type="checkbox"]::before {
    content: "";
    width: 0.65rem;
    height: 0.65rem;
    background: var(--primary);
    transform: scale(0);
    transition: transform 120ms ease-in-out;
    clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
  }
  input[type="checkbox"]:checked::before {
    transform: scale(1);
  }

  video {
    max-width: 100%;
    border-radius: 8px;
  }
</style>
