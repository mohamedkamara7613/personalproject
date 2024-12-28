
@echo off
if exist sd.fn goto :menu
set v=V 8.5
color 1a
title find numbers
mode con cols=83 lines=25
ping 127.0.0.1 -n 2 > nul
echo.
echo.               êêêêêêêêêêêêê   êêê   êêêêê    êêê  êêêêêêêê
echo.               ê           ê    êê     êê      ê     ê     ê
echo.               ê                 ê     êêê     ê     ê      ê
echo.               ê                 ê     ê  ê    ê     ê      ê
echo.               êêêêêêêê          ê     ê   ê   ê     ê      ê
echo.               ê                 ê     ê    ê  ê     ê      ê
echo.               ê                 ê     ê     ê ê     ê      ê
echo.               ê                 ê     ê      êê     ê     ê
echo.              êêêêê            êêêêê  êêê    êêêê  êêêêêêêê
echo.
echo.
echo.
echo.    êêêêê    êêê   êêê      êêê  êêê        êêê  êêêêêêê    êêêêêêêê     êêêêêê
echo.     êê      ê      ê        ê    êê         êê   ê     êê    ê           ê   ê ©
echo.     êêê     ê      ê        ê    ê ê       ê ê   ê      ê    ê           ê    ê
echo.     ê  ê    ê      ê        ê    ê  ê     ê  ê   ê      ê    ê           ê    ê
echo.     ê   ê   ê      ê        ê    ê   ê   ê   ê   ê      ê    ê           ê    ê
echo.     ê    ê  ê      ê        ê    ê    ê ê    ê   êêêêêêê     êêêêêêê     êêêêê
echo.     ê     ê ê      ê        ê    ê     ê     ê   ê      ê    ê           ê  ê
echo.     ê      êê      ê        ê    ê     ê     ê   ê     êê    ê           ê   ê
echo.    êêê     êêê      êêêêêêêê    êêê   êêê   êêê êêêêêêêê    êêêêêêêê    êêê   êê
echo.                                                                            %v%
echo.
ping 127.0.0.1 -n 3 > nul
mode con lines=20 cols=73
title by PR
cls
echo.
echo.
echo.
echo.
echo.   888888b.                  8888888b.     88888888b. TM
echo.   888  "88b                 888    "88b   888     "88b
echo.   888  .88P                 888      888  888       88
echo.   8888888p.  888  888       888     888   888      88
echo.   888  "Y88b 888  888       88888888      88888888R
echo.   888    888 888  888       888           888    888
echo.   888   d88P Y88b 888       888           888     888
echo.   8888888P"   "Y88888       888           888      888
echo.                   888
echo.              l8b d88P
echo.                "Y88P"                               copyright © 2015 PR

ping 127.0.0.1 -n 3 > nul

:menu
if exist sd.fn del sd.fn
set no=0
mode con cols=50 lines=10
title ---------+=find numbers=+---------
cls
echo. ÉÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ»
echo. º  1.commencer                   º
echo. º  2.options des scores          º
echo. º  3.quitter                     º
echo. ÈÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ¼
echo.                                      %v%
set /p no=
if "%no%"=="1" goto :ch niv
if "%no%"=="2" goto :2
if "%no%"=="3" goto :fin
if not defined no goto :menu
goto :menu

:ch niv
set niv=0
mode con lines=20 cols=70
cls
echo  choisissez le niveau :
echo 1.facile
echo 2.difficile
set /p niv=
if "%niv%"=="0" goto :ch niv
if "%niv%"=="1" (set max=100
set /a n=%random%%%101
set /a nombrEssai=11
set "max2="
set "re= "
goto :bu)
if "%niv%"=="2" (set /a n=%random%%%101
set /a nombrEssai=6
set max2=100
set "max="
set "re= * 2"
goto :bu)
goto :ch niv

:bu

set /A nombrEssai-=1

:bu2
set nomb=y
cls
echo.choisiser un nombre entre 0 et %max%%max2%              essai restant=%nombrEssai%
echo.==================================
set /p nomb=

if "%nomb%"=="y" goto :bu2
if %nomb%==%n% goto :bon
if %nombrEssai%==0 goto :fin2
if not defined nomb goto :bu2
if %nomb% GTR %n% goto :moins
if %nomb% LSS %n%  goto :plus
goto :bu2

:fin2
cls
echo. le nombre de faute maximale est depasse!!
echo. il falait trouv‚ %n% .
ping 127.0.0.1 -n 3 >nul

:fin23
cls
set loose=8
echo voulez vous rejouer ?
echo. 1.oui
echo. 2.non
set /p loose=
if "%loose%"=="8" goto :fin 23
if "%loose%"=="oui" call %%0
if "%loose%"=="non" goto :fin
goto :fin 23

:2
set sco=0
cls
mode con cols=50 lines=10
title scores
echo 1.voir les scores
echo.2.voir les meilleurs scores
echo 3.supprimer les scores
echo 4.revenir au menu principal

set /p sco=
if not defined sco goto :2
if "%sco%"=="1" goto :look
if "%sco%"=="2" goto :lookbest
if "%sco%"=="3" goto :del
if "%sco%"=="4" goto :menu
goto :2

:lookbest
mode con lines=20 cols=75
cls
if not exist ms.fn echo aucun meilleurs scores !!&ping 127.0.0.1 -n 3 > nul&goto :menu
more<ms.fn
pause>nul
goto :menu

:look
mode con lines=20 cols=75
cls
if not exist scores.fn (echo.                       aucun r‚sultat !&ping 127.0.0.1 -n 3 > nul
goto :menu)
more <scores.fn
pause>nul
goto :menu

:del

set e=0
mode con cols=60 lines=10
cls
set/p e=voulez vous vraiment supprimer les scores(oui ou non) ?
if not exist scores.fn echo les scores n'existe pas !&ping 127.0.0.1 -n 2 > nul&goto :menu
if "%e%"=="0" goto :menu
if "%e%"=="oui" del scores.fn&goto :menu
if "%e%"=="non" goto :menu
goto :del
:moins
echo c'est moins!!
ping 127.0.0.1 -n 2 > nul
goto :bu

:plus
echo c'est plus !!
ping 127.0.0.1 -n 2 > nul
goto :bu

:bon
set /a t=%nombressai% * 20 %re%
cls
echo.                                                 essai restant=%nombrEssai%
echo %n%
set h=*
if "%max2%"=="100" set inf niv2=niv diff
if "%max%"=="100" set inf niv2=niv facile
set u=
if not exist scores.fn set u=echo.   copyright © PR
echo. vous avez trouvez le bon nombre !!
ping 127.0.0.1 -n 2 > nul
if "%nombressai%"=="0" set t=10
set /p h=quel est votre prenom ?
if "%h%"=="*" goto :bon
(
%u%
echo.==============================================================
echo.le %date% … %time% ^| %inf niv2% : %h% = %t% points.)>>scores.fn
echo sd>sd.fn
if %t% GEQ 100 goto :win
call %%0

:fin
if exist "sd.fn" del sd.fn
mode con cols=50 lines=10
cls
echo.        … bient“t !
ping 127.0.0.1 -n 3 > nul
exit

:win
mode con cols=32 lines=5
set "c="
if not exist ms.fn set c=echo meilleurs scores :
cls
echo.
echo. ÉÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ»
echo. ºnouveau meilleur score !!!  º
echo. ÈÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍÍ¼

(
%c%
echo.==============================================================
echo.le %date% … %time% ^| %inf niv2% : %h% = %t% points.)>>ms.fn
ping 127.0.0.1 -n 3 > nul
call %%0
