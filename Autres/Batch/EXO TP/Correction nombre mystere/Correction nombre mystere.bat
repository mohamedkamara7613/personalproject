@echo off

set nombreMin=0
set nombreMax=100
set nombreCoups=0

:choix_difficulte
  set /p difficulte=Choisissez un niveau de difficulte, entre 1 et 10 : 
    if %difficulte%==1 set nombreMax=10
    if %difficulte%==2 set nombreMax=100
    if %difficulte%==3 set nombreMax=500
    if %difficulte%==4 set nombreMax=1000
    if %difficulte%==5 set nombreMax=1500
    if %difficulte%==6 set nombreMax=2000
    if %difficulte%==7 set nombreMax=5000
    if %difficulte%==8 set nombreMax=10000
    if %difficulte%==9 set nombreMax=15000
    if %difficulte%==10 set nombreMax=30000

:: Choisissons un nombre aléatoire.
:nombre_alea
    set nombremystere=%RANDOM%
    if %nombremystere% gtr %nombreMax% goto nombre_alea
    if %nombremystere% lss %nombreMin% goto nombre_alea

:debut
    set /p nombrechoisi=Choisis un nombre :
    set /a nombreCoups=%nombreCoups%+1
    if %nombrechoisi% lss %nombremystere% goto superieur
    if %nombrechoisi% gtr %nombremystere% goto inferieur
    goto fin

:superieur
    echo Le nombre mystere est superieur.
    goto debut

:inferieur
    echo Le nombre mystere est inferieur.
    goto debut

:fin
    echo Bien joue ! Ton as gagne en %nombreCoups% coup(s).
    if not exist scores.txt (
        echo Nb coups - Niveau > scores.txt
    )
    echo %nombreCoups% - %difficulte% >> scores.txt
    set /p recommencer=Voulez-vous recommencer ? (1 = oui ; 2 = non) : 
    if %recommencer%==1 ( goto choix_difficulte ) else ( exit )

pause