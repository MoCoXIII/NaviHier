<script>
  let { name, value = $bindable(), placeholder, required, groups } = $props();
</script>

<select {name} bind:value {required}>
  <option value="" disabled selected hidden>
    {placeholder}
  </option>
  {#each Object.entries(groups) as [group, choices]}
    <optgroup label={group}>
      {#each Object.values(choices) as { value, name, ...flags }}
        <option {value}>
          {name}
        </option>
      {/each}
    </optgroup>
  {/each}
</select>

<style>
  select {
    font-size: var(--font-size);
    width: 100%;
    margin: 0 0 6px;
    padding: 10px;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border-muted);
    border-radius: 8px;
  }
</style>
