@echo off
::affiche le contenu du fichier test.bat
::for /f "tokens=*" %%a in (test.bat) do echo %%a
::remplacer les X par un entier (noombre)
::choice /t:o,X>nul (marche pas)
::TYPE NUL | CHOICE /N /CY /TY,X>NUL (marche pas)
::ping 127.0.0.1 -n 5 (marche)
ping localhost -n 5
pause>nul