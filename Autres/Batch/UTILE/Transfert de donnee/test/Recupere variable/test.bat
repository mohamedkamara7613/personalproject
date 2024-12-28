@echo off
:: On récupère la valeur depuis le fichier "temp.txt"
set /P VAR=< temp.txt
:: On supprime le fichier
del temp.txt
cls
echo.
echo La variable inputbox est : %VAR%
echo.
pause
