// Raumliste zur lokalen Suche vom Server abfragen
const rooms_xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

// Damit die Anwendung auch auf anderen Geräten im lokalen Netzwerk funktioniert,
// wird die IP-Adresse des Backend-Hosts angegeben.
// Da sich diese als dynamische IP-Adresse ändern kann, soll sie bei Bedarf geändert werden können
// const networkAdress = prompt("Geben Sie die IP-Adresse des Host-Geräts im Netzwerk ein: (192.168.___.___)", _default='178.130');
// const networkAdress = '178.130';
// const localServerHostAdress = '192.168.' + networkAdress;
// const serverURL = 'http://' + localServerHostAdress + ':8080/';

const serverURL = 'https://xrlab.hs-harz.de/~adler/navihier/api/';

// sobald auf einem Server mit Domain gehostet wird, kann diese angegeben werden
// const serverURL = 'https://backend.navihier.de/';

const inputDiv = document.getElementById('inputs');
const inputField = document.getElementById('input');
const sendButton = document.getElementById('send');
const qrButton = document.getElementById('qr-button');

import QrScanner from "https://nimiq.github.io/qr-scanner/qr-scanner.min.js";
const qrVideo = document.getElementById("qr-video");
const qrGroup = document.getElementById("qr-group");

function handleQRresult(result) {
    console.log("QR Scan: ", result);
    if (result.data) {
        let data = result.data;
        if (result.data.startsWith("http")) {
            const urlParams = new URLSearchParams(result.data);
            data = decodeURI(urlParams.get('d'));
        } else {
            data = decodeURI(result.data);
        }
        processInput(data);
    }
};

const scanner = new QrScanner(
    qrVideo,
    (result) => handleQRresult(result),
    {
        highlightScanRegion: true,
        highlightCodeOutline: true,
    }
);

rooms_xhr.open('GET', serverURL + "rooms");
rooms_xhr.onreadystatechange = function () {
    if (rooms_xhr.readyState === XMLHttpRequest.DONE) {
        if (rooms_xhr.status === 200) {  // 200 = OK
            let rooms = JSON.parse(rooms_xhr.responseText,
                (key, value) => {
                    return JSON.parse(value);
                });

            const roomsList = document.getElementById('rooms');
            for (let building of Object.keys(rooms)) {
                let location = rooms[building].location;
                for (let room of rooms[building].rooms) {
                    const option = document.createElement('option');
                    option.dataset.value = building + ", " + room[0];
                    option.textContent = room.join(" / ") + " (" + building + ")";
                    roomsList.appendChild(option);
                }
            }

            sendButton.disabled = false;
        } else {
            console.error('Error:', rooms_xhr.status);
        }
    }
};
rooms_xhr.send();

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('d')) {
    inputDiv.style.display = "none";
    let attempts = 0;
    function waitForRoomList() {
        if (attempts > 10) {
            inputDiv.style.display = "block";
            activateInputButtons();
        } else if (sendButton.disabled) {
            attempts++;
            setTimeout(waitForRoomList, 1000);
        } else {
            processInput(decodeURI(urlParams.get('d')));
        }
    };
    waitForRoomList();
} else {
    activateInputButtons();
}

function activateInputButtons() {
    sendButton.addEventListener('click', () => processInput(inputField.value));
    qrButton.addEventListener('click', () => {
        inputDiv.style.display = "none";
        qrGroup.style.display = "block";
        scanner.start();
    });
}

function processInput(text) {
    inputDiv.style.display = "none";
    scanner.stop();
    qrGroup.style.display = "none";

    const xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
    xhr.open('POST', serverURL + "server");

    // mime type application/json bedeutet, dass im Server express.json() die JSON Nachricht als solche erkennen kann
    // siehe https://expressjs.com/en/5x/api.html#express.json
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {  // 200 = OK
                const response = JSON.parse(xhr.responseText);

                const building = response.building;
                const location = encodeURI(response.location);
                const room = response.room;

                const responseHTML = `<span>Navigation zu ${building} über</span><br>`
                    // Google Maps URL Documentation für den Google Maps Link
                    // https://developers.google.com/maps/documentation/urls/get-started#directions-action
                    // target="_blank" bedeutet, dass der Link in einem neuen Tab geöffnet wird
                    + `<a href="https://www.google.com/maps/dir/?api=1&destination=${location}" target="_blank">Google Maps</a><br>`
                    // Apple Maps URL Documentation für den Apple Maps Link
                    // https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/MapLinks/MapLinks.html
                    + `<a href="https://maps.apple.com/?daddr=${location}" target="_blank">Apple Maps</a>`;

                document.getElementById('output').innerHTML = responseHTML;
            } else {
                console.error('Error:', xhr.status);
            }
        }
    };

    let machineText = null;
    for (let option of document.querySelectorAll('#rooms option')) {
        if (option.textContent === text || option.dataset.value === text) {  // option.textContent ist die menschenfreundliche Version der Raumbezeichnung mit alternativen Raumnamen
            machineText = option.dataset.value;  // im dataset steht der maschinenfreundliche Raumbezeichner (Gebäude, Raum) mit eindeutigem Raum
            console.log(encodeURI(machineText));
            break;
        }
    }
    if (!machineText) {
        alert(`Den Raum "${text}" gibt es in dieser Schreibweise nicht. Bitte wählen Sie einen der vordefinierten Räume aus.`);
        inputDiv.style.display = "block";
        return;
    }
    let [building, room] = machineText.split(", ");
    xhr.send(JSON.stringify({ building, room }));
}