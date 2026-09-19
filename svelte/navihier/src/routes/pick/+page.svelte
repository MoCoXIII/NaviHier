<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import QrScanner from "qr-scanner";

  // TODO
  let { data } = $props();
  const allPOI = $derived(JSON.parse(data.allPOI));
  // $inspect("allPOI", allPOI);

  let url = $derived($page.url);
  let facility = $derived(url.searchParams.get("f") || Object.keys(allPOI)[0]);
  // $inspect("facility", facility);
  let start = $derived(url.searchParams.get("s") || "");
  // $inspect("start", start);
  let destination = $derived(url.searchParams.get("d") || "");
  // $inspect("destination", destination);

  let options = $state({});
  let oParam = $derived(encodeURIComponent(JSON.stringify(options)));

  function facpoi(facility) {
    let facpoi = {};
    const locations = allPOI[facility];
    for (const [locationName, locationData] of Object.entries(locations)) {
      let locpoi = {};
      facpoi[locationName] = locpoi;
      const locationGeo = locationData.location;
      for (const [id, names] of Object.entries(locationData.poi)) {
        locpoi[id] = names;
      }
    }
    return facpoi;
  }

  let poi = $derived(facpoi(facility));
  // $inspect("poi", poi);

  let qrVideo = $state();
  // $inspect(qrVideo);
  let scanner = $state(null);
  let isScanning = $state(false);

  function toggleScanner() {
    if (!browser || !qrVideo) return;

    if (isScanning) {
      scanner?.stop();
      scanner?.destroy();
      scanner = null;
      isScanning = false;
      return;
    }

    scanner = new QrScanner(qrVideo, (result) => handleQRResult(result.data), {
      highlightScanRegion: true,
      highlightCodeOutline: true,
    });

    scanner.start();
    isScanning = true;
  }

  //   $effect(() => {
  //     // im effect zurückgegebene Funktion läuft bei unmount (z.B. Zerstören des Scanner-Video-Elements)
  //     // "If you return a function from the effect, it will be called right before the effect is run again, or when the component is unmounted."
  //     // "An effect can return a teardown function which will run immediately before the effect re-runs [and will] also run when the effect is destroyed, which happens when its parent is destroyed (for example, a component is unmounted) [...]."
  //     // - https://svelte.dev/docs/svelte/$effect
  //     return () => {
  //       scanner?.stop();
  //       scanner?.destroy();
  //     };
  //   });

  function handleQRResult(resultString) {
    if (!resultString) return;

    scanner?.stop();
    isScanning = false;

    if (resultString.toLowerCase().startsWith("http")) {
      const url = new URL(resultString);
      const params = url.searchParams;

      if (params.get("s")) start = params.get("s");
      if (params.get("d")) destination = params.get("d");

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

  let compiledChoices = $derived(() => {
    const choices = [];
    for (let building of Object.keys(poi)) {
      for (let [id, names] of Object.entries(poi[building].poi)) {
        choices.push({
          value: `${building}, ${id}`,
          label: `${names.join(" / ")} (${building})`,
        });
      }
    }
    return choices;
  });
</script>

<form action="/nav">
  <select name="f" bind:value={facility} required>
    {#each Object.keys(allPOI) as fac}
      <option value={fac}>{fac}</option>
    {/each}
  </select>

  <select name="s" bind:value={start} required>
    {#each Object.entries(poi) as [locname, locpoi]}
      {#each Object.entries(locpoi) as [poiid, poinames]}
        {#if `${locname}, ${poiid}` !== destination}
          <option value={`${locname}, ${poiid}`}
            >{poinames.join(" / ")} ({locname})</option
          >
        {/if}
      {/each}
    {/each}
  </select>

  <select name="d" bind:value={destination} required>
    {#each Object.entries(poi) as [locname, locpoi]}
      {#each Object.entries(locpoi) as [poiid, poinames]}
        {#if `${locname}, ${poiid}` !== start}
          <option value={`${locname}, ${poiid}`}
            >{poinames.join(" / ")} ({locname})</option
          >
        {/if}
      {/each}
    {/each}
  </select>

  <button type="button" onclick={toggleScanner}>
    {isScanning ? "QR Scanner stoppen" : "QR Code scannen"}
  </button>

  {#if isScanning}
    <div id="qr-group">
      <video bind:this={qrVideo} id="qr-video" autoplay></video>
    </div>
  {/if}

  <fieldset>
    <legend>Optionen</legend>
    <label>
      <input type="checkbox" bind:checked={options.accessible} />
      Barrierefreiheit
    </label>
  </fieldset>

  <input type="hidden" name="o" value={oParam} />

  <button type="submit" disabled={!start || !destination}> Navigieren </button>
</form>

<style>
  video {
    max-width: 100%;
    border-radius: 8px;
  }
</style>
