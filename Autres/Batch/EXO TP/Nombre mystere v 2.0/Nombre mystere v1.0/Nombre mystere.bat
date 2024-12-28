@echo off
title Numero mystere
mode con cols=90 lines=30
color f0
::_________________________________________________________________________________________________________________________________________________________________
:debut
cls
set niveau=1
set saut=0
set faux=0 & set vrai=0
::_________________________________________________________________________________________________________________________________________________________________
:myster
set /a saut=%saut%+100
:random
set  myster=%RANDOM%
if %myster% GTR %saut% goto :random
if %myster% LSS 1 goto :random
if %saut% GTR 100 goto :niveau%niveau%
::_________________________________________________________________________________________________________________________________________________________________
:niveau11
cls
color f0
echo v 1.0
echo.
echo 	Bienvenu dans le jeu du nombre mystere. Il y a 10 niveau
echo.
echo 	 et a chaque niveau le nombre maximum augmente de 100
echo.
echo		1.Continuer 2.Historique
choice /c 12 /n
if %errorlevel% == 2 goto :Historique
if %errorlevel% == 1 goto :next
:next
echo SVP le nom ne doit pas contenir d'espace ni de caracteres speciaux
set /p nom=Entrez votre nom : 
if not exist "%nom%".save @echo 	Nom : %nom%>"%nom%".save
@echo TIME : %TIME% DATE : %DATE%>>"%nom%".save
timeout /t 10 
::_________________________________________________________________________________________________________________________________________________________________
:niveau1
color f0 
cls
echo.
echo %myster%							Niveau 1
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 100) : 

if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau2
color f0
cls
if %saut% LSS 200 goto :myster
echo.
echo %myster%							Niveau 2
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 0 et 200) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau3
color f0
cls
if %saut% LSS 300 goto :myster
echo.
echo %myster%							Niveau 3
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 300) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau4
color f0
cls
if %saut% LSS 400 goto :myster
echo.
echo %myster%							Niveau 4
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 400) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau5
color f0
cls
if %saut% LSS 500 goto :myster
echo.
echo %myster%							Niveau 5
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 500) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau6
color f0
cls
if %saut% LSS 600 goto :myster
echo.
echo %myster%							Niveau 6
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 600) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau7
color f0
cls
if %saut% LSS 700 goto :myster
echo.
echo %myster%							Niveau 7
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 700) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau8
color f0
cls
if %saut% LSS 800 goto :myster
echo.
echo %myster%							Niveau 8
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 800) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau9
color f0
cls
if %saut% LSS 900 goto :myster
echo.
echo %myster%							Niveau 9
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 900) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:niveau10
color f0
cls
if %saut% LSS 1000 goto :myster
echo.
echo %myster%							Niveau 10
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et 1000) : 
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo
::_________________________________________________________________________________________________________________________________________________________________
:inferieur
cls
color cf
set /a faux=%faux%+1
echo.
echo 		Le nombre mystere est plus petit
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :niveau%niveau%
::_________________________________________________________________________________________________________________________________________________________________
:superieur
cls
color cf
set /a faux=%faux%+1
echo.
echo 		Le nombre mystere est plus grand
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :niveau%niveau%
::_________________________________________________________________________________________________________________________________________________________________
:bingo
cls
color a1
set /a niveau=%niveau%+1
set /a vrai=%vrai%+1
set /a niv=%niveau%-1
echo 	Niveau%niv% >>"%nom%".save
echo FAUX : %faux%	VRAI : %vrai% >>"%nom%".save
echo.
echo Bravo !! Bravo !!Bravo !!Bravo !!Bravo !!Bravo !!Bravo
echo. 
echo 	NIVEAU : Niveau%niveau%
echo. 
echo.		NOM  : %nom% 
echo. 
echo		FAUX : %faux%
echo		VRAI : %vrai%
echo.
echo 	Tapez : 1.Continuer 2.Historique 3.Quitter
choice /c 12 /n
if %errorlevel% == 3 exit
if %errorlevel% == 2 goto :Historique
if %errorlevel% == 1 goto :niveau%niveau% 

:Historique
cls
color f0
echo 1.Continuer 2.Quitter
choice /c 12 /n
if %errorlevel% == 2 goto :niveau11
if %errorlevel% == 1 goto :suivant
:suivant
cls
set /p joueur=Entrez le nom du joueur : 
if exist "%joueur%".save more "%joueur%".save
if not exist "%joueur%".save echo Ce joueur n'existe pas & pause>nul & goto :Historique
pause>nul
goto :niveau11