<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let { data } = $props();
  let path = $derived(data.path);
</script>

{#if path}
  <span>{JSON.stringify(path)}</span>
{/if}
