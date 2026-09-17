<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let { data } = $props();
  let path = $derived(data.path);
</script>

{#if path}
  {#each path as location}
    {#if typeof location === "string"}
      <span>
        Navigieren Sie nun gebäudeübergreifend zur Adresse '{location}'. Links
        zu
      </span>
      <a
        href="https://www.google.com/maps/dir/?api=1&destination={encodeURIComponent(
          location,
        )}"
        target="_blank">Google Maps</a
      >
      <span> und </span>
      <a
        href="https://maps.apple.com/?daddr={encodeURIComponent(location)}"
        target="_blank">Apple Maps</a
      >
      <span> wurden von dieser Seite generiert.</span>
    {:else}
      {#each Object.values(location) as maps}
        {#each maps as map}
          {#each Object.entries(map) as [mapname, mapdata]}
            <div id="map">
              <img
                id="mapimg"
                src={"data:image/png;base64," + mapdata.b64}
                alt="Karte von '{mapname}'"
              />
              <svg id="mapsvg">
                <circle
                  id="mappathstart"
                  cx="{mapdata.wp[0].x}px"
                  cy="{mapdata.wp[0].y}px"
                  r="5px"
                  fill="red"
                ></circle>
                <path
                  id="mappath"
                  fill="none"
                  stroke="red"
                  d="M {mapdata.wp[0].x} {mapdata.wp[0].y} {mapdata.wp
                    .slice(1)
                    .map((waypoint) => `L ${waypoint.x} ${waypoint.y}`)
                    .join(' ')}"
                ></path>
              </svg>
            </div>
          {/each}
        {/each}
      {/each}
    {/if}
  {/each}
{/if}

<style>
  #map {
    position: relative;
    display: block;

    /* zentrieren */
    left: 50%;
    transform: translateX(-50%);
  }

  #mapimg {
    display: block;
    pointer-events: none;
  }

  #mapsvg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
</style>
