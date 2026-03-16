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


// Test: interaktiver Raumplan aus JSON

const mapImage = document.querySelector("img[usemap]");
let selectedRooms = [];
let drawnPaths = [];
let JSONData;
let currentMap;

await fetch("Test Gebäudeplan/Gebäudeplan_Bsp.json")
    .then(response => response.json())
    .then(data => {
        JSONData = data;
        let map = data.maps[0];
        currentMap = map;
        for (let room of map.rooms) {
            const area = room;
            const areaElement = document.createElement("area");
            areaElement.setAttribute("shape", area.shape);
            areaElement.setAttribute("coords", area.coords.join(","));
            areaElement.onclick = (() => roomClicked(area));
            document.querySelector("map").appendChild(areaElement);
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
    handleNewTargets();
}


function handleNewTargets() {
    drawnPaths.forEach(path => path.remove());
    drawnPaths = [];
    if (selectedRooms.length == 2) {
        const startRoomID = selectedRooms[0];
        const endRoomID = selectedRooms[1];

        const waypoints = currentMap.waypoints;
        const startRoom = waypoints.find(waypoint => waypoint.links.some(link => link === ("room:" + startRoomID)));
        const endRoom = waypoints.find(waypoint => waypoint.links.some(link => link === ("room:" + endRoomID)));

        const startWaypoint = startRoom.id;
        const endWaypoint = endRoom.id;

        const traversedWaypoints = traverseWaypoints(startWaypoint, endWaypoint, waypoints);

        const traversedWaypointIDs = traversedWaypoints.map(waypoint => waypoint.id);
        const traversedWaypointCoords = traversedWaypoints.map(waypoint => [waypoint.x, waypoint.y]);

        drawPath(traversedWaypointCoords);
    }
}

function traverseWaypoints(start, end, waypoints) {
    const queue = [[start, []]];
    const visited = new Set();

    while (queue.length > 0) {
        const [node, path] = queue.shift();
        if (visited.has(node)) continue;
        visited.add(node);

        if (node === end) return [...path, end].map(id => waypoints.find(waypoint => waypoint.id === id));

        for (const link of waypoints.find(waypoint => waypoint.id === node).links) {
            if (link.startsWith("room:")) continue;
            const nextNode = link.split(":")[1];
            queue.push([nextNode, [...path, node]]);
        }
    }

    return null;
}


function drawPath(coordsList) {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    const mapRect = mapImage.getBoundingClientRect();
    svg.setAttribute("style", `position: absolute; top: ${mapRect.top}px; left: ${mapRect.left}px; width: ${mapRect.width}px; height: ${mapRect.height}px; pointer-events: none;`);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", "M " + coordsList.map(coords => `${coords[0]} ${coords[1]} `).join("L"));
    path.setAttribute("stroke", "red");
    path.setAttribute("stroke-width", "5");
    path.setAttribute("fill", "none");
    svg.appendChild(path);
    mapImage.parentNode.appendChild(svg);
    drawnPaths.push(svg);
}

// Tool: Position des Mausklicks relativ zum Bild auslesen
// document.addEventListener("click", (event) => {
//     const mapRect = mapImage.getBoundingClientRect();
//     const mousePosition = {
//         x: event.clientX - mapRect.left,
//         y: event.clientY - mapRect.top
//     };
//     console.log(mousePosition.x, mousePosition.y);
// });