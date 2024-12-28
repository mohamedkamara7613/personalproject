 rem désactive l'affichage des commandes
echo off
rem remise à blanc de l'écran
cls
rem liste des variables 
echo Salut %USERNAME%,nous sommes le %DATE% 
echo il est %Time% déja!, 
echo %RANDOM% est un chiffre aléatoire.
echo Ton PC se nomme %COMPUTERNAME%,
echo il possède %NUMBER_OF_PROCESSORS% processeur,
echo c'est une architecture %PROCESSOR_IDENTIFIER% 
rem arrêt
pause