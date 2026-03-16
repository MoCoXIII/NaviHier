// script.js als Kontrollzentrum der letztendlichen Anwendung

// Test zum Auslesen von QR-Codes
import QrScanner from "https://nimiq.github.io/qr-scanner/qr-scanner.min.js";

const video = document.getElementById("qr-video");
const qrGroup = document.getElementById("qr-group");

function handleQRresult(result) {
    console.log("QR Scan: ", result);
    if (result.data.startsWith("?")) {
        scanner.stop();
        qrGroup.style.display = "none";
        // window.location.href = result.data;  // TODO: Daten wirklich nutzen
    }
};

const scanner = new QrScanner(
    video,
    (result) => handleQRresult(result),
    {
        highlightScanRegion: true,
        highlightCodeOutline: true,
    }
);

// Um den Scanner zu testen, die unteren beiden Zeilen in der Kommentierung tauschen
// scanner.start();  // Kommentiert wenn Scanner inaktiv sein soll
qrGroup.style.display = "none";  // Kommentiert wenn Scanner aktiv sein soll


// Test: Einfügen einer Area aus JSON

const mapImage = document.querySelector("img[usemap]");
let selectedRooms = [];


await fetch("Test Gebäudeplan/Gebäudeplan_Bsp.json")
    .then(response => response.json())
    .then(data => {
        for (let map of data.maps) {
            for (let room of map.rooms) {
                const area = room;
                const areaElement = document.createElement("area");
                areaElement.setAttribute("shape", area.shape);
                areaElement.setAttribute("coords", area.coords.join(","));
                areaElement.onclick = (() => roomClicked(area));
                document.querySelector("map").appendChild(areaElement);
            }
        }
    });

function roomClicked(area) {
    const oldBox = document.getElementById(area.names[0]);
    if (oldBox) {  // Wenn eine Box für diesen Raum bereits existiert, entferne sie, statt eine neue zu erstellen
        oldBox.remove();
        selectedRooms.splice(selectedRooms.indexOf(area.names[0]), 1);
    } else {
        const areaCoords = area.coords;
        const imgRect = mapImage.getBoundingClientRect();
        const style = `
        position: absolute;
        top: ${areaCoords[1] + imgRect.top}px;
        left: ${areaCoords[0] + imgRect.left}px;
        width: ${areaCoords[2] - areaCoords[0]}px;
        height: ${areaCoords[3] - areaCoords[1]}px;
        background-color: rgba(255, 0, 0, 0.5);
        pointer-events: none;`;
        const box = document.createElement("div");
        box.id = area.names[0];
        box.setAttribute("style", style);
        document.body.appendChild(box);

        // Limitiere die Anzahl der gewählten Räume auf Start- und Zielraum
        selectedRooms.push(area.names[0]);
        if (selectedRooms.length > 2) {
            document.getElementById(selectedRooms.shift()).remove();
        }
    }
}
