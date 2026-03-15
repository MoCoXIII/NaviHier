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
