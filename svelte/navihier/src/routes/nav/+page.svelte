<script>
  import { goto } from "$app/navigation";

  import { page } from "$app/stores";
  import { onMount } from "svelte";

  let path = $state([]);

  onMount(async () => {
    const { s, d, f } = $page.url.searchParams;

    const route = await fetch("/path", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ start: s, destination: d, facility: f }),
    });

    path = await route.json();
  });
</script>

{#if !path}
  <h1>Lädt...</h1>
{:else}
  <span>{path}</span>
{/if}
