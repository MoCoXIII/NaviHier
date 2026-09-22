<script>
  import { browser } from "$app/environment";
  import "choices.js/public/assets/styles/choices.css";

  let { name, value = $bindable(), placeholder, required, groups } = $props();

  let Choices = $state();
  let selector = $state();
  let bindSelector = $derived(() => {
    if (!selector) {
      return undefined;
    }

    let choices = [];
    let extraSearchFields = [];
    for (const [group, _choices] of Object.entries(groups)) {
      let c = [];
      let g = { label: group, choices: c };
      for (const { value, name, ...flags } of Object.values(_choices)) {
        c.push({ value, label: name, customProperties: flags });
        for (const k of Object.keys(flags)) {
          const possibleProperty = "customProperties." + k;
          if (!extraSearchFields.includes(possibleProperty)) {
            extraSearchFields.push(possibleProperty);
          }
        }
      }
      choices.push(g);
    }

    return new Choices(selector, {
      placeholderValue: placeholder,
      choices: choices,
      searchFields: ["label", "value", ...extraSearchFields],
      searchResultLimit: -1,
    });
  });
  let boundSelector = $derived(bindSelector());

  // bindet Choices an den selector, indem die Funktion wenn möglich nach Aktualisierung aufgerufen wird
  // ohne diese Zeile wird Choices nicht an den selector gebunden
  // (boundSelector muss mindestens ein Mal genutzt werden, damit die Funktion hinter bindSelector überhaupt aufgerufen wird)
  // (hätte auch $inspect sein können, das ist aber nur im dev Modus aktiv, also $effect als Alternative)
  $effect(() => boundSelector);

  if (browser) {
    import("choices.js").then((library) => {
      Choices = library.default;
    });
  }
</script>

{#if Choices}
  <select {name} bind:value {required} bind:this={selector}></select>
{/if}

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

  :root {
    --choices-primary-color: var(--primary);
    --choices-item-color: var(--text);
    --choices-bg-color: var(--bg);
    --choices-bg-color-dropdown: var(--bg-light);
    --choices-keyline-color: var(--border);
    --choices-bg-color-disabled: var(--bg-dark);
    --choices-item-disabled-color: var(--text-muted);
    --choices-disabled-color: var(--bg-dark);
    --choices-highlighted-color: var(--highlight);
    --choices-icon-cross: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjMDAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==");
    --choices-icon-cross-inverse: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjRkZGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==");
    --choices-font-size-lg: var(--font-size);
    --choices-font-size-md: var(--font-size);
    --choices-font-size-sm: var(--font-size);
    --choices-border-radius: 8px;
    --choices-width: 100%;
    --choices-inner-padding: 4px 0;

    :global {
      .choices__input {
        color: var(--text);
      }
    }
  }
</style>
