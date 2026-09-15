<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import QrScanner from "qr-scanner";

  // TODO
  let { data } = $props();
  let allPOI = $derived(data.allPOI);
  
  let url = $derived($page.url);
  let facility = $derived(url.searchParams.get("f") || "");
  let start = $derived(url.searchParams.get("s") || "");
  let destination = $derived(url.searchParams.get("d") || "");
  
  let poi = $derived(allPOI[facility]);

  let qrVideo = $state();
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

  function navigateToRoute() {
    if (!browser) return;

    const params = new URLSearchParams();
    if (facility) params.set("f", facility);
    if (start) params.set("s", start);
    if (destination) params.set("d", destination);

    goto(`/nav?${params.toString()}`);
  }
</script>

<form onsubmit={navigateToRoute}>
  <select
    name="f"
    bind:value={facility}
    use:choicesAction={{ placeholder: "Select facility" }}
  >
    <option value="">Default</option>
    <!-- TODO -->
  </select>

  <select
    name="s"
    bind:value={start}
    data-target="start"
    use:choicesAction={{ value: start, placeholder: "Select start point" }}
    required
  ></select>

  <select
    name="d"
    bind:value={destination}
    data-target="destination"
    use:choicesAction={{
      value: destination,
      placeholder: "Select destination",
    }}
    required
  ></select>

  <button type="button" onclick={toggleScanner}>
    {isScanning ? "Stop QR Scanner" : "Scan QR Code"}
  </button>

  {#if isScanning}
    <div id="qr-group">
      <video bind:this={qrVideo} id="qr-video" autoplay></video>
    </div>
  {/if}

  <button type="submit" disabled={!start || !destination}> Navigieren </button>
</form>

<style>
  video {
    max-width: 100%;
    border-radius: 8px;
  }
</style>
