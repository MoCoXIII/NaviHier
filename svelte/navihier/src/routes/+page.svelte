<script>
  import { goto } from "$app/navigation";
  import { redirect } from '@sveltejs/kit';

  redirect(307, "/pick");

  let path = null;
  pathSetter.then(() => {
    // start und destination erfolgreich festgelegt
    console.log(start);
    console.log(destination);
    const getPath = new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open(
        "GET",
        serverURL +
          "path/" +
          encodeURIComponent(start) +
          "/" +
          encodeURIComponent(destination) +
          "/" +
          facility,
      );
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // 200 = OK
            path = JSON.parse(xhr.responseText);
            resolve();
          } else {
            console.error("Error:", xhr.status, xhr.responseText);
            reject();
          }
        }
      };
      xhr.send();
    });

    getPath.then(() => {
      console.log(path);

      function* nextLocationIterator() {
        for (let locationPath of path) {
          if (locationPath === null) {
            // Weg konnte nicht gefunden werden
            yield `<h1>Kein Weg gefunden</h1>`;
          } else {
            // Standort-Wegdaten wiedergeben
            yield locationPath;
          }
        }
      }
      const locationsToWalk = nextLocationIterator();

      function* nextMapIterator(locationPath) {
        for (let [locationName, mapPaths] of Object.entries(locationPath)) {
          for (let mapPath of mapPaths) {
            for (let [mapName, waypointsData] of Object.entries(mapPath)) {
              let mapImage = null;
              yield new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open(
                  "GET",
                  serverURL +
                    "map/" +
                    mapName +
                    "/" +
                    locationName +
                    "/" +
                    facility,
                );
                xhr.onreadystatechange = function () {
                  if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                      // 200 = OK
                      mapImage = new Image();
                      mapImage.src =
                        "data:image/png;base64," + xhr.responseText;
                      resolve([mapImage, waypointsData]);
                    } else {
                      console.error("Error:", xhr.status, xhr.responseText);
                      reject();
                    }
                  }
                };
                xhr.send();
              });
            }
          }
        }
      }
      function showNextLocation() {
        const nextLocation = locationsToWalk.next();
        if (nextLocation.done) {
          // Weg komplett abgearbeitet

          if (
            confirm("Das Ziel ist erreicht. Soll die Seite neu geladen werden?")
          ) {
            // Wenn der Weg durch Query Parameter angegeben wurde,
            // würde .reload() diese Parameter ausgefüllt lassen.
            // Dem Nutzer soll die Möglichkeit gegeben werden,
            // diese Parameter entfernen zu lassen.
            if (
              window.location.search &&
              confirm(
                "Es sind möglicherweise feste Ziele in der URL angegeben. Sollen diese entfernt werden?",
              )
            ) {
              window.location.search = "";
            } else {
              window.location.reload();
            }
          }
          return;
        }
        if (typeof nextLocation.value === "string") {
          // Weg zu anderem Standort, nutze Kartendienst
          const showGeoLinks = new Promise((resolve, reject) => {
            const responseHTML =
              `<span>Navigation zu ${nextLocation.value} über</span><br>` +
              // Google Maps URL Documentation für den Google Maps Link
              // https://developers.google.com/maps/documentation/urls/get-started#directions-action
              // target="_blank" bedeutet, dass der Link in einem neuen Tab geöffnet wird
              `<a href="https://www.google.com/maps/dir/?api=1&destination=${nextLocation.value}" target="_blank">Google Maps</a><br>` +
              // Apple Maps URL Documentation für den Apple Maps Link
              // https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/MapLinks/MapLinks.html
              `<a href="https://maps.apple.com/?daddr=${nextLocation.value}" target="_blank">Apple Maps</a>`;

            document.body.innerHTML = responseHTML;

            const thereButton = document.createElement("button");
            thereButton.innerHTML = "Ich bin angekommen";
            thereButton.onclick = resolve;
            document.body.appendChild(document.createElement("br"));
            document.body.appendChild(thereButton);
          });
          showGeoLinks.then(() => {
            document.body.innerHTML = "";
            showNextLocation();
          });
          return;
        }
        const mapsToWalk = nextMapIterator(nextLocation.value);
        function showNextMap() {
          document.body.innerHTML = "";
          const nextMapIteratorResponse = mapsToWalk.next();
          if (nextMapIteratorResponse.done) {
            // Ziel innerhalb des Gebäudes erreicht
            showNextLocation();
            return;
          }
          const nextMapPromise = nextMapIteratorResponse.value;
          nextMapPromise.then(([mapImage, waypointsData]) => {
            document.body.appendChild(mapImage);

            // über das MapImage ein SVG überlagern
            const svg = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "svg",
            );
            function update_image_sizes() {
              mapImage.style.position = "absolute";
              svg.style.position = "absolute";

              const widthScale = window.innerWidth / mapImage.naturalWidth;
              const heightScale = window.innerHeight / mapImage.naturalHeight;
              // mapImage zentrieren und auf Bildschirmgröße wie durch 'object-fit: contain' skalieren
              if (widthScale > heightScale) {
                // Freiraum in der Breite, also wird nach Höhe skaliert
                const newWidth = mapImage.naturalWidth * heightScale;
                mapImage.style.top = "0px";
                mapImage.style.left = `${(window.innerWidth - newWidth) / 2}px`;
                mapImage.style.width = `${newWidth}px`;
                mapImage.style.height = `${window.innerHeight}px`;
              } else {
                // Freiraum in der Höhe, also wird nach Breite skaliert
                const newHeight = mapImage.naturalHeight * widthScale;
                mapImage.style.top = `${(window.innerHeight - newHeight) / 2}px`;
                mapImage.style.left = "0px";
                mapImage.style.width = `${window.innerWidth}px`;
                mapImage.style.height = `${newHeight}px`;
              }

              // Sind die Werte für das Bild festgelegt, kann das SVG sie kopieren
              svg.style.top = mapImage.style.top;
              svg.style.left = mapImage.style.left;
              svg.style.width = mapImage.style.width;
              svg.style.height = mapImage.style.height;
            }
            update_image_sizes();
            document.body.appendChild(svg);

            // Dokumentation für folgende Nutzung des SVG Path Elements
            // https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d
            const path = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "path",
            );
            path.style.fill = "none"; // kein geschlossener Pfad, daher wird er nicht ausgefüllt
            path.style.stroke = "red"; // die Linie des Pfades kann beliebig gefärbt werden, Rot ist nur gut sichtbar

            // um zu kennzeichnen, wo gestartet wird, kann der erste Wegpunkt als Kreis auf der Linie dargestellt werden
            // am einfachsten ist, dafür einen Kreis unabhängig vom path ins SVG zu bringen
            // https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/circle
            const circle = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "circle",
            );
            circle.style.cx = `${waypointsData[0].x}px`;
            circle.style.cy = `${waypointsData[0].y}px`;
            circle.style.r = "5px";
            circle.style.fill = "red";
            svg.appendChild(circle);

            // um den Path auf die aktuelle Bildgröße anzupassen, muss sein d-Parameter öfter festgelegt werden können
            function updatePathD() {
              // kein Update, wenn der Nutzer in das Bild gezoomt ist
              if (window.visualViewport.scale > 1) return;

              // bevor die Positionen der Wegpunkte auf die aktuelle Bildgröße gebracht werden, muss die Bildgröße korrigiert werden
              update_image_sizes();

              // um die Positionen der Wegpunkte auf die aktuelle Bildgröße anzupassen,
              // muss die Skalierung von der eigentlichen Bildgröße ermittelt werden
              const scale = mapImage.clientWidth / mapImage.naturalWidth;
              // dann kann jeder Wegpunkt auf die aktuelle Bildgröße skaliert werden
              // ebenso muss der Kreis angepasst werden
              circle.style.cx = `${waypointsData[0].x * scale}px`;
              circle.style.cy = `${waypointsData[0].y * scale}px`;

              // der SVG Path startet bei 0,0
              // daher muss zum ersten Punkt bewegt werden, ohne die Linie zu zeichnen
              // M bedeutet MoveTo in absoluten Einheiten von oben links (m wäre relativ zum letzten Punkt)
              const pathD =
                `M ${waypointsData[0].x * scale} ${waypointsData[0].y * scale} ` +
                // folgende Wegpunkte können über gerade Linien verbunden werden
                // L bedeutet LineTo in absoluten Einheiten von oben links (l wäre relativ zum letzten Punkt)
                waypointsData
                  .slice(1) // ignoriere den ersten Wegpunkt
                  .map(
                    (waypoint) =>
                      `L ${waypoint.x * scale} ${waypoint.y * scale}`,
                  ) // statt eines Wegpunktobjekts wird "L x y" eingefügt
                  .join(" "); // alle "L x y" Wegpunkte werden mit Leerzeichen zu einem einzelnen String verkettet

              path.setAttribute("d", pathD);
            }
            window.addEventListener("resize", updatePathD);
            updatePathD();

            svg.appendChild(path);

            svg.onclick = () => {
              if (confirm("Zur nächsten Karte wechseln?")) showNextMap();
            };
          });
        }
        showNextMap(); // erste Karte automatisch laden
      }
      showNextLocation(); // ersten Standort automatisch laden
    });
  });
