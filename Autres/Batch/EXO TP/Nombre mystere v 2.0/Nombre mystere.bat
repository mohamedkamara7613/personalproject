@echo off
set local EnableDelayedExpansion
title Numero mystere
mode con cols=70 lines=20
color f0

:debut
cls
set nom=inconnu
set saut=0
set coup=0
set niv=1
set tmp=0
set triche=14

:menu
cls
color f0
echo v 2.0
echo.
echo 	Bienvenu dans le jeu du nombre mystere. Il y a 9 niveau
echo.
echo 	 et a chaque niveau le nombre maximum augmente de 100
echo.
echo		1.Commencer 2.Choix niveau 3.Historique
choice /c 123 /n
if %errorlevel% == 3 goto :Historique
if %errorlevel% == 2 goto :lvlselect
if %errorlevel% == 1 goto :next

:lvlselect
echo.
echo 	Choississez un niveau de 1 a 9
echo.
echo   		[1] Entre 1 et 100
echo   		[2] Entre 1 et 200
echo   		[3] Entre 1 et 300
echo   		[4] Entre 1 et 400
echo   		[5] Entre 1 et 500
echo   		[6] Entre 1 et 600
echo   		[7] Entre 1 et 700
echo   		[8] Entre 1 et 800
echo   		[9] Entre 1 et 900
choice /c 123456789 /n
if %errorlevel% == 9 (set /a saut=800 & set /a niv=9)
if %errorlevel% == 8 (set /a saut=700 & set /a niv=8)
if %errorlevel% == 7 (set /a saut=600 & set /a niv=7)
if %errorlevel% == 6 (set /a saut=500 & set /a niv=6)
if %errorlevel% == 5 (set /a saut=400 & set /a niv=5)
if %errorlevel% == 4 (set /a saut=300 & set /a niv=4)
if %errorlevel% == 3 (set /a saut=200 & set /a niv=3)
if %errorlevel% == 2 (set /a saut=100 & set /a niv=2)
if %errorlevel% == 1 (set /a saut=0 & set /a niv=1)

:next
cls
echo   SVP le nom ne doit pas contenir d'espace ni de caracteres speciaux
set /p nom=Entrez votre nom : 
if not exist "%nom%".save echo 		Joueur : %nom% >>NomDeJoueur.save
if not exist "%nom%".save @echo 	Nom : %nom%>"%nom%".save
@echo TIME : %TIME% DATE : %DATE%>>"%nom%".save

:myster
set /a saut=%saut%+100
set /a myster=%RANDOM%%%saut%
if %RANDOM%==0 goto :myster
goto :suivant
:suivant
color f0 
cls
if %myster%==%tmp% call :myster
echo.
echo    	                          Niveau %niv%
echo.
set nombre=0
set /p nombre=Tapez un nombre  (entre 1 et %saut%) : 

if %nombre%==%triche% goto :bingo
if %nombre% GTR %myster% goto :inferieur
if %nombre% LSS %myster% goto :superieur
goto :bingo

:inferieur
cls
color cf
set /a coup=%coup%+1
echo.
echo 		Le nombre mystere est plus petit
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :suivant

:superieur
cls
color cf
set /a coup=%coup%+1
echo.
echo 		Le nombre mystere est plus grand
echo.
echo 	Appuyez sur entrer pour retenter votre chance
pause>nul
goto :suivant

:bingo
cls
color a1
if %niv% LSS 10 set /a niv=%niv%+1
set /a coup=%coup%+1
set /a niv1=%niv%-1
echo 	Niveau%niv1% >>"%nom%".save
echo 	NOMBRE DE COUP : %coup% >>"%nom%".save
echo.
echo 	Bravo !! Bravo !!Bravo !!Bravo !!Bravo !!Bravo !!Bravo
echo. 
echo 		NIVEAU : %niv1%
echo. 
echo 		NOM  : %nom% 
echo. 
echo 		NOMBRE DE COUP : %coup%
echo.
set coup=0
set /a tmp=%myster%
if %niv%==10 goto :lvlselect
echo 	Tapez : 1.Continuer 2.Historique 3.Quitter
choice /c 123 /n
if %errorlevel% == 3 exit
if %errorlevel% == 2 goto :Historique
if %errorlevel% == 1 goto :suivant 

:Historique
cls
color f0
echo.
echo.
echo.
echo 			1.Continuer 	2.Quitter
choice /c 12 /n
if %errorlevel% == 2 goto :menu
if %errorlevel% == 1 goto :inditentification
:inditentification
cls
type NomDeJoueur.save
set /p joueur=Entrez le nom du joueur : 
if exist "%joueur%".save more "%joueur%".save
if not exist "%joueur%".save echo Ce joueur n'existe pas & pause>nul & goto :Historique
pause>nul
goto :menu