::Pour executer du script visual basic dans la mm fenetre de maniere synchrone
::il faut executer la commande "pushd %~dp0" pour memoriser le repertoire actuel de travail
::Puis "cscript" suivie du chemin du fichier a executer
::et enfin "popd" pour retourner dans le repertoire precedent et continuer le script batch
@echo off
pushd %~dp0
::echo %~dp0
cscript test.vbs
popd
cls
set /p nom= Quelle est votre nom ?
color fc
pause>nul
