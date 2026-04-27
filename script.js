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
let selectedRoomPaths = [];
let drawnPaths = [];
let JSONData;
let currentMap;


function rescaleMapImage() {
    const maxWidth = window.innerWidth - 20;
    const maxHeight = window.innerHeight - 20;
    const aspectRatio = mapImage.naturalWidth / mapImage.naturalHeight;
    const width = aspectRatio > 1 ? maxHeight * aspectRatio : maxWidth;
    mapImage.style.width = `${width}px`;
}
window.addEventListener("resize", () => {
    rescaleMapImage();
});

const originalScaleWidth = 1000;  // Die Breite des Bildes, auf der der Raumplan in Pixeln definiert ist

// Von den Folgenden Zeilen soll nur eine entkommentiert sein, da sonst die letztere die erstere überschreibt
// mapImage.style.width = `${originalScaleWidth}px`;  // Entkommentieren, um kalibrierte Größe zu sehen
rescaleMapImage();  // Kommentieren, wenn die obige Zeile entkommentiert ist

const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
const updateSvgScale = () => {
    const mapRect = mapImage.getBoundingClientRect();
    const scale = mapImage.clientWidth / mapImage.naturalWidth;
    const svgWidth = mapImage.naturalWidth * scale;
    const svgHeight = mapImage.naturalHeight * scale;
    svg.setAttribute("style", `position: absolute; top: ${mapRect.top}px; left: ${mapRect.left}px; width: ${svgWidth}px; height: ${svgHeight}px; pointer-events: none;`);
}
window.addEventListener("resize", updateSvgScale);
updateSvgScale();
mapImage.parentNode.appendChild(svg);


await fetch("Test_Gebäudeplan\\facilities\\Test_Gymnasium\\building_01\\floor_01\\Gebäudeplan_Bsp.json")
    .then(response => response.json())
    .then(data => {
        JSONData = data;
        let map = data.maps[0];
        currentMap = map;
        for (let room of map.rooms) {
            const area = room;
            const areaElement = document.createElement("area");
            areaElement.setAttribute("shape", area.shape);
            const updateAreaElementScale = () => {
                const scale = mapImage.clientWidth / originalScaleWidth;
                const areaCoords = area.coords.map(coord => coord * scale);
                areaElement.setAttribute("coords", areaCoords.join(","));
            };
            window.addEventListener("resize", updateAreaElementScale);
            updateAreaElementScale();
            areaElement.onclick = (() => roomClicked(area));
            document.querySelector("map").appendChild(areaElement);
        }

    });

function roomClicked(area) {
    const oldPath = svg.querySelector("#" + area.names[0]);
    if (oldPath) {  // Wenn ein Pfad für diesen Raum bereits existiert, entferne ihn, statt einen neuen zu erstellen
        oldPath.remove();
        selectedRooms.splice(selectedRooms.indexOf(area.names[0]), 1);
        selectedRoomPaths.splice(selectedRoomPaths.indexOf(oldPath), 1);
    } else {
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.id = area.names[0];

        const updateScale = () => {
            const scale = mapImage.clientWidth / originalScaleWidth;
            let d;
            if (area.shape === "rect") {
                const [x1, y1, x2, y2] = area.coords.map(c => c * scale);
                d = `M ${x1} ${y1} L ${x2} ${y1} L ${x2} ${y2} L ${x1} ${y2} Z`;
            } else if (area.shape === "poly") {
                const scaledCoords = area.coords.map(c => c * scale);
                const points = [];
                for (let i = 0; i < scaledCoords.length; i += 2) {
                    points.push(`${scaledCoords[i]} ${scaledCoords[i + 1]}`);
                }
                d = `M ${points.join(' L ')} Z`;
            }
            path.setAttribute("d", d);
        };
        window.addEventListener("resize", updateScale);
        updateScale();

        path.setAttribute("fill", "rgba(255, 0, 0, 0.5)");
        path.setAttribute("stroke", "none");

        svg.appendChild(path);

        // Limitiere die Anzahl der gewählten Räume auf Start- und Zielraum
        selectedRooms.push(area.names[0]);
        selectedRoomPaths.push(path);
        if (selectedRooms.length > 2) {
            const removedRoom = selectedRooms.shift();
            const removedPath = selectedRoomPaths.shift();
            removedPath.remove();
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
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.id = "walk";

    const existingPath = svg.querySelector("#walk");
    if (existingPath) {
        existingPath.remove();
    }

    const updatePathScale = () => {
        const scale = mapImage.clientWidth / originalScaleWidth;
        path.setAttribute("d", "M " + coordsList.map(coords => `${coords[0] * scale} ${coords[1] * scale} `).join("L"));
    }
    window.addEventListener("resize", updatePathScale);
    updatePathScale();
    path.setAttribute("stroke", "red");
    path.setAttribute("stroke-width", "5");
    path.setAttribute("fill", "none");
    svg.appendChild(path);
    drawnPaths.push(path);
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