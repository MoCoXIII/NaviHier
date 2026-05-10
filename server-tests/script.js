document.getElementById('send').addEventListener('click', () => {
    const input = document.getElementById('input').value;
    const xhr = new XMLHttpRequest();  // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
    xhr.open('POST', 'http://localhost:8080/server');

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