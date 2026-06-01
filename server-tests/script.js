// Raumliste zur lokalen Suche vom Server abfragen
const rooms_xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

// Damit die Anwendung auch auf anderen Geräten im lokalen Netzwerk funktioniert,
// wird die IP-Adresse des Backend-Hosts angegeben.
// Da sich diese als dynamische IP-Adresse ändern kann, soll sie bei Bedarf geändert werden können
// const networkAdress = prompt("Geben Sie die IP-Adresse des Host-Geräts im Netzwerk ein: (192.168.___.___)", _default='178.130');
const networkAdress = '178.130';
const localServerHostAdress = '192.168.' + networkAdress;
const serverURL = 'http://' + localServerHostAdress + ':8080/';

// sobald auf einem Server mit Domain gehostet wird, kann diese angegeben werden
// const serverURL = 'https://backend.navihier.de/';


rooms_xhr.open('GET', serverURL + "rooms");
rooms_xhr.onreadystatechange = function () {
    if (rooms_xhr.readyState === XMLHttpRequest.DONE) {
        if (rooms_xhr.status === 200) {  // 200 = OK
            let rooms = JSON.parse(rooms_xhr.responseText,
                reviver = (key, value) => {
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

            const sendButton = document.getElementById('send');
            sendButton.disabled = false;
        } else {
            console.error('Error:', rooms_xhr.status);
        }
    }
};
rooms_xhr.send();


document.getElementById('send').addEventListener('click', () => {
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
                const location = response.location;
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

    let input = document.getElementById('input').value;
    for (let option of document.querySelectorAll('#rooms option')) {
        if (option.textContent === input) {
            input = option.dataset.value;  // ersetze menschlich lesefreundlichen Text durch maschinenfreundlichen Text
            break;
        }
    }
    if (input === document.getElementById('input').value) {
        alert("Diesen Raum gibt es nicht. Bitte wählen Sie einen der vordefinierten Räume aus.");
        return;
    }
    let [building, room] = input.split(", ");
    xhr.send(JSON.stringify({ building, room }));
});