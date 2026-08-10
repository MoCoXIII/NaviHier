@echo off

echo Um den Server zu stoppen, bitte das Batch Script beenden oder das Fenster/Tab schließen.
echo NaviHier Server starten...

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
