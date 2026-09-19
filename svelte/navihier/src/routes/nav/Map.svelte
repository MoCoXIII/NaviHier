<script>
  let { mapdata, mapname } = $props();

  let mapimg = $state();
  let mapw = $state();
  let maph = $state();
  let scale = $derived(mapw / mapimg?.naturalWidth);
</script>

<div
  id="map"
  style="
  position: relative; 
  border: 1rem;
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;"
>
  <img
    bind:this={mapimg}
    bind:clientWidth={mapw}
    bind:clientHeight={maph}
    style="
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    display: block;
    pointer-events: none;"
    src={"data:image/png;base64," + mapdata.b64}
    alt="Karte von '{mapname}'"
  />
  <svg
    style="
    position: absolute;
    top: 0;
    left: {mapimg?.left}px;
    width: {mapw}px;
    height: {maph}px;
    pointer-events: none;"
  >
    <circle
      id="mappathstart"
      cx="{mapdata.wp[0].x * scale}px"
      cy="{mapdata.wp[0].y * scale}px"
      r={5 * scale}
      fill="red"
    ></circle>
    <path
      id="mappath"
      fill="none"
      stroke="red"
      stroke-width={3 * scale}
      d="M {mapdata.wp[0].x * scale} {mapdata.wp[0].y * scale} {mapdata.wp
        .slice(1)
        .map((waypoint) => `L ${waypoint.x * scale} ${waypoint.y * scale}`)
        .join(' ')}"
    ></path>
  </svg>
</div>
