@echo off
setlocal EnableDelayedExpansion
set file="lien1.txt"
echo.
If not exist %file% (pause>nul|echo Le fichier %file% n'existe pas, fermeture du script. &exit)
set var = 1
echo Tout sur une ligne :
for /l %%i in ("54") do (
for /f "usebackq Tokens= Delims=\" %%x in (%file%) do set Build1=!Build1!%%x & start !Build1! & set /a var = %%var + 1
)
exit

echo Pour du multi-lignes :
set NL=^
 
 
for /f "usebackq Tokens=* Delims=" %%z in (%file%) do set Build2=!Build2!!NL!%%z
echo !Build2!
pause>nul|echo Fin du script.
