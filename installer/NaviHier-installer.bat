@echo off

echo Dieser Installer installiert das NaviHier Repository auf einer Windows Maschine.
echo [31mDer Installer sollte NICHT innerhalb des NaviHier Repository Ordners gestartet werden.[0m
pause & echo.

echo Die Installation ist nur in folgenden Anwendungen sinnvoll:
echo - Diese Maschine soll einen NaviHier Server hosten.
echo - Auf dieser Maschine sollen Kartendaten eines NaviHier Servers aufbereitet werden.
echo   (Dies ist beispielsweise das Erstellen von Wegpunkten, Verbindungen und Zielen durch das Host-Programm.)
echo - Auf dieser Maschine soll am NaviHier Projekt gearbeitet werden.
echo   (NaviHier ist Open-Source. Jeder darf sinnvoll dazu beitragen.)
echo.
echo Sind keine dieser Anwendungen gewollt, muss NaviHier nicht installiert werden.
echo Bitte beenden Sie dieses Skript, wenn NaviHier nicht installiert werden soll.
echo Wenn Sie fortfahren, werden auch chocolatey und git installiert (sofern nicht vorhanden).
pause & echo.

: clone
echo Es wird versucht, das NaviHier Repository zu klonen.
echo [31mWICHTIG: Das Repository wird als neuer Ordner mit dem Namen "NaviHier" erscheinen.
echo Wurde diese Datei durch Doppelklick gestartet, wird dieser Ordner im Verzeichnis der Datei erscheinen.[0m
echo Stellen Sie sicher, dass diese Datei im korrekten Verzeichnis liegt.
echo [31mWenn Sie nicht genau wissen, was Sie tun, starten Sie das Skript bitte nur per Doppelklick aus dem Datei-Explorer.[0m
echo Beenden Sie das Skript, wenn Sie unsicher sind.
pause & echo.
call git clone https://github.com/MoCoXIII/NaviHier || (
    echo Ist das Klonen fehlgeschlagen, ist git eventuell nicht installiert.
    echo Ist der git Befehl aus einem anderen Grund fehlgeschlagen, beenden Sie bitte das Skript und beheben Sie den angezeigten Fehler manuell.
    echo Fahren Sie bitte fort, wenn git nicht installiert ist.
    pause & echo.
    goto git
)
echo Das NaviHier Repository wurde erfolgreich geklont.
echo Wenn Sie fortfahren, beenden Sie das Skript.
echo Das Fenster verschwindet danach von selbst.
pause & exit

: git
net session || (
    echo Damit Chocolatey git korrekt installieren kann, muss das Skript als Administrator gestartet werden.
    echo Bitte starten Sie es als Administrator erneut. Fortfahren beendet das Programm, wobei das Fenster verschwinden kann.
    pause & exit
)
echo Nach dem Fortfahren wird versucht, git mit Chocolatey zu installieren.
pause & echo.
powershell -c "choco install git -y" || (
    echo Konnte git nicht installiert werden, kann dies daran liegen, dass Chocolatey nicht installiert ist.
    echo Fahren Sie bitte fort, wenn dies der Fall ist, um Chocolatey automatisch zu installieren.
    echo Beheben Sie andernfalls den Fehler manuell und beenden Sie das Skript.
    pause & echo.
    goto choco
)
echo Git wurde installiert.
echo Wenn dies stimmt, kann mit einem weiteren Klonversuch fortgefahren werden.
pause & echo.
goto clone

: choco
echo Chocolatey ist ein Paketmanager.
echo Mit diesem installiert NaviHier die meisten erforderlichen Programme.
echo Damit der Installer alle gebrauchten Skripte starten kann, wird die Windows ExecutionPolicy des aktuellen Nutzers aufgehoben.
echo Fahren Sie fort, um den Paketmanager Chocolatey zu installieren.
pause & echo.

::powershell -c "Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process"
powershell -c "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted"

powershell -c "irm https://community.chocolatey.org/install.ps1|iex"

echo Chocolatey wurde installiert.
echo Die Konsole muss eventuell neu gestartet werden, um auf Choco zuzugreifen.
echo Fortfahren beendet das Skript. Starten Sie es danach erneut.
pause & exit
