@echo off
title Sauvegarde de personnage 
mode con cols=90 lines=20
color f4
:: nom, qtor, vie sont mes variables

:menu
cls
set /p nom=Entrez votre nom : 
if exist %nom%.save goto :exist	
if not exist %nom%.save goto :nexist

::recupere le fichier deja creer et affiche le contenu
:exist 
cls
for /f "tokens=1-3 delims=/" %%a in (%nom%.save) do set nom=%%a & set vie=%%b & set or=%%c
echo 	Informations de joueur
echo 	  Nom :%nom% 
echo 	  Vie : %vie% 
echo 	  Or  : %qtor% 
pause>nul
goto :menu

::creer le fichier et inscrit les informations
:nexist
cls
set /p vie= nombre vie : 
set /p qtor= Quantite or : 
echo. %nom%/%vie%/%qtor%>%nom%.save
pause>nul
goto :menu