</script>

<style>
  body {
    background-color: #000;
    color: #fff;
  }

  input {
    color: #fff;
  }

  /* Choices.js style kopiert von https://github.com/Choices-js/Choices#dark-mode-example und bearbeitet */
  @media (prefers-color-scheme: dark) {
    :root {
      --choices-primary-color: #363636;
      --choices-item-color: rgb(255, 255, 255);
      --choices-text-color: #d6dce0;
      --choices-bg-color: #101010;
      --choices-bg-color-dropdown: #101010;
      --choices-keyline-color: #d6dce0;
      --choices-bg-color-disabled: #181a1b;
      --choices-item-disabled-color: #eee;
      --choices-disabled-color: #8d8d8d;
      --choices-highlighted-color: #16292d;
      --choices-icon-cross: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjMDAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==");
      --choices-icon-cross-inverse: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjEiIHZpZXdCb3g9IjAgMCAyMSAyMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSIjRkZGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0yLjU5Mi4wNDRsMTguMzY0IDE4LjM2NC0yLjU0OCAyLjU0OEwuMDQ0IDIuNTkyeiIvPjxwYXRoIGQ9Ik0wIDE4LjM2NEwxOC4zNjQgMGwyLjU0OCAyLjU0OEwyLjU0OCAyMC45MTJ6Ii8+PC9nPjwvc3ZnPg==");
    }
  }
</style>
