// Raumliste zur lokalen Suche vom Server abfragen
const rooms_xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
const serverURL = 'http://localhost:8080/';
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
                    option.value = building + ", " + room[0];
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
    const input = document.getElementById('input').value;
    const xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
    xhr.open('POST', serverURL + "server");

    // mime type application/json bedeutet, dass im Server express.json() die JSON Nachricht als solche erkennen kann
    // siehe https://expressjs.com/en/5x/api.html#express.json
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {  // 200 = OK
                const response = JSON.parse(xhr.responseText);
                document.getElementById('output').textContent = response;
            } else {
                console.error('Error:', xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify({ input }));  // sendet "{input: ...}"
});