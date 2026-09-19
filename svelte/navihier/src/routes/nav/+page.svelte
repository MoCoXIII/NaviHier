<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import Map from "./Map.svelte";

  let { data } = $props();
  let path = $derived(data.path);
</script>

{#if path}
  <div id="pagediv">
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
              <Map {mapdata} {mapname} />
            {/each}
          {/each}
        {/each}
      {/if}
    {/each}
  </div>
{/if}

<style>
  #pagediv {
    width: 100%;
    height: 100%;
    display: block;
    align-items: center;
    justify-content: center;
    border: 1rem;
  }
</style>
