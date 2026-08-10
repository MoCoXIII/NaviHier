@echo off

echo Um den Server zu stoppen, bitte das Batch Script beenden oder das Fenster/Tab schließen.
echo Der NaviHier Server wird lokal auf dieser Maschine unter http://127.0.0.1:8080/ erreichbar sein.
echo Um auf ihn im lokalen Netzwerk zuzugreifen,
echo ist die IP-Adresse dieser Maschine via ipconfig zu ermitteln und statt 127.0.0.1 zu verwenden.
choice /m "Soll ipconfig die lokale IP-Adresse dieser Maschine anzeigen?"
if %ERRORLEVEL%==1 ipconfig
echo Starten des NaviHier Servers...

: run
call node index.js
:: npm install ruft ein anderes Script auf.
:: dieses Script wird dadurch beendet.
:: das Stichwort call umgeht dieses Problem.
:: daher sitzt call vor allen node und npm Befehlen
call npm install
call node index.js
net session || (
    echo Die Installation von Node.js und Chocolatey braucht Administratorrechte.
    echo Bitte starte das Skript als Administrator erneut.
    pause & exit
)
: install
powershell -c "choco install nodejs -y --force"
call npm install
call node index.js
powershell -c "irm https://community.chocolatey.org/install.ps1|iex"
goto install
