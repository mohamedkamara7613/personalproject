rem désactive l'affichage des commandes
@echo off
rem remise à blanc de l'écran
cls
echo variable de base date: %date%
rem découpage %date:~0,2%
rem 1er chiffre numéro du caractère de début de la sélection
rem 2eme chiffre nombre de caractères après le début
echo Nous sommes le %date:~0,2% le %date:~3,2%eme mois de l'annee %date:~6,4% 
rem arrêt
pause