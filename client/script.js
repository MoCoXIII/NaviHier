import QrScanner from "https://nimiq.github.io/qr-scanner/qr-scanner.min.js";

const serverURL = window.location.origin + "/";

// Wenn mehrere Einrichtungen auf dem Server gehostet werden, muss die Zieleinrichtung festgelegt werden
// Wenn gesetzt, aber der Server nur eine Einrichtung hostet, wird der Parameter ignoriert
const facility = "";

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
            if (resultString.startsWith('http')) {
                const url = new URL(resultString);  // nicht direkt URLSearchParams, da es mit ganzen URLs nicht umgehen kann
                const urlParams = url.searchParams;
                start = urlParams.get('s') || start;
                destination = urlParams.get('d') || destination;
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
                    for (let [mapName, waypointIDs] of Object.entries(mapPath)) {
                        let mapImage = null;
                        yield new Promise((resolve, reject) => {
                            const xhr = new XMLHttpRequest();
                            xhr.open('GET', serverURL + "map/" + mapName + "/" + locationName + "/" + facility);
                            xhr.onreadystatechange = function () {
                                if (xhr.readyState === XMLHttpRequest.DONE) {
                                    if (xhr.status === 200) {  // 200 = OK
                                        mapImage = new Image();
                                        mapImage.src = "data:image/png;base64," + xhr.responseText;
                                        resolve(mapImage, waypointIDs);
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
                window.location.reload();
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
                nextMapPromise.then((mapImage, waypointIDs) => {
                    document.body.appendChild(mapImage);

                    // hier Wegpunkte auf Karte anzeigen

                    mapImage.onclick = showNextMap;
                });
            };
            showNextMap();  // erste Karte automatisch laden
        };
        showNextLocation(); // ersten Standort automatisch laden
    });
});


// code hiernach als Kommentar betrachten
// arbeitet sozusagen als "Archiv" bis hier drüber eine bessere Version zustande kommt

//     xhr.open('POST', serverURL + "server");

//     // mime type application/json bedeutet, dass im Server express.json() die JSON Nachricht als solche erkennen kann
//     // siehe https://expressjs.com/en/5x/api.html#express.json
//     // benötigt, damit die POST Anfrage Daten senden kann
//     xhr.setRequestHeader('Content-Type', 'application/json');

//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {  // 200 = OK
//                 const response = JSON.parse(xhr.responseText);

//                 const building = response.building;
//                 const location = encodeURI(response.location);
//                 const room = response.room;

//                 document.getElementById('output').innerHTML = responseHTML;
//             } else {
//                 console.error('Error:', xhr.status);
//             }
//         }
//     };

//     let machineText = null;
//     for (let option of document.querySelectorAll('#rooms option')) {
//         if (option.textContent === text || option.dataset.value === text) {  // option.textContent ist die menschenfreundliche Version der Raumbezeichnung mit alternativen Raumnamen
//             machineText = option.dataset.value;  // im dataset steht der maschinenfreundliche Raumbezeichner (Gebäude, Raum) mit eindeutigem Raum
//             console.log(encodeURI(machineText));
//             break;
//         }
//     }
//     if (!machineText) {
//         alert(`Den Raum "${text}" gibt es in dieser Schreibweise nicht. Bitte wählen Sie einen der vordefinierten Räume aus.`);
//         inputDiv.style.display = "block";
//         return;
//     }
//     let [building, room] = machineText.split(", ");
//     xhr.send(JSON.stringify({ building, room }));
// }