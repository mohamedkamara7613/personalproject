@echo off
set local enableDelayedExpansion
mode con cols=90 lines=20
color 3f
::Fond blanc sur turquoise

:menu
cls
echo 	           Quel type de transfert voulez faire:
echo.
echo                      1.Continuer     2.Quittez
echo.
choice /c 12 /n
if %errorlevel%==2 goto :Quittez
if %errorlevel%==1 goto :alldir
goto :menu

:alldir
cls
echo.
echo Ce programme s'aprette a faire le transfert de tout le continue du repertoires specifies
echo Veuillez vous assurer que vous disposer les chemins de source et de destination !!!
echo.
::Demande fait avec fichier vbs
::Demande le chemin de la source des fichiers et demande le chemin de la destination
pushd %~dp0
cscript "recuper_chemin_transfert.vbs"
popd
cls
set cheminSource=%1
set cheminDestination=%2
echo.
echo !!! Verifier bien le chemin specifier pour le transfert des fichiers !!!
echo.
::Donne le choix de verifier les chemins
echo 	1.Recommencer 2.Continuer 3.Menu
choice /c 123 /n
if %errorlevel%==3 goto :menu
if %errorlevel%==2 goto :suite
if %errorlevel%==1 goto :alldir

:suite
cls
echo.
echo La copie de tous les fichiers et sous-repertoires va commencer dans 5 secondes...
echo.
timeout /t 5 >nul

::Cette commande copie tous les fichiers les dossiers et les sous-repertoires de la source
::affiche les fichiers devant etre copier, exclut les dossiers vides, copie les fichier modifier a partir d'une date,
::continu la copie mm avec des erreurs, copie les fichiers caches
xcopy "%cheminSource%" "%cheminDestination%"  /D /S /C /H /K /I /Y
if %ERRORLEVEL% == 0 (
echo.>>sauve.save
echo Le %DATE% A %TIME%----------------------------------------------->>sauve.save
echo TRANSFERT DE : "%cheminSource%" VERS : "%cheminDestination%">>sauve.save
)
::Cette commande va copier les fichiers cachés et en lecture seule et créer le dossier de destination et les sous-dossiers s'ils n'existent pas
::xcopy C:\unDossier E:\dossierSauvegarde /D /E /C /R /H /I /K /Y
echo .............................Le transfert terminer !!!.............................
pause>nul
goto :menu

:Quittez
echo.
echo ..............................A la prochaine merci.......................................
echo.
timeout /t 5 /nobreak
exit
