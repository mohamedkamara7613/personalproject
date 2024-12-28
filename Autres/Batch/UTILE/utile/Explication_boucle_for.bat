@echo off
del temp.txt
rem création d'un fichier
echo 1 >> temp.txt
echo 2 >> temp.txt
echo 3 >> temp.txt
echo 4 >> temp.txt
echo 5 >> temp.txt

rem visualisation du contenu
echo le fichier temp.txt contient les lignes suivantes:
more temp.txt

echo.

echo Pour chaque ligne du fichier afficher son contenu
FOR /f %%i IN (temp.txt) DO (
echo ligne %%i
)
pause