<script>
  let { children } = $props();
</script>

{@render children()}

<style>
  /* Theme Erkennung */
  /* https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme */

  /* Color Scheme generiert mit https://www.iamsajid.com/ui-colors/ */
  /* neutral / vivid 0.05; warmer / cooler 210 */

  /* light mode */
  :root {
    --font-size: 16px;
    --font-size-title: 24px;

    --path-color: hsl(0, 95%, 36%);

    --bg-dark: hsl(189 44% 88%);
    --bg: hsl(189 78% 93%);
    --bg-light: hsl(189 100% 98%);
    --text: hsl(193 100% 3%);
    --text-muted: hsl(189 43% 24%);
    --highlight: hsl(189 100% 96%);
    --border: hsl(189 22% 46%);
    --border-muted: hsl(189 25% 58%);
    --primary: hsl(187 100% 11%);
    --secondary: hsl(7 51% 30%);
    --danger: hsl(9 21% 41%);
    --warning: hsl(52 23% 34%);
    --success: hsl(147 19% 36%);
    --info: hsl(217 22% 41%);
  }
  @media (prefers-color-scheme: dark) {
    /* dark mode */
    :root {
      --path-color: hsl(0, 95%, 36%);

      --bg-dark: hsl(195 100% 1%);
      --bg: hsl(191 96% 3%);
      --bg-light: hsl(189 61% 7%);
      --text: hsl(189 100% 91%);
      --text-muted: hsl(189 31% 66%);
      --highlight: hsl(189 29% 35%);
      --border: hsl(189 43% 24%);
      --border-muted: hsl(188 90% 12%);
      --primary: hsl(189 59% 59%);
      --secondary: hsl(9 69% 73%);
      --danger: hsl(9 26% 64%);
      --warning: hsl(52 19% 57%);
      --success: hsl(146 17% 59%);
      --info: hsl(217 28% 65%);
    }
  }

  :root {
    background-color: var(--bg-dark);
    transition: background-color 0.3s ease;
    color: var(--text);
    font-family: arial;
    font-size: var(--font-size);
  }
</style>
