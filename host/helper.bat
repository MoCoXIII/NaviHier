@echo off
:: batch-Dokumentation siehe https://en.wikibooks.org/wiki/Windows_Batch_Scripting

echo Dieses Skript automatisiert sinnvolle Funktionen rund um das NaviHier Host-Programm
:: Beim Schreiben von Nutzerinteraktionen ist zu beachten, dass echo UTF-8 nicht unterstützt, weshalb Sonderzeichen wie äöü vermieden werden sollten.
echo.
echo.
:: https://ss64.com/nt/syntax-ansi.html für Color-Codes
:: Escape Character  von https://gist.githubusercontent.com/mlocati/fdabcaeb8071d5c75a2d51712db24011/raw/b710612d6320df7e146508094e84b92b34c77d48/win10colors.cmd
echo [31m WICHTIG: Dieses Skript ist nur von Entwicklern zu nutzen. Bitte beende das Programm, wenn du nicht sicher bist, was du tust. [0m
echo.
echo.

: choose
echo Folgende Funktionen sind von diesem Programm abrufbar:
echo 1: pipreqs installieren
echo 2: requirements.txt mit pipreqs erzeugen und ersetzen (Bibliotheken bitte vorher installiert haben)
echo 3: Bibliotheken aus requirements.txt installieren
echo 4: Beenden

choice /c 1234 /m "Welche Funktion soll abgerufen werden?"
if %ERRORLEVEL%==1 goto pipreqs
if %ERRORLEVEL%==2 goto requirements
if %ERRORLEVEL%==3 goto install
if %ERRORLEVEL%==4 goto done

: pipreqs
pip install pipreqs
goto choose

: requirements
pipreqs --use-local --force
:: --use-local ist wichtig, damit pygame-ce, wenn es über das Stichwort "pygame" importiert wird,
:: nicht als "pygame" in die requirements.txt eingetragen wird.
:: "pygame" kann von pip nicht aus einer requirements.txt geladen werden.
:: pygame-ce ist eine Abhängigkeit von easypygamewidgets, also wird pygame-ce dadurch installiert.
goto choose

: install
pip install -r requirements.txt
goto choose

: done
exit