import QrScanner from "https://nimiq.github.io/qr-scanner/qr-scanner.min.js";

const serverURL = window.location.origin + "/";

// Wenn mehrere Einrichtungen auf dem Server gehostet werden, muss die Zieleinrichtung festgelegt werden
// Wenn gesetzt, aber der Server nur eine Einrichtung hostet, wird der Parameter ignoriert
const facility = "hs-harz";

// Wenn zukünftig auch z.B. Passwörter zu bestimmten Einrichtungsdaten genutzt werden,
// könnten diese über die 'verification' übermittelt werden (nicht implementiert)
let verification = "";

let start = null;
let destination = null;

const pathSetter = new Promise(setPathEnds);

function setPathEnds(resolve, reject) {
    const urlParams = new URLSearchParams(window.location.search);

    start = urlParams.get('s');
    if (start) start = decodeURIComponent(start);
    destination = urlParams.get('d');
    if (destination) destination = decodeURIComponent(destination);

    if (start && destination) { resolve(); return; };

    offerQRScan(resolve, reject);
};

function offerQRScan(resolve, reject) {
    const qrPromise = new Promise((resolve, reject) => {
        if (confirm("QR-Code lesen?")) {
            handleQRScan(resolve, reject);
        } else {
            resolve();
        };
    });

    qrPromise.then(() => {  // so viel wie möglich aus qrCode gelesen
        const startPromise = new Promise((resolve, reject) => {
            if (!start) {
                setStartManually(resolve, reject);
            } else {
                resolve();
            };
        });
        startPromise.then(() => {  // start erfolgreich festgelegt
            const destinationPromise = new Promise((resolve, reject) => {
                if (!destination) {
                    setDestinationManually(resolve, reject);
                } else {
                    resolve();
                };
            });
            destinationPromise.then(() => {  // destination erfolgreich festgelegt
                resolve();
            });
        });
    });
};

function handleQRScan(resolve, reject) {
    const qrGroup = document.createElement('div');
    qrGroup.id = 'qr-group';

    // const qrInfo = document.createElement('p');
    // qrInfo.textContent = "Wenn der gescannte QR-Code auf eine Website hinweist, wird ihm automatisch gefolgt. Scannen Sie nur Codes, denen Sie vertrauen.";
    // qrGroup.appendChild(qrInfo);

    const qrVideo = document.createElement('video');
    qrVideo.id = 'qr-video';
    qrVideo.autoplay = true;

    qrGroup.appendChild(qrVideo);
    document.body.appendChild(qrGroup);

    const scanner = new QrScanner(
        qrVideo,
        (result) => {
            scanner.stop();
            qrGroup.remove();
            const resultString = result.data;
            if (resultString.toLowerCase().startsWith('http')) {
                const url = new URL(resultString);  // nicht direkt URLSearchParams, da es mit ganzen URLs nicht umgehen kann
                const urlParams = url.searchParams;
                start = urlParams.get('s') || start;
                destination = urlParams.get('d') || destination;

                // Die gelesene URL könnte ein verkürzter Link sein,
                // in dem die URL Parameter nicht enthalten sind.
                // Dies ist zu unterstützen, damit QR-Codes kleiner sein können.
                // Am einfachsten ist dann, der URL einfach zu folgen.
                if (
                    !start && !destination
                ) window.location.href = resultString;
            } else if (resultString.startsWith('?')) {
                const urlParams = new URLSearchParams(resultString);
                start = urlParams.get('s') || start;
                destination = urlParams.get('d') || destination;
            }
            resolve();
        },
        {
            highlightScanRegion: true,
            highlightCodeOutline: true,
        }
    );

    scanner.start();
};

function setStartManually(resolve, reject) {
    const getPOIPromise = new Promise((resolve, reject) => {
        getPOI("Bitte wähle den Startort aus.", resolve, reject);
    });

    getPOIPromise.then((startResult) => {
        start = startResult;
        resolve();
    });
};

function setDestinationManually(resolve, reject) {
    const getPOIPromise = new Promise((resolve, reject) => {
        getPOI("Bitte wähle den Zielort aus.", resolve, reject);
    });

    getPOIPromise.then((destinationResult) => {
        destination = destinationResult;
        resolve();
    });
};

let poiCache = null;
function getPOI(userMessage, resolve, reject) {
    const poiPromise = new Promise((resolve, reject) => {
        if (!poiCache) {
            const xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
            xhr.open('GET', serverURL + "poi/" + facility + "/", + verification);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {  // 200 = OK
                        poiCache = JSON.parse(xhr.responseText,
                            (key, value) => {
                                return JSON.parse(value);
                            });
                        resolve();
                    } else {
                        console.error('Error:', xhr.status, xhr.responseText);
                        reject();
                    }
                }
            };
            xhr.send();
        } else {  // poi wurden bereits geladen
            resolve();
        };
    });

    poiPromise.then(() => {
        const selectElement = document.createElement("select");
        document.body.appendChild(selectElement);

        let compiledChoices = [];
        for (let building of Object.keys(poiCache)) {
            let location = poiCache[building].location;
            for (let [id, names] of Object.entries(poiCache[building].poi)) {
                let value = building + ", " + id;
                let label = names.join(" / ") + " (" + building + ")";
                compiledChoices.push({ value: value, label: label });
            }
        }

        const selector = new Choices(selectElement, {
            placeholderValue: userMessage,
            choices: compiledChoices
        });

        selectElement.addEventListener(
            'choice',
            function (event) {
                selector.destroy();
                selectElement.remove();
                resolve(event.detail.value);
            },
            false
        );
    });
};



