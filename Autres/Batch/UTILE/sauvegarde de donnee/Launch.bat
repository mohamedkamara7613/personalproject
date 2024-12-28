@echo off
title Sauvegarde de donnnée (programmation) vers disque dur 
color 0c
mode con cols=60 lines=20

::Permet de faire une sauvegarde des fichiers liés a la programmation vers mon disque dur
set destination1=\INFORMATIQUE\programmation\Developement web\HTML5-CSS
set destination2=\INFORMATIQUE\programmation\Langage batch
set destination3=\INFORMATIQUE\programmation\Algorythme
set destination4=\INFORMATIQUE\programmation\Langage C

::Copie de HTML5-CSS vers disque dur de sauvegarde
xcopy "C:\Users\USER\Desktop\HTML5-CSS" "%destination1%" /D /E /C /H /K /I /Y

::Copie de Langage batch vers disque dur de sauvegarde
xcopy "C:\Users\USER\Desktop\Langage batch" "%destination2%" /D /E /C /H /K /I /Y

::Copie de Algorythme vers disque dur de sauvegarde
xcopy "C:\Users\USER\Desktop\Algorythme" "%destination3%" /D /E /C /H /K /I /Y

::Copie de Langage C vers disque dur de sauvegarde
xcopy "C:\Users\USER\Desktop\Langage C" "%destination4%" /D /E /C /H /K /I /Y
PAUSE