let path = null;
pathSetter.then(() => {  // start und destination erfolgreich festgelegt
    console.log(start);
    console.log(destination);
    const getPath = new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', serverURL + "path/" + encodeURIComponent(start) + "/" + encodeURIComponent(destination) + "/" + facility);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {  // 200 = OK
                    path = JSON.parse(xhr.responseText);
                    resolve();
                } else {
                    console.error('Error:', xhr.status, xhr.responseText);
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
        };
        const locationsToWalk = nextLocationIterator();

        function* nextMapIterator(locationPath) {
            for (let [locationName, mapPaths] of Object.entries(locationPath)) {
                for (let mapPath of mapPaths) {
                    for (let [mapName, waypointsData] of Object.entries(mapPath)) {
                        let mapImage = null;
                        yield new Promise((resolve, reject) => {
                            const xhr = new XMLHttpRequest();
                            xhr.open('GET', serverURL + "map/" + mapName + "/" + locationName + "/" + facility);
                            xhr.onreadystatechange = function () {
                                if (xhr.readyState === XMLHttpRequest.DONE) {
                                    if (xhr.status === 200) {  // 200 = OK
                                        mapImage = new Image();
                                        mapImage.src = "data:image/png;base64," + xhr.responseText;
                                        resolve([mapImage, waypointsData]);
                                    } else {
                                        console.error('Error:', xhr.status, xhr.responseText);
                                        reject();
                                    }
                                }
                            }
                            xhr.send();
                        });
                    }
                }
            }
        };
        function showNextLocation() {
            const nextLocation = locationsToWalk.next();
            if (nextLocation.done) {
                // Weg komplett abgearbeitet

                if (confirm("Das Ziel ist erreicht. Soll die Seite neu geladen werden?")) {
                    // Wenn der Weg durch Query Parameter angegeben wurde,
                    // würde .reload() diese Parameter ausgefüllt lassen.
                    // Dem Nutzer soll die Möglichkeit gegeben werden,
                    // diese Parameter entfernen zu lassen.
                    if (window.location.search && confirm("Es sind möglicherweise feste Ziele in der URL angegeben. Sollen diese entfernt werden?")) {
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
                    const responseHTML = `<span>Navigation zu ${nextLocation.value} über</span><br>`
                        // Google Maps URL Documentation für den Google Maps Link
                        // https://developers.google.com/maps/documentation/urls/get-started#directions-action
                        // target="_blank" bedeutet, dass der Link in einem neuen Tab geöffnet wird
                        + `<a href="https://www.google.com/maps/dir/?api=1&destination=${nextLocation.value}" target="_blank">Google Maps</a><br>`
                        // Apple Maps URL Documentation für den Apple Maps Link
                        // https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/MapLinks/MapLinks.html
                        + `<a href="https://maps.apple.com/?daddr=${nextLocation.value}" target="_blank">Apple Maps</a>`;

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
                    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    function update_image_sizes() {
                        mapImage.style.position = "absolute";
                        svg.style.position = "absolute";

                        const widthScale = window.innerWidth / mapImage.naturalWidth;
                        const heightScale = window.innerHeight / mapImage.naturalHeight;
                        // mapImage zentrieren und auf Bildschirmgröße wie durch 'object-fit: contain' skalieren
                        if (widthScale > heightScale) {  // Freiraum in der Breite, also wird nach Höhe skaliert
                            const newWidth = mapImage.naturalWidth * heightScale;
                            mapImage.style.top = "0px";
                            mapImage.style.left = `${(window.innerWidth - newWidth) / 2}px`;
                            mapImage.style.width = `${newWidth}px`;
                            mapImage.style.height = `${window.innerHeight}px`;
                        } else {  // Freiraum in der Höhe, also wird nach Breite skaliert
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
                    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    path.style.fill = "none"; // kein geschlossener Pfad, daher wird er nicht ausgefüllt
                    path.style.stroke = "red"; // die Linie des Pfades kann beliebig gefärbt werden, Rot ist nur gut sichtbar

                    // um zu kennzeichnen, wo gestartet wird, kann der erste Wegpunkt als Kreis auf der Linie dargestellt werden
                    // am einfachsten ist, dafür einen Kreis unabhängig vom path ins SVG zu bringen
                    // https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/circle
                    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
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
                        const pathD = `M ${waypointsData[0].x * scale} ${waypointsData[0].y * scale} `
                            // folgende Wegpunkte können über gerade Linien verbunden werden
                            // L bedeutet LineTo in absoluten Einheiten von oben links (l wäre relativ zum letzten Punkt)
                            + waypointsData.slice(1) // ignoriere den ersten Wegpunkt 
                                .map(waypoint => `L ${waypoint.x * scale} ${waypoint.y * scale}`)  // statt eines Wegpunktobjekts wird "L x y" eingefügt
                                .join(" ");  // alle "L x y" Wegpunkte werden mit Leerzeichen zu einem einzelnen String verkettet

                        path.setAttribute("d", pathD);
                    }
                    window.addEventListener("resize", updatePathD);
                    updatePathD();

                    svg.appendChild(path);

                    svg.onclick = () => {
                        if (confirm("Zur nächsten Karte wechseln?")) showNextMap();
                    };
                });
            };
            showNextMap();  // erste Karte automatisch laden
        };
        showNextLocation(); // ersten Standort automatisch laden
    });
});